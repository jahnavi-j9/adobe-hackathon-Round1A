import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re
import os
import json
from typing import List, Dict, Tuple

class MLHeadingExtractor:
    def __init__(self, model_path="models/heading_model.pkl"):
        self.model = None
        self.model_path = model_path
        self.feature_columns = [
            'font_size', 'is_bold', 'is_italic', 'cap_ratio', 'x_pos_norm', 
            'y_pos_norm', 'line_length', 'word_count', 'starts_with_number',
            'ends_with_colon', 'all_caps', 'relative_font_size', 'indentation',
            'vertical_spacing_above', 'vertical_spacing_below'
        ]
        
    def extract_text_features(self, doc) -> List[Dict]:
        """Extract comprehensive features from PDF text blocks"""
        all_features = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            page_width = page.rect.width
            page_height = page.rect.height
            
            # Extract all text elements with positions
            text_elements = []
            for block in blocks:
                if block['type'] == 0:  # text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_elements.append({
                                'text': span['text'].strip(),
                                'font_size': span['size'],
                                'is_bold': 'Bold' in span['font'],
                                'is_italic': 'Italic' in span['font'],
                                'x0': span['bbox'][0],
                                'y0': span['bbox'][1],
                                'x1': span['bbox'][2],
                                'y1': span['bbox'][3],
                                'page': page_num + 1
                            })
            
            # Calculate relative features
            if text_elements:
                font_sizes = [elem['font_size'] for elem in text_elements]
                median_font_size = np.median(font_sizes)
                
                # Sort by y-position for spacing calculations
                text_elements.sort(key=lambda x: x['y0'])
                
                for i, elem in enumerate(text_elements):
                    if not elem['text']:
                        continue
                        
                    features = self._extract_line_features(
                        elem, median_font_size, page_width, page_height,
                        text_elements, i
                    )
                    all_features.append(features)
        
        return all_features
    
    def _extract_line_features(self, elem, median_font_size, page_width, page_height, 
                              all_elements, index) -> Dict:
        """Extract features for a single text line"""
        text = elem['text']
        
        # Basic features
        features = {
            'text': text,
            'font_size': elem['font_size'],
            'is_bold': int(elem['is_bold']),
            'is_italic': int(elem['is_italic']),
            'page': elem['page']
        }
        
        # Typography features
        features['cap_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        features['line_length'] = len(text)
        features['word_count'] = len(text.split())
        
        # Layout features
        features['x_pos_norm'] = elem['x0'] / page_width
        features['y_pos_norm'] = elem['y0'] / page_height
        features['indentation'] = elem['x0']
        
        # Relative features
        features['relative_font_size'] = elem['font_size'] / median_font_size
        
        # Content pattern features
        features['starts_with_number'] = int(bool(re.match(r'^\d+\.?\d*', text)))
        features['ends_with_colon'] = int(text.endswith(':'))
        features['all_caps'] = int(text.isupper() and len(text) > 1)
        
        # Spacing features
        features['vertical_spacing_above'] = self._calculate_spacing_above(
            elem, all_elements, index
        )
        features['vertical_spacing_below'] = self._calculate_spacing_below(
            elem, all_elements, index
        )
        
        return features
    
    def _calculate_spacing_above(self, elem, all_elements, index) -> float:
        """Calculate vertical spacing above current element"""
        if index == 0:
            return 0.0
        prev_elem = all_elements[index - 1]
        return elem['y0'] - prev_elem['y1']
    
    def _calculate_spacing_below(self, elem, all_elements, index) -> float:
        """Calculate vertical spacing below current element"""
        if index == len(all_elements) - 1:
            return 0.0
        next_elem = all_elements[index + 1]
        return next_elem['y0'] - elem['y1']
    
    def train_model(self, training_data_path: str):
        """Train the ML model from labeled data"""
        # Load training data
        df = pd.read_csv(training_data_path)
        
        # Prepare features and labels
        X = df[self.feature_columns]
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        print("Model Performance:")
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
    
    def predict_headings(self, features: List[Dict]) -> List[Dict]:
        """Predict heading labels for extracted features"""
        if not self.model:
            self.load_model()
        
        # Prepare feature matrix
        feature_df = pd.DataFrame(features)
        X = feature_df[self.feature_columns]
        
        # Make predictions
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        # Add predictions to features
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            features[i]['predicted_label'] = pred
            features[i]['confidence'] = np.max(prob)
        
        return features
    
    def extract_outline(self, pdf_path: str) -> Dict:
        """Main function to extract outline from PDF"""
        doc = fitz.open(pdf_path)
        
        # Extract features
        features = self.extract_text_features(doc)
        
        # Predict headings
        predicted_features = self.predict_headings(features)
        
        # Extract title and outline
        title = self._extract_title(predicted_features)
        outline = self._extract_outline_structure(predicted_features)
        
        doc.close()
        
        return {
            "title": title,
            "outline": outline
        }
    
    def _extract_title(self, features: List[Dict]) -> str:
        """Extract document title from predictions"""
        # Look for title predictions first
        title_candidates = [f for f in features if f['predicted_label'] == 'Title']
        if title_candidates:
            # Return the most confident title prediction
            return max(title_candidates, key=lambda x: x['confidence'])['text']
        
        # Fallback: largest text on first page
        first_page_features = [f for f in features if f['page'] == 1]
        if first_page_features:
            return max(first_page_features, key=lambda x: x['font_size'])['text']
        
        return ""
    
    def _extract_outline_structure(self, features: List[Dict]) -> List[Dict]:
        """Extract structured outline from predictions"""
        outline = []
        
        for feature in features:
            if feature['predicted_label'] in ['H1', 'H2', 'H3']:
                outline.append({
                    "level": feature['predicted_label'],
                    "text": feature['text'],
                    "page": feature['page']
                })
        
        # Sort by page and remove duplicates
        seen = set()
        unique_outline = []
        for item in sorted(outline, key=lambda x: (x['page'], x['text'])):
            key = (item['level'], item['text'], item['page'])
            if key not in seen:
                seen.add(key)
                unique_outline.append(item)
        
        return unique_outline

# Main extraction function for compatibility
def extract_outline(pdf_path: str) -> Dict:
    """Main function called by main.py"""
    extractor = MLHeadingExtractor()
    return extractor.extract_outline(pdf_path)

# Training script (run this once to train your model)
def train_heading_model():
    """Train the heading detection model"""
    extractor = MLHeadingExtractor()
    
    # You need to create training_data.csv with labeled examples
    # Format: text,font_size,is_bold,is_italic,cap_ratio,x_pos_norm,y_pos_norm,line_length,word_count,starts_with_number,ends_with_colon,all_caps,relative_font_size,indentation,vertical_spacing_above,vertical_spacing_below,label
    
    extractor.train_model("training_data.csv")

if __name__ == "__main__":
    # Uncomment to train model
    # train_heading_model()
    
    # Test extraction
    result = extract_outline("sample.pdf")
    print(json.dumps(result, indent=2))

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

def generate_dummy_pdf(filename="app/input/sample.pdf", pages=12):
    os.makedirs("app/input", exist_ok=True)
    c = canvas.Canvas(filename, pagesize=A4)
    for i in range(1, pages + 1):
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, 800, f"H1 Heading Page {i}")
        c.setFont("Helvetica", 16)
        c.drawString(100, 750, f"H2 Subheading Page {i}")
        c.setFont("Helvetica", 13)
        c.drawString(100, 700, f"H3 Minor Heading Page {i}")
        c.showPage()
    c.save()
    print(f"✅ Dummy PDF generated: {filename}")

if __name__ == "__main__":
    generate_dummy_pdf()

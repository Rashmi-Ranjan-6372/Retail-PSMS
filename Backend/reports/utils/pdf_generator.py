from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(data, file_name="report.pdf"):

    document = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    for item in data:

        elements.append(
            Paragraph(str(item), styles["BodyText"])
        )

    document.build(elements)

    return file_name
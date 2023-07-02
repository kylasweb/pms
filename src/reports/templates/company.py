from io import BytesIO

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

styles = getSampleStyleSheet()
title_styles = styles["Title"]
heading_style = styles["Heading1"]
subheading_style = styles["Heading2"]
normal_style = styles["Normal"]


def create_report(title: str, data: dict[str, str | dict[str, str]]):
    # Create a PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a stylesheet for styling the content

    title = Paragraph(f"<u>{title}</u>", title_styles)
    content = [title, Spacer(1, 20)]
    # Iterate over the company_id details and add them to the content list
    for heading, subheadings in data.items():
        # Heading

        heading_paragraph = Paragraph(heading, heading_style)
        content.extend((heading_paragraph, Spacer(1, 10)))
        if isinstance(subheadings, dict):
            # Subheadings and content
            for subheading, content_text in subheadings.items():
                subheading_paragraph = Paragraph(f"<strong>{subheading} : </strong> <em> {content_text}</em>", normal_style)
                content.append(subheading_paragraph)
        else:
            content_paragraph = Paragraph(subheadings, normal_style)
            content.extend((content_paragraph, Spacer(1, 5)))
        content.append(Spacer(1, 10))

    # Build the PDF document with the content
    doc.build(content)
    buffer.seek(0)
    return buffer





from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Define the content and styles
letter_title = "Business Letter"
sender_name = "Your Name"
sender_address = "Your Address"
recipient_name = "Recipient Name"
recipient_address = "Recipient Address"
letter_body = """
Dear {recipient_name},

I hope this letter finds you well. 

This is the body of the business letter.

Sincerely,
{sender_name}
"""

# Create the PDF and add content
doc = SimpleDocTemplate("business_letter.pdf", pagesize=letter)

styles = getSampleStyleSheet()
title_style = styles["Heading1"]
content_style = styles["BodyText"]

# Create a frame with a border
border_width = 1  # Adjust the border width as needed
frame_width = letter[0] - 2 * inch
frame_height = letter[1] - 2 * inch
border_frame = Frame(
    inch, inch, frame_width, frame_height, showBoundary=1, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
)

# Add the letter title
title = Paragraph(letter_title, title_style)
elements = [title, Spacer(1, 0.5 * inch)]
sender_info = Paragraph(
    f"<b>From:</b><br/>{sender_name}<br/>{sender_address}",
    content_style
)
elements.extend((sender_info, Spacer(1, 0.2 * inch)))
recipient_info = Paragraph(
    f"<b>To:</b><br/>{recipient_name}<br/>{recipient_address}",
    content_style
)
elements.extend((recipient_info, Spacer(1, 0.5 * inch)))
body = Paragraph(
    letter_body.format(recipient_name=recipient_name, sender_name=sender_name),
    content_style
)
elements.append(body)

# Add the border frame to the document
border_frame.addFromList(elements, doc)

# Build the PDF document
doc.build([])

from io import BytesIO

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.graphics.shapes import Line
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

styles = getSampleStyleSheet()
title_styles = styles["Title"]
heading_style = styles["Heading1"]
subheading_style = styles["Heading3"]
normal_style = styles["Normal"]


def create_report(title: str, data: dict[str, str | dict[str, str] | list[dict[str, str]]]):
    # Create a PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a stylesheet for styling the content

    title = Paragraph(f"<u>{title}</u>", title_styles)
    content = [title, Spacer(1, 20)]
    # Iterate over the company_id details and add them to the content list
    heading = "Company Details"
    heading_paragraph = Paragraph(heading, heading_style)
    content.extend((heading_paragraph, Spacer(1, 10)))
    for heading, subheadings in data.items():
        # Heading
        if heading.casefold() in ["properties"]:
            content.append(PageBreak())
            property_development = "Rental Properties"
            heading_paragraph = Paragraph(property_development, heading_style)
            content.extend((heading_paragraph, Spacer(1, 10)))
            content.extend(iter(create_property_development(subheadings)))
            continue
        else:
            heading_paragraph = Paragraph(heading, subheading_style)
            content.extend((heading_paragraph, Spacer(1, 10)))
        if isinstance(subheadings, dict):
            # Subheadings and content
            for subheading, content_text in subheadings.items():
                subheading_paragraph = Paragraph(f"<strong>{subheading} : </strong> <em> {content_text}</em>",
                                                 normal_style)
                content.append(subheading_paragraph)

        elif isinstance(subheadings, list):
            if isinstance(subheadings[0], dict):
                for item_object in subheadings:
                    for item_name, item_content in item_object.items():
                        item_paragraph = Paragraph(f"<strong>{item_name} : </strong> <em>{item_content} </em>",
                                                   normal_style)
                        content.append(item_paragraph)

            if isinstance(subheadings[0], str):
                formatted_items = format_to_ul_list(list_items=subheadings)
                item_paragraph = Paragraph(formatted_items, normal_style)
                content.append(item_paragraph)

        else:
            content_paragraph = Paragraph(subheadings, normal_style)
            content.extend((content_paragraph, Spacer(1, 5)))
        content.append(Spacer(1, 10))

    # Build the PDF document with the content
    doc.build(content)
    buffer.seek(0)
    return buffer


def convert_to_table_data(subheadings: list[dict[str, str]]) -> list[list[str]]:
    # Extract the keys from the first dictionary to use as column headers
    keys = list(subheadings[0].keys())

    # Create the table data with column headers
    table_data = [keys]

    # Iterate over the subheadings and extract the values for each key
    for subheading in subheadings:
        row = [subheading[key] for key in keys]
        table_data.append(row)

    return table_data


def format_to_ul_list(list_items):
    ul_list = "<ul>\n"
    for item in list_items:
        ul_list += f"<li>{item}</li>\n"
    ul_list += "</ul>"
    return ul_list


def create_property_development(data_list):
    # Get the sample styles for formatting
    sub_content = []
    line = Paragraph("<br/>", normal_style)
    if isinstance(data_list, list):
        horizontal_space = "                    "
        for item_object in data_list:
            # Add property name as subheading
            heading = Paragraph(item_object.get("name"), heading_style)
            sub_content.append(heading)
            # Add description
            description_heading = Paragraph("DESCRIPTION", subheading_style)

            sub_content.append(description_heading)
            description = Paragraph(f"<strong>{item_object.get('description')}</strong>", normal_style)
            sub_content.extend((description, line, line))
            # Add lease terms
            lease_heading = Paragraph("<strong>LEASE TERMS</strong>", subheading_style)
            sub_content.append(lease_heading)
            lease_terms = Paragraph(f"<strong>{item_object.get('lease_terms')}</strong>", normal_style)
            sub_content.extend((lease_terms, line, line))
            details_heading = Paragraph("<strong>DETAILS</strong>", subheading_style)
            sub_content.extend((details_heading, line, line))
            # Add property type
            property_type = Paragraph(f"Property Type:{horizontal_space} {item_object.get('property_type')}", normal_style)
            sub_content.append(property_type)

            # Add number of units
            number_of_units = Paragraph(f"Number of Units: {item_object.get('number_of_units')}", normal_style)
            sub_content.append(number_of_units)

            # Add available units
            available_units = Paragraph(f"Available Units: {item_object.get('available_units')}", normal_style)
            sub_content.extend((available_units, line))
            # Add amenities
            amenities = Paragraph(f"Amenities: {item_object.get('amenities')}", normal_style)
            sub_content.extend((amenities, line))
            # Add landlord
            landlord = Paragraph(f"Landlord: {item_object.get('landlord')}", normal_style)
            sub_content.append(landlord)

            # Add maintenance contact
            maintenance_contact = Paragraph(f"Maintenance Contact: {item_object.get('maintenance_contact')}",
                                            normal_style)
            sub_content.append(maintenance_contact)

            # Add built year
            built_year = Paragraph(f"Built Year: {item_object.get('built_year')}", normal_style)
            sub_content.extend((built_year, line))
            # Add parking spots
            parking_spots = Paragraph(f"Parking Spots: {item_object.get('parking_spots')}", normal_style)
            sub_content.extend((parking_spots, line))
                    # Add a new line after each item

    return sub_content

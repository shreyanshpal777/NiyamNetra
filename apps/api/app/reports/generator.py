from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.core.config import get_settings
from app.database.models import InspectionDocument


def _fmt(value, default="-"):
    if value is None or value == "":
        return default
    return value


def generate_inspection_report(inspection: InspectionDocument) -> str:
    settings = get_settings()

    report_dir = settings.report_dir
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{inspection.id}.pdf"

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], fontSize=18, spaceAfter=12
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=13, spaceBefore=12, spaceAfter=6
    )
    small_style = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8)

    elements = []

    # 1. Title
    elements.append(Paragraph("Inspector AI - Compliance Inspection Report", title_style))

    # 2. Metadata
    created = inspection.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    metadata = [
        ["Inspection ID", inspection.id],
        ["Date/Time", created.strftime("%Y-%m-%d %H:%M:%S UTC")],
        ["Product Name", _fmt(inspection.product_name)],
        ["Category", _fmt(inspection.category)],
        ["Final Status", _fmt(inspection.status)],
        ["Compliance Score", _fmt(inspection.score)],
    ]
    meta_table = Table(metadata, colWidths=[50 * mm, 120 * mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(meta_table)

    # 3. Uploaded image
    elements.append(Paragraph("3. Evidence Image", h2_style))
    image_path = inspection.image_path
    if image_path and Path(image_path).exists():
        try:
            img = Image(str(image_path))
            img.drawWidth = 80 * mm
            img.drawHeight = 80 * mm
            img.hAlign = "CENTER"
            elements.append(img)
        except Exception:
            elements.append(Paragraph("(Image could not be embedded)", styles["BodyText"]))
    else:
        elements.append(Paragraph("(No image available for this inspection)", styles["BodyText"]))

    # 4. Extracted product information
    elements.append(Paragraph("4. Extracted Product Information", h2_style))
    pd = inspection.product_data
    product_rows = [
        ["MRP", _fmt(pd.mrp) if pd else "-"],
        ["Net Quantity", (
            f"{_fmt(pd.net_weight_value)} {_fmt(pd.net_weight_unit)}".strip()
            if pd and pd.net_weight_value is not None else "-"
        )],
        ["Manufacturer", _fmt(pd.manufacturer) if pd else "-"],
        ["Batch Number", _fmt(pd.batch_number) if pd else "-"],
        ["Manufacturing Date", _fmt(pd.manufacturing_date) if pd else "-"],
        ["Expiry Date", _fmt(pd.expiry_date) if pd else "-"],
        ["Customer Care", _fmt(pd.customer_care_phone) if pd else "-"],
    ]
    pd_table = Table(product_rows, colWidths=[50 * mm, 120 * mm])
    pd_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(pd_table)

    # 5. OCR and measurement summary
    elements.append(Paragraph("5. OCR and Measurement Summary", h2_style))
    if inspection.ocr_results:
        ocr_data = [["Text", "Confidence", "Height (px)", "Height (mm)"]]
        for word in inspection.ocr_results:
            ocr_data.append([
                word.text,
                f"{word.confidence:.2f}",
                f"{word.height_px:.2f}",
                f"{word.height_mm:.2f}" if word.height_mm is not None else "-",
            ])
        ocr_table = Table(ocr_data, colWidths=[70 * mm, 30 * mm, 30 * mm, 30 * mm])
        ocr_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))
        elements.append(ocr_table)
    else:
        elements.append(Paragraph("(No OCR results)", styles["BodyText"]))

    # 6. Compliance rule results
    elements.append(Paragraph("6. Compliance Rule Results", h2_style))
    if inspection.rule_results:
        rule_data = [["Rule", "Status", "Observed", "Expected", "Explanation", "Evidence"]]
        for rule in inspection.rule_results:
            rule_data.append([
                rule.name,
                rule.status,
                _fmt(rule.observed_value),
                _fmt(rule.expected_value),
                rule.message,
                ", ".join(rule.evidence_ids) if rule.evidence_ids else "-",
            ])
        rule_table = Table(rule_data, colWidths=[30 * mm, 25 * mm, 25 * mm, 25 * mm, 45 * mm, 15 * mm])
        rule_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            # Colour-code status cells
            ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#006400")),
        ]))
        elements.append(rule_table)
    else:
        elements.append(Paragraph("(No rule results)", styles["BodyText"]))

    # 7. Evidence integrity
    elements.append(Paragraph("7. Evidence Integrity", h2_style))
    eh = inspection.evidence_hashes
    integrity_rows = [
        ["Original Image SHA-256", _fmt(eh.original_image_sha256 if eh else None)],
        ["Result JSON SHA-256", _fmt(eh.result_json_sha256 if eh else None)],
        ["Report PDF SHA-256", _fmt(eh.report_pdf_sha256 if eh else None)],
        ["Hash Algorithm", _fmt(inspection.hash_algorithm)],
        ["Hash Timestamp", _fmt(inspection.hashed_at.strftime("%Y-%m-%d %H:%M:%S UTC") if inspection.hashed_at else None)],
    ]
    integrity_table = Table(integrity_rows, colWidths=[60 * mm, 110 * mm])
    integrity_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    elements.append(integrity_table)

    # 8. Disclaimer
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Disclaimer: This report is generated by demo compliance rules and is not legal advice.",
        small_style,
    ))

    doc = SimpleDocTemplate(
        str(report_path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    doc.build(elements)

    return str(report_path)

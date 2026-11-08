import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import pandas as pd

class PDFReportService:
    @staticmethod
    def generate_executive_pdf(kpis: dict, df_purchase: pd.DataFrame, filename: str = "reporte_ejecutivo.pdf") -> str:
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor("#1F4E78"),
            spaceAfter=12
        )

        elements.append(Paragraph("Reporte Ejecutivo de Inventario - Enterprise", title_style))
        elements.append(Paragraph(f"<b>Stock Total Global:</b> {kpis['total_units']:,} unidades", styles['Normal']))
        elements.append(Paragraph(f"<b>Capital Inmovilizado:</b> ${kpis['total_capital']:,.2f}", styles['Normal']))
        elements.append(Paragraph(f"<b>SKUs en Riesgo Crítico:</b> {kpis['critical_skus']}", styles['Normal']))
        elements.append(Spacer(1, 15))

        elements.append(Paragraph("<b>Sugerencias de Compras Prioritarias</b>", styles['Heading2']))
        elements.append(Spacer(1, 8))

        if not df_purchase.empty:
            table_data = [["Producto", "Bodega", "Stock Actual", "Sugerido Comprar"]]
            for _, row in df_purchase.iterrows():
                table_data.append([str(row['product_id']), str(row['warehouse_id']), str(row['quantity']), str(row['Sugerido_Comprar'])])

            t = Table(table_data, colWidths=[200, 100, 100, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F4E78")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F2F2F2")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("No hay órdenes de compra sugeridas en este momento.", styles['Normal']))

        doc.build(elements)
        return filename
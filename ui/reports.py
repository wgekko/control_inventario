# import streamlit as st
# import pandas as pd
# from services.analytics_service import AnalyticsService
# from services.forecasting_service import ForecastingService

# def render_reports_view(df_inv: pd.DataFrame, df_audit: pd.DataFrame):
#     st.subheader("🔮 Reportes Inteligentes y Proyecciones")

#     df_forecast = AnalyticsService.predict_next_month(df_audit)
#     df_purchase = ForecastingService.suggest_purchase_orders(df_inv, df_forecast)

#     st.write("### 🛒 ¿Qué productos debo comprar y en qué cantidad?")
#     if not df_purchase.empty:
#         st.dataframe(df_purchase, width='stretch')
#     else:
#         st.success("El inventario actual satisface completamente la demanda estimada proyectada.")

#     st.markdown("---")
#     st.write("### 📈 Estimación de Demanda Mensual (Proyección 30 Días)")
#     st.dataframe(df_forecast, width='stretch')

import streamlit as st
import pandas as pd
from services.pdf_report_service import PDFReportService
from services.analytics_service import AnalyticsService
from services.forecasting_service import ForecastingService

def render_reports_view(df_inv: pd.DataFrame, df_audit: pd.DataFrame, df_rejected: pd.DataFrame):
    st.subheader("🔮 Reportes Inteligentes, Machine Learning y Exportación")

    df_forecast = AnalyticsService.predict_next_month(df_audit)
    df_purchase = ForecastingService.suggest_purchase_orders(df_inv, df_forecast)

    st.write("### 🛒 Órdenes de Compra Sugeridas (Basado en Proyecciones)")
    if not df_purchase.empty:
        st.dataframe(df_purchase, width='stretch')
        
        # Botón para descargar PDF Ejecutivo
        kpis = AnalyticsService.get_dashboard_kpis(df_inv, df_rejected)
        if st.button(":material/folder_copy: Generar y Descargar Reporte Ejecutivo en PDF"):
            pdf_path = PDFReportService.generate_executive_pdf(kpis, df_purchase)
            with open(pdf_path, "rb") as f:
                st.download_button(":material/download:  Descargar PDF", f, file_name="reporte_ejecutivo_inventario.pdf", mime="application/pdf")
    else:
        st.success("El inventario satisface la demanda estimada.")
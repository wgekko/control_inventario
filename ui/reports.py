# import streamlit as st
# import pandas as pd
# from services.pdf_report_service import PDFReportService
# from services.analytics_service import AnalyticsService
# from services.forecasting_service import ForecastingService

# def render_reports_view(df_inv: pd.DataFrame, df_audit: pd.DataFrame, df_rejected: pd.DataFrame):
#     st.subheader(":maerial/order_approve: Reportes Inteligentes, Machine Learning y Exportación")

#     df_forecast = AnalyticsService.predict_next_month(df_audit)
#     df_purchase = ForecastingService.suggest_purchase_orders(df_inv, df_forecast)

#     st.write("### :material/shopping_cart: Órdenes de Compra Sugeridas y Proyecciones")
#     if not df_purchase.empty:
#         # 1. Muestra los datos y estimaciones numéricas en tabla interactiva
#         st.dataframe(df_purchase, width='stretch')        
#        
#         st.write("### :material/analytics: Gráfico Comparativo: Stock vs Demanda Estimada")
#         if "Demanda Estimada (30 días)" in df_purchase.columns and "Sugerido_Comprar" in df_purchase.columns:
#             chart_df = df_purchase.set_index("product_id")[["quantity", "min_stock", "Demanda Estimada (30 días)", "Sugerido_Comprar"]]
#             st.bar_chart(chart_df)

#         # 3. Botón para exportar a PDF (opcional)
#         kpis = AnalyticsService.get_dashboard_kpis(df_inv, df_rejected)
#         if st.button(":material/picture_as_pdf: Generar y Descargar Reporte Ejecutivo en PDF"):
#             pdf_path = PDFReportService.generate_executive_pdf(kpis, df_purchase)
#             with open(pdf_path, "rb") as f:
#                 st.download_button(":material/download: Descargar PDF", f, file_name="reporte_ejecutivo_inventario.pdf", mime="application/pdf")
#     else:
#         st.success("El inventario satisface la demanda estimada.")


#------------------ version mejorada con graficos -----------------------------        


import streamlit as st
import pandas as pd
from services.pdf_report_service import PDFReportService
from services.analytics_service import AnalyticsService
from services.forecasting_service import ForecastingService

def render_reports_view(df_inv: pd.DataFrame, df_audit: pd.DataFrame, df_rejected: pd.DataFrame):
    st.subheader(":maerial/order_approve: Reportes Inteligentes, Machine Learning y Exportación")

    # Obtener proyecciones, compras sugeridas y KPIs generales
    df_forecast = AnalyticsService.predict_next_month(df_audit)
    df_purchase = ForecastingService.suggest_purchase_orders(df_inv, df_forecast)
    kpis = AnalyticsService.get_dashboard_kpis(df_inv, df_rejected)

    # Verificamos si existen órdenes de compra urgentes
    has_purchases = df_purchase is not None and not df_purchase.empty

    if has_purchases:
        # ==========================================
        # ESCENARIO A: HAY NECESIDAD DE COMPRAS
        # ==========================================
        st.write("### :material/shopping_cart: Órdenes de Compra Sugeridas y Proyecciones")
        st.dataframe(df_purchase, width='stretch')
        
        st.write("### :material/analytics: Gráfico de Análisis y Proyección de Compras")
        try:
            cols_to_plot = [col for col in ["quantity", "min_stock", "Demanda ML Estimada (30 días)", "Sugerido_Comprar"] if col in df_purchase.columns]
            if cols_to_plot and "product_id" in df_purchase.columns:
                chart_data = df_purchase.set_index("product_id")[cols_to_plot]
                st.bar_chart(chart_data)
            else:
                numeric_df = df_purchase.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    st.bar_chart(numeric_df)
        except Exception as e:
            st.info(f"No se pudo renderizar el gráfico interactivo: {e}")

        st.markdown("---")
        if st.button(":material/picture_as_pdf: Generar y Descargar Reporte Ejecutivo en PDF"):
            pdf_path = PDFReportService.generate_executive_pdf(kpis, df_purchase)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=":material/download: Descargar PDF Generado",
                    data=f,
                    file_name="reporte_ejecutivo_inventario.pdf",
                    mime="application/pdf"
                )
    else:
        # ==========================================
        # ESCENARIO B: INVENTARIO SALUDABLE (Enfoque Macro UX)
        # ==========================================
        st.success(":material/check_box: **Inventario Saludable:** El stock actual satisface por completo la demanda estimada a los próximos 30 días. No hay rupturas inminentes ni compras urgentes requeridas.")
        
        st.markdown("---")
        st.subheader(":material/display_settings: Panel de Salud y Cobertura General del Inventario")
        
        # 1. Métricas clave estáticas (KPIs de tranquilidad) en columnas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Cobertura Global", value="100%", delta="Óptima")
        with col2:
            total_capital = kpis.get("total_capital", 0.0)
            st.metric(label="Capital Inmovilizado", value=f"${total_capital:,.2f}")
        with col3:
            total_units = kpis.get("total_units", 0)
            st.metric(label="Unidades Totales en Stock", value=f"{total_units:,}")
        with col4:
            total_skus = len(df_inv) if not df_inv.empty else 0
            st.metric(label="SKUs Activos", value=f"{total_skus}")

        st.markdown("---")
        
        # 2. Gráfico de resumen macro (Comparativa de todo el stock actual frente al stock mínimo/seguridad)
        st.write("### :material/production_quantity_limits: Distribución General: Stock Actual vs. Stock Mínimo por Producto")
        if df_inv is not None and not df_inv.empty:
            try:
                chart_cols = [col for col in ["quantity", "min_stock"] if col in df_inv.columns]
                if chart_cols and "product_id" in df_inv.columns:
                    inv_chart_data = df_inv.set_index("product_id")[chart_cols]
                    st.bar_chart(inv_chart_data)
                else:
                    st.info("No hay suficientes columnas cuantitativas para graficar la distribución general.")
            except Exception as e:
                st.info(f"No se pudo renderizar el gráfico macro: {e}")
        else:
            st.info("No hay registros de inventario disponibles para mostrar.")

        # 3. Opción de descargar un reporte general de salud en PDF
        st.markdown("---")
        if st.button(":material/picture_as_pdf: Generar y Descargar Reporte de Salud General en PDF"):
            empty_purchases = pd.DataFrame(columns=["product_id", "warehouse_id", "quantity", "Sugerido_Comprar"])
            pdf_path = PDFReportService.generate_executive_pdf(kpis, empty_purchases)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=":material/download: Descargar Reporte de Salud en PDF",
                    data=f,
                    file_name="reporte_salud_inventario.pdf",
                    mime="application/pdf"
                )
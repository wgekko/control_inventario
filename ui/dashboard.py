import streamlit as st
import pandas as pd
from services.analytics_service import AnalyticsService

def render_dashboard(df_inv: pd.DataFrame, df_audit: pd.DataFrame, df_rejected: pd.DataFrame):
    st.subheader(":material/dashboard_2_gear: Panel de Indicadores y Salud Logística")

    kpis = AnalyticsService.get_dashboard_kpis(df_inv, df_rejected)
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Stock Total", f"{kpis['total_units']:,} unid.")
    c2.metric("Capital Inmovilizado", f"${kpis['total_capital']:,.2f}")
    c3.metric("Riesgo de Agotamiento", f"{kpis['critical_skus']} SKUs", delta="-Alerta" if kpis['critical_skus'] > 0 else "OK", delta_color="inverse")
    c4.metric("Pérdidas de Venta (Rechazos)", f"{kpis['rejected_count']}", delta="Fallos" if kpis['rejected_count'] > 0 else "Limpio", delta_color="inverse")

    st.markdown("---")
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.write("#### :material/insert_chart: Clasificación de Productos (Análisis ABC por Capital)")
        df_abc = AnalyticsService.run_abc_classification(df_inv)
        st.dataframe(df_abc[["product_id", "warehouse_id", "quantity", "valor_total", "Categoria_ABC"]], width='stretch')

    with col2:
        st.write("#### :material/warning: Stock Crítico por Bodega")
        criticos = df_inv[df_inv["quantity"] <= df_inv["min_stock"]]
        st.dataframe(criticos[["product_id", "warehouse_id", "quantity", "min_stock"]], width='stretch')
import streamlit as st
import pandas as pd
from services.analytics_service import AnalyticsService

def render_alerts_view(df_audit: pd.DataFrame, df_rejected: pd.DataFrame):
    st.subheader(":material/motion_sensor_alert: Detección de Anomalías y Fallos de Negocio")

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### :material/filter_alt: Salidas Inusualmente Grandes (Anomalías)")
        anomalies = AnalyticsService.find_anomalies(df_audit)
        if not anomalies.empty:
            st.dataframe(anomalies, width='stretch')
        else:
            st.info("No se detectaron transacciones anómalas en la ventana analizada.")

    with col2:
        st.write("#### :material/data_info_alert: Demanda Insatisfecha (Rechazos por Stock)")
        st.dataframe(df_rejected, width='stretch')
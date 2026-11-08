import streamlit as st
from database.migration import init_db
from services.inventory_service import InventoryService
from services.movement_service import MovementService
from ui.dashboard import render_dashboard
from ui.inventory import render_inventory_view
from ui.movements import render_movements_view
from ui.reports import render_reports_view
from ui.alerts import render_alerts_view

# Configuración de página
st.set_page_config(page_title="Gestor de Inventario Enterprise", layout="wide")

# Inicialización única de servicios y base de datos
if "inv_service" not in st.session_state:
    init_db()
    inv_service = InventoryService()
    st.session_state.inv_service = inv_service
    st.session_state.mov_service = MovementService(inv_service)

inv_service = st.session_state.inv_service
mov_service = st.session_state.mov_service

# Cargar Datos en Tiempo Real
df_inv = inv_service.get_inventory_df()
df_audit = mov_service.get_audit_logs()
df_rejected = mov_service.get_rejected_logs()

# Navegación en Barra Lateral
st.sidebar.subheader(":material/system_update_alt: Sistema de Inventarios")
option = st.sidebar.radio("Menú Principal", [
    "Dashboard General",
    "Estado de Inventario",
    "Operaciones & Carga",
    "Reportes & Compras",
    "Alertas & Anomalías"
])

# Enrutamiento de Vistas (con los 3 DataFrames requeridos en reportes)
if option == "Dashboard General":
    render_dashboard(df_inv, df_audit, df_rejected)
elif option == "Estado de Inventario":
    render_inventory_view(df_inv)
elif option == "Operaciones & Carga":
    render_movements_view(df_inv, inv_service, mov_service)
elif option == "Reportes & Compras":
    render_reports_view(df_inv, df_audit, df_rejected)
elif option == "Alertas & Anomalías":
    render_alerts_view(df_audit, df_rejected)
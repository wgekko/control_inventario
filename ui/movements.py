# import streamlit as st
# import pandas as pd
# import asyncio

# def render_movements_view(df_inv: pd.DataFrame, inv_service, mov_service, loop):
#     st.subheader("📝 Gestión de Entradas, Salidas y Carga Masiva")
#     tab1, tab2, tab3 = st.tabs(["Formulario Manual", "Carga Masiva (Excel/CSV)", "Prueba de Carga (Stress Test)"])

#     productos = sorted(df_inv["product_id"].unique().tolist())
#     bodegas = sorted(df_inv["warehouse_id"].unique().tolist())

#     with tab1:
#         with st.form("form_manual"):
#             prod = st.selectbox("Producto SKU", productos)
#             wh = st.selectbox("Bodega", bodegas)
#             tipo = st.radio("Operación", ["Entrada", "Salida"])
#             cant = st.number_input("Cantidad", min_value=1, value=1)
#             btn = st.form_submit_button("Enviar Movimiento")

#         if btn:
#             delta = cant if tipo == "Entrada" else -cant
#             loop.run_until_complete(inv_service.add_movement(prod, wh, delta))
#             st.success(f"Movimiento encolado exitosamente: {tipo} {cant} unid.")
#             loop.run_until_complete(asyncio.sleep(0.1))
#             st.rerun()

#     with tab2:
#         file = st.file_uploader("Adjuntar planilla Excel / CSV", type=["xlsx", "csv"])
#         default_wh = st.selectbox("Bodega por defecto", bodegas)
#         if file and st.button("🚀 Procesar Archivo"):
#             df_file = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
#             count = loop.run_until_complete(mov_service.bulk_upload_from_dataframe(df_file, default_wh))
#             st.success(f"Se procesaron {count} registros desde el archivo.")
#             loop.run_until_complete(asyncio.sleep(0.1))
#             st.rerun()

#     with tab3:
#         if st.button("Simular 30 Ventas Simultáneas"):
#             async def run_stress():
#                 tasks = [inv_service.add_movement("Teclado Mecánico RGB", "Bodega SCL", -2) for _ in range(30)]
#                 await asyncio.gather(*tasks)
#             loop.run_until_complete(run_stress())
#             st.success("Ráfaga de 30 ventas ejecutada.")
#             st.rerun()


import streamlit as st
import pandas as pd

def render_movements_view(df_inv: pd.DataFrame, inv_service, mov_service):
    st.subheader(":material/manage_search: Gestión de Entradas, Salidas y Carga Masiva")
    tab1, tab2, tab3 = st.tabs(["Formulario Manual", "Carga Masiva (Excel/CSV)", "Prueba de Carga (Stress Test)"])

    productos = sorted(df_inv["product_id"].unique().tolist())
    bodegas = sorted(df_inv["warehouse_id"].unique().tolist())

    with tab1:
        with st.form("form_manual"):
            prod = st.selectbox("Producto SKU", productos)
            wh = st.selectbox("Bodega", bodegas)
            tipo = st.radio("Operación", ["Entrada", "Salida"])
            cant = st.number_input("Cantidad", min_value=1, value=1)
            btn = st.form_submit_button("Enviar Movimiento")

        if btn:
            delta = cant if tipo == "Entrada" else -cant
            success = inv_service.process_movement(prod, wh, delta)
            if success:
                st.success(f":material/check_circle: Movimiento procesado con éxito: {tipo} {cant} unid.")
            else:
                st.error(":material/close: Movimiento rechazado: Stock insuficiente.")
            st.rerun()

    with tab2:
        file = st.file_uploader("Adjuntar planilla Excel / CSV", type=["xlsx", "csv"])
        default_wh = st.selectbox("Bodega por defecto", bodegas)
        if file and st.button(":material/update: Procesar Archivo"):
            df_file = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
            count = mov_service.bulk_upload_from_dataframe(df_file, default_wh)
            st.success(f"Se procesaron {count} registros desde el archivo.")
            st.rerun()

    with tab3:
        if st.button("Simular 30 Ventas Simultáneas"):
            for _ in range(30):
                inv_service.process_movement("Teclado Mecánico RGB", "Bodega SCL", -2)
            st.success("Ráfaga de 30 ventas ejecutada.")
            st.rerun()
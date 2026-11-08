import streamlit as st
import pandas as pd

def render_inventory_view(df_inv: pd.DataFrame):
    st.subheader(":material/inventory_2: Estado General del Inventario")

    c_search, c_toggle = st.columns([2, 1])
    with c_search:
        search = st.text_input(":material/search: Buscar SKU / Producto:", placeholder="Nombre del producto...")
    with c_toggle:
        only_critical = st.toggle(":material/problem: Mostrar solo críticos")

    df_filtered = df_inv.copy()
    if search:
        df_filtered = df_filtered[df_filtered["product_id"].str.contains(search, case=False, na=False)]
    if only_critical:
        df_filtered = df_filtered[df_filtered["quantity"] <= df_filtered["min_stock"]]

    def highlight_stock(row):
        if row["quantity"] <= row["min_stock"]:
            return ['background-color: #ff4b4b22; color: #ff4b4b; font-weight: bold;'] * len(row)
        return [''] * len(row)

    st.dataframe(df_filtered.style.apply(highlight_stock, axis=1), width='stretch')
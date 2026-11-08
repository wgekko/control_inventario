# import pandas as pd

# class ForecastingService:
#     @staticmethod
#     def suggest_purchase_orders(df_inv: pd.DataFrame, df_forecast: pd.DataFrame) -> pd.DataFrame:
#         """Determina exactamente qué productos comprar y en qué cantidad para cubrir la demanda proyectada."""
#         if df_inv.empty:
#             return pd.DataFrame()

#         merged = pd.merge(df_inv, df_forecast, left_on="product_id", right_on="Producto", how="left")
#         merged["Demanda Estimada (30 días)"] = merged["Demanda Estimada (30 días)"].fillna(0)

#         # Sugerencia de compra: (Stock Mínimo + Demanda Futura) - Stock Actual
#         merged["Sugerido_Comprar"] = (merged["min_stock"] + merged["Demanda Estimada (30 días)"]) - merged["quantity"]
#         merged["Sugerido_Comprar"] = merged["Sugerido_Comprar"].apply(lambda x: max(0, int(x)))

#         to_buy = merged[merged["Sugerido_Comprar"] > 0]
#         return to_buy[["product_id", "warehouse_id", "quantity", "min_stock", "Demanda Estimada (30 días)", "Sugerido_Comprar"]]
import pandas as pd

class ForecastingService:
    @staticmethod
    def suggest_purchase_orders(df_inv: pd.DataFrame, df_forecast: pd.DataFrame) -> pd.DataFrame:
        """Determina exactamente qué productos comprar y en qué cantidad para cubrir la demanda proyectada."""
        if df_inv.empty:
            return pd.DataFrame()

        if df_forecast.empty:
            df_copy = df_inv.copy()
            df_copy["Demanda Estimada (30 días)"] = 0
            df_copy["Sugerido_Comprar"] = (df_copy["min_stock"] - df_copy["quantity"]).apply(lambda x: max(0, int(x)))
            to_buy = df_copy[df_copy["Sugerido_Comprar"] > 0]
            return to_buy[["product_id", "warehouse_id", "quantity", "min_stock", "Demanda Estimada (30 días)", "Sugerido_Comprar"]]

        merged = pd.merge(df_inv, df_forecast, left_on="product_id", right_on="Producto", how="left")
        merged["Demanda Estimada (30 días)"] = merged["Demanda Estimada (30 días)"].fillna(0)

        # Sugerencia de compra: (Stock Mínimo + Demanda Futura) - Stock Actual
        merged["Sugerido_Comprar"] = (merged["min_stock"] + merged["Demanda Estimada (30 días)"]) - merged["quantity"]
        merged["Sugerido_Comprar"] = merged["Sugerido_Comprar"].apply(lambda x: max(0, int(x)))

        to_buy = merged[merged["Sugerido_Comprar"] > 0]
        return to_buy[["product_id", "warehouse_id", "quantity", "min_stock", "Demanda Estimada (30 días)", "Sugerido_Comprar"]]
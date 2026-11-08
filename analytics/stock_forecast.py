# import pandas as pd
# import numpy as np

# class StockForecaster:
#     @staticmethod
#     def forecast_demand(df_audit: pd.DataFrame, window_days: int = 30) -> pd.DataFrame:
#         """Calcula el consumo promedio diario y proyecta la demanda esperada a 30 días."""
#         if df_audit.empty:
#             return pd.DataFrame(columns=["product_id", "daily_avg", "projected_month"])

#         # Filtrar solo salidas (deltas negativos)
#         salidas = df_audit[df_audit["delta"] < 0].copy()
#         salidas["consumed"] = salidas["delta"].abs()

#         grouped = salidas.groupby("product_id")["consumed"].sum().reset_index()
#         grouped["daily_avg"] = np.round(grouped["consumed"] / 7.0, 2) # Basado en ventana de 7 días
#         grouped["projected_month"] = np.round(grouped["daily_avg"] * window_days, 0)

#         return grouped.rename(columns={
#             "product_id": "Producto",
#             "daily_avg": "Consumo Diario Est.",
#             "projected_month": "Demanda Estimada (30 días)"
#         })

import pandas as pd
import numpy as np

class StockForecaster:
    @staticmethod
    def forecast_demand(df_audit: pd.DataFrame, window_days: int = 30) -> pd.DataFrame:
        """Calcula el consumo promedio diario y proyecta la demanda esperada a 30 días."""
        cols = ["Producto", "Consumo Diario Est.", "Demanda Estimada (30 días)"]
        
        if df_audit is None or df_audit.empty:
            return pd.DataFrame(columns=cols)

        # Filtrar solo salidas (deltas negativos)
        salidas = df_audit[df_audit["delta"] < 0].copy()
        if salidas.empty:
            return pd.DataFrame(columns=cols)

        salidas["consumed"] = salidas["delta"].abs()

        grouped = salidas.groupby("product_id")["consumed"].sum().reset_index()
        grouped["daily_avg"] = np.round(grouped["consumed"] / 7.0, 2)
        grouped["projected_month"] = np.round(grouped["daily_avg"] * window_days, 0)

        return grouped.rename(columns={
            "product_id": "Producto",
            "daily_avg": "Consumo Diario Est.",
            "projected_month": "Demanda Estimada (30 días)"
        })[cols]

import numpy as np
import pandas as pd

class InventoryMathEngine:
    @staticmethod
    def calculate_scientific_parameters(df_inv: pd.DataFrame, df_audit: pd.DataFrame, lead_time_days: int = 5, service_factor: float = 1.645) -> pd.DataFrame:
        """Calcula el Stock de Seguridad Estadístico y el Lote Óptimo de Pedido (EOQ)."""
        if df_inv.empty:
            return df_inv

        df = df_inv.copy()
        
        # Calcular desviaciones de demanda si hay auditoría
        if not df_audit.empty:
            salidas = df_audit[df_audit["delta"] < 0].copy()
            salidas["qty"] = salidas["delta"].abs()
            stats = salidas.groupby("product_id")["qty"].agg(["mean", "std"]).reset_index()
            stats["std"] = stats["std"].fillna(0)
            df = pd.merge(df, stats, left_on="product_id", right_on="product_id", how="left").fillna({"mean": 1.0, "std": 0.5})
        else:
            df["mean"] = 1.0
            df["std"] = 0.5

        # Stock de Seguridad = Z * sqrt(Lead Time) * Desviación estándar diaria
        df["Stock_Seguridad_Optimo"] = np.ceil(service_factor * np.sqrt(lead_time_days) * df["std"])
        
        # Punto de Reorden = (Demanda Diaria * Lead Time) + Stock de Seguridad
        df["Punto_Reorden"] = np.ceil((df["mean"] * lead_time_days) + df["Stock_Seguridad_Optimo"])

        return df
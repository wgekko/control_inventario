import pandas as pd

class AnomalyDetector:
    @staticmethod
    def detect_unusual_movements(df_audit: pd.DataFrame, threshold_std: float = 2.0) -> pd.DataFrame:
        """Detecta retiros de stock anómalos o inusualmente grandes usando puntuación Z (Z-Score)."""
        if df_audit.empty or len(df_audit) < 5:
            return pd.DataFrame()

        df = df_audit[df_audit["delta"] < 0].copy()
        df["magnitude"] = df["delta"].abs()

        mean = df["magnitude"].mean()
        std = df["magnitude"].std()

        if std == 0 or pd.isna(std):
            return pd.DataFrame()

        df["z_score"] = (df["magnitude"] - mean) / std
        anomalies = df[df["z_score"] >= threshold_std]
        return anomalies[["id", "product_id", "warehouse_id", "delta", "timestamp", "z_score"]]
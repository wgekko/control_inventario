import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class KMeansSegmentation:
    @staticmethod
    def cluster_inventory(df_inv: pd.DataFrame, df_audit: pd.DataFrame) -> pd.DataFrame:
        """Agrupa los SKUs usando K-Means considerando valor, frecuencia y volumen."""
        if df_inv.empty:
            return df_inv

        df = df_inv.copy()
        df["valor_total"] = df["quantity"] * df["unit_cost"]

        # Calcular frecuencia y volumen de salidas si existe auditoría
        if not df_audit.empty:
            salidas = df_audit[df_audit["delta"] < 0].copy()
            salidas["qty"] = salidas["delta"].abs()
            freq = salidas.groupby("product_id").agg(
                frecuencia=("id", "count"),
                volumen_salidas=("qty", "sum")
            ).reset_index()
            df = pd.merge(df, freq, left_on="product_id", right_on="product_id", how="left").fillna(0)
        else:
            df["frecuencia"] = 0
            df["volumen_salidas"] = 0

        features = df[["valor_total", "frecuencia", "volumen_salidas"]]
        
        # Normalizar datos para K-Means
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Aplicar K-Means (3 clústeres: Estratégicos/Alta Prioridad, Operativos, De Baja Rotación)
        kmeans = KMeans(n_clusters=min(3, len(df)), random_state=42, n_init=10)
        df["Cluster_Segmento"] = kmeans.fit_predict(scaled_features)

        cluster_labels = {
            0: "Cluster B (Operativos Estándar)",
            1: "Cluster A (Alta Rotación / Críticos)",
            2: "Cluster C (Baja Rotación / Obsolescencia)"
        }
        df["Segmento_Logistico"] = df["Cluster_Segmento"].map(cluster_labels).fillna("Cluster Estándar")
        return df
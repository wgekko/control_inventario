import pandas as pd

class ABCAnalysis:
    @staticmethod
    def classify(df_inv: pd.DataFrame) -> pd.DataFrame:
        """Clasificación ABC basada en la inversión de capital inmovilizado."""
        if df_inv.empty:
            return df_inv

        df = df_inv.copy()
        df["valor_total"] = df["quantity"] * df["unit_cost"]
        df = df.sort_values(by="valor_total", ascending=False)

        total_val = df["valor_total"].sum()
        if total_val == 0:
            df["Categoria_ABC"] = "C"
            return df

        df["cum_val"] = df["valor_total"].cumsum()
        df["cum_perc"] = (df["cum_val"] / total_val) * 100

        def assign_abc(perc):
            if perc <= 80:
                return "A (Alto Valor)"
            elif perc <= 95:
                return "B (Valor Medio)"
            return "C (Bajo Valor)"

        df["Categoria_ABC"] = df["cum_perc"].apply(assign_abc)
        return df.drop(columns=["cum_val", "cum_perc"])
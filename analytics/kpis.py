import pandas as pd

class KPICalculator:
    @staticmethod
    def calculate_summary(df_inv: pd.DataFrame, df_rejected: pd.DataFrame):
        if df_inv.empty:
            return {
                "total_units": 0,
                "total_capital": 0.0,
                "critical_skus": 0,
                "rejected_count": 0
            }

        df_inv["capital"] = df_inv["quantity"] * df_inv["unit_cost"]
        total_units = int(df_inv["quantity"].sum())
        total_capital = float(df_inv["capital"].sum())
        critical_skus = int((df_inv["quantity"] <= df_inv["min_stock"]).sum())
        rejected_count = len(df_rejected) if not df_rejected.empty else 0

        return {
            "total_units": total_units,
            "total_capital": total_capital,
            "critical_skus": critical_skus,
            "rejected_count": rejected_count
        }
import pandas as pd
from analytics.kpis import KPICalculator
from analytics.abc_analytics import ABCAnalysis
from analytics.stock_forecast import StockForecaster
from analytics.anomaly_detection import AnomalyDetector

class AnalyticsService:
    @staticmethod
    def get_dashboard_kpis(df_inv: pd.DataFrame, df_rejected: pd.DataFrame):
        return KPICalculator.calculate_summary(df_inv, df_rejected)

    @staticmethod
    def run_abc_classification(df_inv: pd.DataFrame):
        return ABCAnalysis.classify(df_inv)

    @staticmethod
    def predict_next_month(df_audit: pd.DataFrame):
        return StockForecaster.forecast_demand(df_audit)

    @staticmethod
    def find_anomalies(df_audit: pd.DataFrame):
        return AnomalyDetector.detect_unusual_movements(df_audit)
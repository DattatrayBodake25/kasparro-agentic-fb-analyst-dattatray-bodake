import pandas as pd
from datetime import datetime


class DataAgent:
    """
    Loads and summarizes Facebook Ads performance data.
    Produces structured summaries for other agents to use.
    """

    def __init__(self, config):
        self.config = config
        self.data_path = config["paths"]["data"]
        self.low_ctr_threshold = config["thresholds"]["low_ctr"]
        self.roas_drop_pct = config["thresholds"]["roas_drop_pct"]

    def load_data(self):
        """Load the CSV dataset safely."""
        try:
            df = pd.read_csv(self.data_path)
            print(f"Dataset loaded successfully: {len(df)} rows, {len(df.columns)} columns.")
            return df
        except FileNotFoundError:
            print(f"Error: Data file not found at path '{self.data_path}'.")
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
        except Exception as e:
            print(f"Unexpected error while loading dataset: {e}")
        return pd.DataFrame()

    def summarize_metrics(self, df: pd.DataFrame):
        """Summarize key metrics and trends from the dataset."""
        try:
            numeric_cols = ["spend", "impressions", "clicks", "ctr", "purchases", "revenue", "roas"]
            summary = df[numeric_cols].describe().to_dict()

            # Convert date column to datetime for trend analysis
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # ROAS trend over time (simple start/end comparison)
            roas_trend = (
                df.groupby("date")["roas"]
                .mean()
                .reset_index()
                .sort_values("date", ascending=True)
            )

            if not roas_trend.empty:
                trend_info = {
                    "start_roas": float(roas_trend["roas"].iloc[0]),
                    "end_roas": float(roas_trend["roas"].iloc[-1]),
                    "trend_direction": (
                        "decline" if roas_trend["roas"].iloc[-1] < roas_trend["roas"].iloc[0] else "growth"
                    ),
                }
            else:
                trend_info = {"start_roas": None, "end_roas": None, "trend_direction": "unknown"}

            # Identify low CTR campaigns (underperformers)
            low_ctr_df = df[df["ctr"] < self.low_ctr_threshold]
            low_ctr_summary = {
                "count": len(low_ctr_df["campaign_name"].unique()),
                "avg_ctr": round(low_ctr_df["ctr"].mean(), 4) if not low_ctr_df.empty else None,
                "avg_roas": round(low_ctr_df["roas"].mean(), 4) if not low_ctr_df.empty else None,
                "sample_campaigns": (
                    low_ctr_df["campaign_name"].dropna().unique()[:5].tolist()
                    if not low_ctr_df.empty else []
                ),
            }

            # Final combined summary
            summary_json = {
                "dataset_rows": len(df),
                "overall_summary": summary,
                "roas_trend": trend_info,
                "low_ctr_summary": low_ctr_summary,
                "timestamp": datetime.now().isoformat(),
            }
            return summary_json

        except KeyError as e:
            print(f"Missing expected column in dataset: {e}")
        except Exception as e:
            print(f"Error summarizing metrics: {e}")
        return {}

    def run(self):
        """Main execution method for data loading and summarization."""
        df = self.load_data()
        if df.empty:
            print("DataAgent terminated: No valid data to process.")
            return {}

        summary = self.summarize_metrics(df)
        if not summary:
            print("DataAgent completed with no summary generated.")
            return {}

        # Basic summary logs (student-style, short)
        print("Data summary generated successfully.")
        print(f" - Total rows: {summary['dataset_rows']}")
        print(f" - ROAS trend: {summary['roas_trend']['trend_direction']}")
        print(f" - Low CTR campaigns: {summary['low_ctr_summary']['count']}")
        return summary
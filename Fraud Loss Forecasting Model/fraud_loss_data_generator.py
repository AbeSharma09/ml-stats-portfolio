"""Synthetic fraud-loss data generator for Q1 2026.

Creates a panel-style dataset with real-world style features such as:
- product/channel/region/segment/device
- transaction volume and ticket size
- login and OTP failures
- chargebacks, new accounts, active customers
- holiday / payday / control change flags
- fraud cases and fraud loss

Output:
    q1_2026_synthetic_fraud_losses.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def _sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1 / (1 + np.exp(-x))


def generate_synthetic_fraud_data(
    start_date: str = "2026-01-01",
    end_date: str = "2026-03-31",
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    dates = pd.date_range(start_date, end_date, freq="D")

    products = ["credit_card", "debit_card", "digital_wallet"]
    channels = ["mobile_app", "web", "branch"]
    regions = ["north", "south", "east", "west"]
    segments = ["retail", "premium"]
    device_types = ["ios", "android", "desktop"]

    # Structural multipliers that create realistic differences across segments.
    product_txn_mult = {"credit_card": 1.20, "debit_card": 1.00, "digital_wallet": 0.82}
    channel_txn_mult = {"mobile_app": 1.30, "web": 1.10, "branch": 0.45}
    region_txn_mult = {"north": 1.00, "south": 0.94, "east": 0.98, "west": 1.05}
    segment_txn_mult = {"retail": 1.00, "premium": 0.68}
    device_txn_mult = {"ios": 1.04, "android": 1.10, "desktop": 0.72}

    product_risk = {"credit_card": 1.15, "debit_card": 0.90, "digital_wallet": 1.30}
    channel_risk = {"mobile_app": 1.20, "web": 1.05, "branch": 0.75}
    region_risk = {"north": 1.00, "south": 1.08, "east": 0.96, "west": 1.12}
    segment_risk = {"retail": 1.00, "premium": 0.72}
    device_risk = {"ios": 0.95, "android": 1.08, "desktop": 0.80}

    holiday_dates = {
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-01-26"),
        pd.Timestamp("2026-03-08"),
    }

    rows = []
    for d in dates:
        dow = d.dayofweek
        weekend = int(dow >= 5)
        month = d.month
        day = d.day
        month_end = int(d.is_month_end)
        payday = int(day in {1, 15, 30, 31})
        holiday_flag = int(d in holiday_dates)

        # Time-varying market / business patterns.
        growth_trend = 1.0 + 0.0025 * (d - dates[0]).days
        weekend_volume = 0.88 if weekend else 1.00
        holiday_volume = 0.82 if holiday_flag else 1.00
        month_end_volume = 1.06 if month_end else 1.00
        payday_volume = 1.12 if payday else 1.00

        for product in products:
            for channel in channels:
                for region in regions:
                    for segment in segments:
                        # Device mix depends on channel to look realistic.
                        if channel == "branch":
                            device = "desktop"
                        elif channel == "mobile_app":
                            device = rng.choice(["ios", "android"], p=[0.46, 0.54])
                        else:
                            device = rng.choice(device_types, p=[0.20, 0.18, 0.62])

                        base_txn = 2200
                        struct_txn = (
                            base_txn
                            * product_txn_mult[product]
                            * channel_txn_mult[channel]
                            * region_txn_mult[region]
                            * segment_txn_mult[segment]
                            * device_txn_mult[device]
                            * growth_trend
                            * weekend_volume
                            * holiday_volume
                            * month_end_volume
                            * payday_volume
                        )

                        promo_exposure = int(
                            (channel in {"mobile_app", "web"})
                            and (month == 2 or (month == 3 and day <= 10))
                        )
                        control_change_flag = int(month == 3 and day >= 12 and channel != "branch")
                        campaign_flag = int(month == 2 and channel in {"mobile_app", "web"} and segment == "retail")
                        seasonality = 1.0 + 0.08 * np.sin(2 * np.pi * (d.dayofyear / 30.0))
                        noise = rng.normal(1.0, 0.08)
                        txn_count = max(
                            50,
                            int(
                                rng.poisson(
                                    lam=max(25, struct_txn * seasonality * noise)
                                )
                            ),
                        )

                        avg_txn_value = float(
                            np.clip(
                                rng.lognormal(mean=4.1 if product != "credit_card" else 4.25, sigma=0.35),
                                12,
                                450,
                            )
                        )

                        active_customers = max(
                            100,
                            int(txn_count / rng.uniform(1.5, 3.4) + rng.normal(0, 12))
                        )
                        new_accounts = max(
                            0,
                            int(
                                rng.poisson(
                                    lam=18
                                    * product_txn_mult[product]
                                    * (1.15 if channel == "mobile_app" else 0.85)
                                    * (1.35 if segment == "retail" else 0.7)
                                    * (1.3 if month == 2 else 1.0)
                                )
                            ),
                        )

                        login_failures = max(
                            0,
                            int(
                                rng.poisson(
                                    lam=14
                                    * channel_risk[channel]
                                    * (1.25 if channel == "mobile_app" else 0.95)
                                    * (1.1 if weekend else 1.0)
                                    * (1.18 if campaign_flag else 1.0)
                                )
                            ),
                        )

                        otp_failures = max(
                            0,
                            int(
                                rng.poisson(
                                    lam=7
                                    * channel_risk[channel]
                                    * (1.2 if channel == "mobile_app" else 0.9)
                                    * (1.1 if holiday_flag else 1.0)
                                )
                            ),
                        )

                        chargeback_count = max(
                            0,
                            int(
                                rng.poisson(
                                    lam=max(
                                        0.1,
                                        2.0
                                        * product_risk[product]
                                        * channel_risk[channel]
                                        * region_risk[region]
                                        * segment_risk[segment]
                                        * (1.3 if control_change_flag else 1.0)
                                    )
                                )
                            ),
                        )

                        # Latent fraud propensity that links operational signals to outcomes.
                        raw_risk = (
                            0.9
                            + 0.25 * np.log1p(login_failures)
                            + 0.18 * np.log1p(otp_failures)
                            + 0.12 * np.log1p(chargeback_count + 1)
                            + 0.11 * np.log1p(new_accounts + 1)
                            + 0.10 * promo_exposure
                            + 0.13 * control_change_flag
                            + 0.07 * campaign_flag
                            + 0.08 * weekend
                            + 0.05 * holiday_flag
                            + 0.06 * (product == "digital_wallet")
                            + 0.05 * (channel == "mobile_app")
                            + 0.04 * (region in {"south", "west"})
                            + 0.06 * (segment == "retail")
                        )

                        risk_multiplier = (
                            0.65
                            + 0.50 * _sigmoid(raw_risk - 1.4)
                            + rng.normal(0, 0.03)
                        )
                        risk_multiplier = float(np.clip(risk_multiplier, 0.35, 1.55))

                        fraud_rate = float(
                            np.clip(
                                0.00055
                                * product_risk[product]
                                * channel_risk[channel]
                                * region_risk[region]
                                * segment_risk[segment]
                                * risk_multiplier,
                                0.00008,
                                0.006,
                            )
                        )

                        fraud_cases = max(
                            0,
                            int(rng.poisson(lam=max(0.05, txn_count * fraud_rate))),
                        )

                        severity = (
                            avg_txn_value
                            * (1.20 if product == "credit_card" else 1.0)
                            * (1.08 if channel == "web" else 1.0)
                            * (1.05 if control_change_flag else 1.0)
                        )
                        fraud_loss = float(
                            max(
                                0.0,
                                fraud_cases * severity * rng.uniform(0.72, 1.35)
                                + rng.normal(0, 35),
                            )
                        )

                        fraud_alerts = int(
                            max(
                                0,
                                round(
                                    fraud_cases
                                    * rng.uniform(1.7, 4.2)
                                    + login_failures * rng.uniform(0.15, 0.65)
                                ),
                            )
                        )

                        dispute_rate = float(np.clip(0.0012 + 0.00015 * chargeback_count + rng.normal(0, 0.0002), 0, 0.02))
                        manual_review_rate = float(np.clip(0.02 + 0.01 * control_change_flag + rng.normal(0, 0.004), 0.005, 0.08))
                        approval_rate = float(np.clip(0.86 - 0.015 * control_change_flag - 0.008 * weekend + rng.normal(0, 0.01), 0.55, 0.98))
                        decline_rate = float(np.clip(1.0 - approval_rate, 0.01, 0.45))
                        device_risk_score = float(
                            np.clip(
                                0.25
                                + 0.18 * (device == "android")
                                + 0.10 * (channel == "mobile_app")
                                + 0.08 * promo_exposure
                                + rng.normal(0, 0.03),
                                0.05,
                                0.95,
                            )
                        )

                        rows.append(
                            {
                                "date": d,
                                "month": d.month,
                                "day": d.day,
                                "day_of_week": dow,
                                "week_of_year": int(d.isocalendar().week),
                                "weekend_flag": weekend,
                                "month_end_flag": month_end,
                                "payday_flag": payday,
                                "holiday_flag": holiday_flag,
                                "product": product,
                                "channel": channel,
                                "region": region,
                                "customer_segment": segment,
                                "device_type": device,
                                "promo_exposure_flag": promo_exposure,
                                "campaign_flag": campaign_flag,
                                "control_change_flag": control_change_flag,
                                "transaction_count": txn_count,
                                "avg_txn_value": round(avg_txn_value, 2),
                                "active_customers": active_customers,
                                "new_accounts": new_accounts,
                                "login_failures": login_failures,
                                "otp_failures": otp_failures,
                                "chargeback_count": chargeback_count,
                                "fraud_alerts": fraud_alerts,
                                "manual_review_rate": round(manual_review_rate, 4),
                                "approval_rate": round(approval_rate, 4),
                                "decline_rate": round(decline_rate, 4),
                                "device_risk_score": round(device_risk_score, 4),
                                "fraud_rate": round(fraud_rate, 6),
                                "fraud_cases": fraud_cases,
                                "fraud_loss": round(fraud_loss, 2),
                            }
                        )

    df = pd.DataFrame(rows).sort_values(["date", "product", "channel", "region", "customer_segment"]).reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic fraud-loss data for Q1 2026.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("q1_2026_synthetic_fraud_losses.csv"),
        help="Output CSV path",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    df = generate_synthetic_fraud_data(seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Saved {len(df):,} rows to {args.output}")


if __name__ == "__main__":
    main()


# Data Dictionary – Fraud Loss Forecasting Dataset

## Column Definitions

| Column Name | Definition |
|---|---|
| date | Daily observation date |
| transaction_volume | Total transactions processed |
| active_customers | Number of active customers |
| digital_usage_rate | Percentage of customers using digital channels |
| fraudulent_transactions | Total fraudulent transactions detected |
| fraud_rate | Percentage of fraudulent transactions |
| avg_fraud_amount | Average fraud amount per incident |
| total_fraud_loss | Total fraud loss amount |
| chargeback_volume | Number of chargebacks |
| account_takeover_cases | Number of account takeover fraud cases |
| operational_risk_score | Internal operational risk severity score |
| fraud_control_effectiveness | Fraud prevention effectiveness score |
| marketing_campaign_flag | Indicates marketing campaign activity |
| holiday_flag | Indicates holiday/high-traffic periods |
| emerging_attack_flag | Indicates new fraud attack patterns |
| recovery_rate | Percentage of recovered fraud losses |
| customer_growth_rate | Daily customer growth percentage |
| avg_transaction_value | Average transaction value |
| high_risk_geo_transactions | Transactions from high-risk geographies |
| fraud_investigation_backlog | Pending fraud investigations |
| false_positive_rate | Legitimate transactions flagged as fraud |
| merchant_risk_index | Merchant exposure risk score |
| stress_scenario_multiplier | Multiplier for stressed fraud environment |

---

## Target Variable

### total_fraud_loss

This is the primary forecasting target used in the notebook.

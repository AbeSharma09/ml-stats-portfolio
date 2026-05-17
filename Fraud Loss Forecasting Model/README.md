
# Fraud Loss Forecasting Engine – Q1 2026

## Project Overview

This project demonstrates an end-to-end fraud loss forecasting framework for a banking / financial services environment using both statistical and machine learning techniques.

The project simulates realistic fraud-loss data for Q1 2026 and applies multiple forecasting approaches commonly used in banking risk and fraud analytics environments.

---

## Project Components

### 1. Synthetic Data Generator
File:
`fraud_loss_data_generator.py`

Purpose:
- Generates realistic synthetic fraud-risk data
- Simulates operational and business drivers
- Creates daily fraud-loss observations for Q1 2026
- Exports data to CSV

Generated Output:
`q1_2026_synthetic_fraud_losses.csv`

---

### 2. Forecasting Notebook
File:
`fraud_loss_forecasting_demo.ipynb`

Purpose:
- Performs exploratory data analysis
- Builds multiple forecasting models
- Compares model performance
- Evaluates forecasting accuracy

Models Included:
- Naive Forecasting
- Moving Average
- Exponential Smoothing
- SARIMAX
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Evaluation Metrics:
- MAE
- RMSE
- MAPE

---

## Business Problem Statement

Fraud losses directly impact financial institutions through:
- operational losses
- customer dissatisfaction
- regulatory concerns
- reserve requirements

The objective is to forecast future fraud losses using historical trends and operational drivers.

---

## Skills Demonstrated

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- Time Series Forecasting
- Risk Analytics
- Fraud Analytics
- Business Forecasting
- Data Visualization

---

## Folder Structure

project/
├── fraud_loss_data_generator.py
├── q1_2026_synthetic_fraud_losses.csv
├── fraud_loss_forecasting_demo.ipynb
├── README.md
└── data_dictionary.md

---

## Disclaimer

This project uses fully synthetic data generated for educational and demonstration purposes only.

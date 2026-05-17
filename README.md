# ml-stats-portfolio
A curated portfolio of machine learning models and statistical analyses solving real-world data problems.

## Projects

- Customer Cashflow Intelligence & Balance Forecasting Engine: end-to-end pipeline for forecasting customer balances. Includes a data generator, a notebook pipeline, SHAP explainability plots, and example artifacts. See [Customer Cashflow Intelligence & Balance Forecasting Engine](Customer%20Cashflow%20Intelligence%20%26%20Balance%20Forecasting%20Engine).
- Fraud Loss Forecasting Model: synthetic data generator, demo notebook, data dictionary, and evaluation artifacts for forecasting fraud-related losses. See [Fraud Loss Forecasting Model](Fraud%20Loss%20Forecasting%20Model).

## Quick Start

1. Create and activate a Python environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell on Windows
pip install -r requirements.txt  # create this file if it doesn't exist
```

2. Run notebooks (Jupyter/Lab):

```bash
pip install jupyterlab
jupyter lab
```

3. Run example data generators or demos:

```bash
python "Customer Cashflow Intelligence & Balance Forecasting Engine/data generator.py"
python "Fraud Loss Forecasting Model/fraud_loss_data_generator.py"
```

## Notes

- Each project folder contains notebooks and scripts demonstrating the pipeline and evaluation.
- Add a `requirements.txt` for reproducible environments; consider using `pip freeze > requirements.txt` after installing dependencies.

## Next Steps

- Add `requirements.txt` and small README files inside each project folder describing how to run their notebooks.

## Contact

If you have questions or want help adding `requirements.txt`, open an issue or reply here.

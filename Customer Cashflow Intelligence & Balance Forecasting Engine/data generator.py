import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# Parameters
n_customers = 5000
n_months = 24

# Persona distribution
persona_options = ["stable", "overspender", "saver", "debt_heavy", "volatile"]
persona_probs = [0.3, 0.2, 0.2, 0.15, 0.15]

rows = []

for cust_id in range(1, n_customers + 1):

    # Assign persona
    persona = np.random.choice(persona_options, p=persona_probs)

    # Base attributes
    base_salary = np.random.randint(30000, 150000)
    balance = np.random.randint(5000, 50000)

    # Persona-based behavior
    if persona == "stable":
        expense_ratio = np.random.uniform(0.5, 0.7)
        emi = np.random.randint(2000, 8000)

    elif persona == "overspender":
        expense_ratio = np.random.uniform(0.8, 1.1)
        emi = np.random.randint(3000, 10000)

    elif persona == "saver":
        expense_ratio = np.random.uniform(0.3, 0.5)
        emi = np.random.randint(0, 5000)

    elif persona == "debt_heavy":
        expense_ratio = np.random.uniform(0.6, 0.8)
        emi = np.random.randint(10000, 25000)

    else:  # volatile
        expense_ratio = np.random.uniform(0.4, 0.9)
        emi = np.random.randint(0, 15000)

    for month in range(1, n_months + 1):

        # Salary growth (yearly hike)
        salary = base_salary * (1 + 0.05 * (month // 12))
        salary *= np.random.uniform(0.95, 1.05)

        # Income shock (only for volatile users)
        if persona == "volatile" and np.random.rand() < 0.15:
            salary *= np.random.uniform(0.5, 0.8)

        # Other credits (refunds, transfers)
        other_credit = np.random.uniform(0, 5000)

        total_credit = salary + other_credit

        # Expenses
        expenses = total_credit * expense_ratio

        # Festival spike (Oct–Nov effect)
        if month % 12 in [10, 11]:
            expenses *= np.random.uniform(1.2, 1.6)

        # Random emergency spike
        if np.random.rand() < 0.1:
            expenses *= np.random.uniform(1.3, 1.8)

        # Total debit includes EMI
        total_debit = expenses + emi

        # Update balance
        balance = balance + total_credit - total_debit

        # Store row
        rows.append([
            cust_id,
            persona,
            month,
            round(salary, 2),
            round(other_credit, 2),
            round(total_credit, 2),
            round(total_debit, 2),
            emi,
            round(balance, 2)
        ])

# Create DataFrame
df = pd.DataFrame(rows, columns=[
    "customer_id",
    "persona",
    "month",
    "salary",
    "other_credit",
    "total_credit",
    "total_debit",
    "emi",
    "balance"
])

# Save CSV
df.to_csv("balance_forecasting_persona.csv", index=False)

print("CSV created successfully ✅")
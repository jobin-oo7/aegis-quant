import pulp
from typing import List, Dict, Any

def optimize_security_investments(
    controls: List[Dict[str, Any]],
    budget_inr: float
) -> Dict[str, Any]:
    """
    Solves the 0-1 Knapsack problem for cyber security control selection.
    
    controls: List of dicts, each containing:
      - 'id': str
      - 'name': str
      - 'cost_inr': float
      - 'risk_reduction_inr': float (delta ALE derived from FAIR)
    budget_inr: Maximum expenditure approved by CFO
    """
    if budget_inr <= 0 or not controls:
        return {
            "selected_controls": [],
            "total_spent_inr": 0.0,
            "total_risk_reduced_inr": 0.0,
            "rosi_percentage": 0.0,
            "remaining_budget_inr": max(budget_inr, 0.0)
        }

    # 1. Initialize Integer Linear Programming (ILP) Problem
    prob = pulp.LpProblem("Cyber_Investment_Optimization", pulp.LpMaximize)

    # 2. Define Binary Decision Variables: x[i] = 1 if control is selected, 0 otherwise
    control_vars = {
        c["id"]: pulp.LpVariable(f"control_{c['id']}", cat=pulp.LpBinary)
        for c in controls
    }

    # 3. Objective Function: Maximize total financial risk reduction (Delta ALE)
    prob += pulp.lpSum([
        c["risk_reduction_inr"] * control_vars[c["id"]]
        for c in controls
    ]), "Total_Risk_Reduction"

    # 4. Constraint: Total cost must not exceed the budget ceiling
    prob += pulp.lpSum([
        c["cost_inr"] * control_vars[c["id"]]
        for c in controls
    ]) <= budget_inr, "Budget_Constraint"

    # 5. Solve using the bundled Coin-OR CBC solver (silent mode)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # 6. Extract Selected Controls and Compile Financial Metrics
    selected = []
    total_spent = 0.0
    total_risk_reduced = 0.0

    for c in controls:
        if pulp.value(control_vars[c["id"]]) == 1.0:
            selected.append(c)
            total_spent += c["cost_inr"]
            total_risk_reduced += c["risk_reduction_inr"]

    # Calculate Return on Security Investment (RoSI)
    # RoSI = ((Risk Reduced - Cost of Controls) / Cost of Controls) * 100
    rosi = 0.0
    if total_spent > 0:
        rosi = ((total_risk_reduced - total_spent) / total_spent) * 100.0

    return {
        "selected_controls": selected,
        "total_spent_inr": round(total_spent, 2),
        "total_risk_reduced_inr": round(total_risk_reduced, 2),
        "rosi_percentage": round(rosi, 2),
        "remaining_budget_inr": round(budget_inr - total_spent, 2)
    }

if __name__ == "__main__":
    # Test Scenario: CFO approves ₹12,00,000 budget.
    # Security team proposes 6 candidate defense controls:
    candidate_controls = [
        {"id": "ctrl_1", "name": "Deploy Phishing-Resistant MFA", "cost_inr": 200000.0, "risk_reduction_inr": 850000.0},
        {"id": "ctrl_2", "name": "Endpoint Detection & Response (EDR)", "cost_inr": 500000.0, "risk_reduction_inr": 1800000.0},
        {"id": "ctrl_3", "name": "Cloud Security Posture Management (CSPM)", "cost_inr": 400000.0, "risk_reduction_inr": 1200000.0},
        {"id": "ctrl_4", "name": "Database Column-level Encryption (DPDP)", "cost_inr": 350000.0, "risk_reduction_inr": 1400000.0},
        {"id": "ctrl_5", "name": "External Red Team Assessment", "cost_inr": 600000.0, "risk_reduction_inr": 900000.0},
        {"id": "ctrl_6", "name": "Privileged Access Management (PAM)", "cost_inr": 300000.0, "risk_reduction_inr": 1100000.0},
    ]

    cfo_budget = 1200000.0  # ₹12 Lakhs

    print(f"--- Running AegisQuant Knapsack Optimizer ---")
    print(f"Total Available Budget: ₹{cfo_budget:,}")
    print(f"Evaluating {len(candidate_controls)} candidate controls...\n")

    solution = optimize_security_investments(candidate_controls, cfo_budget)

    print("Recommended Controls to Deploy:")
    for ctrl in solution["selected_controls"]:
        print(f"  [+] {ctrl['name']}: Cost ₹{ctrl['cost_inr']:,} -> Risk Reduced ₹{ctrl['risk_reduction_inr']:,}")

    print("\nFinancial Summary:")
    print(f"Total Capital Deployed: ₹{solution['total_spent_inr']:,}")
    print(f"Total Risk Averted:     ₹{solution['total_risk_reduced_inr']:,}")
    print(f"Unspent Budget:         ₹{solution['remaining_budget_inr']:,}")
    print(f"Calculated RoSI:        {solution['rosi_percentage']}%")
    print("--- Optimization Complete ---")
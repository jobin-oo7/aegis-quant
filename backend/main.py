from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Asset, Vulnerability, Control
from schemas import AssetResponse, ControlResponse, OptimizeRequest, OptimizeResponse
from core.optimizer import optimize_security_investments
from core.fair_engine import simulate_fair_risk

app = FastAPI(
    title="AegisQuant API",
    description="Cyber Risk Quantification & Investment Optimization Platform (SIH26105)",
    version="1.0.0"
)

# Enable CORS for Next.js development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {"status": "online", "system": "AegisQuant Core Engine"}

@app.get("/api/v1/assets", response_model=List[AssetResponse])
def get_all_assets(db: Session = Depends(get_db)):
    """Retrieve all monitored assets along with mapped vulnerabilities."""
    return db.query(Asset).all()

@app.get("/api/v1/controls", response_model=List[ControlResponse])
def get_all_controls(db: Session = Depends(get_db)):
    """Retrieve candidate security controls with cost and risk reduction ratings."""
    return db.query(Control).all()

@app.post("/api/v1/optimize", response_model=OptimizeResponse)
def run_budget_optimization(payload: OptimizeRequest, db: Session = Depends(get_db)):
    """
    Executes 0-1 Knapsack Integer Linear Programming to find the optimal
    bundle of controls that maximizes risk reduction under the given budget constraint.
    """
    if payload.budget_inr < 0:
        raise HTTPException(status_code=400, detail="Budget cannot be negative.")

    controls = db.query(Control).all()
    if not controls:
        raise HTTPException(status_code=404, detail="No controls found in database.")

    # Prepare data payload for core optimizer
    controls_data = [
        {
            "id": c.id,
            "name": c.name,
            "cost_inr": c.cost_inr,
            "risk_reduction_inr": c.risk_reduction_inr
        }
        for c in controls
    ]

    result = optimize_security_investments(controls_data, payload.budget_inr)

    return {
        "budget_inr": payload.budget_inr,
        "total_spent_inr": result["total_spent_inr"],
        "total_risk_reduced_inr": result["total_risk_reduced_inr"],
        "remaining_budget_inr": result["remaining_budget_inr"],
        "rosi_percentage": result["rosi_percentage"],
        "selected_controls": result["selected_controls"]
    }
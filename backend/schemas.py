from pydantic import BaseModel
from typing import List, Optional

# Vulnerability Schemas
class VulnerabilityResponse(BaseModel):
    id: int
    cve_id: str
    description: Optional[str]
    cvss_score: float
    epss_probability: float
    remediation_status: str

    class Config:
        from_attributes = True

# Asset Schemas
class AssetResponse(BaseModel):
    id: int
    name: str
    criticality_tier: str
    hourly_downtime_cost_inr: float
    in_dpdp_scope: bool
    vulnerabilities: List[VulnerabilityResponse] = []

    class Config:
        from_attributes = True

# Control Schemas
class ControlResponse(BaseModel):
    id: int
    name: str
    category: str
    cost_inr: float
    risk_reduction_inr: float
    is_active: bool

    class Config:
        from_attributes = True

# Optimization Request & Response Schemas
class OptimizeRequest(BaseModel):
    budget_inr: float

class SelectedControl(BaseModel):
    id: int
    name: str
    cost_inr: float
    risk_reduction_inr: float

class OptimizeResponse(BaseModel):
    budget_inr: float
    total_spent_inr: float
    total_risk_reduced_inr: float
    remaining_budget_inr: float
    rosi_percentage: float
    selected_controls: List[SelectedControl]
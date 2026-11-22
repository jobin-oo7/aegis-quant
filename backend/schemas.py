from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class VulnerabilityResponse(BaseModel):
    id: int
    cve_id: str
    cvss_score: float
    description: Optional[str] = "No description available"
    epss_probability: Optional[float] = 0.0
    remediation_status: Optional[str] = "OPEN"
    asset_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class AssetResponse(BaseModel):
    id: int
    name: str
    criticality_tier: Optional[str] = "Tier 2"
    hourly_downtime_cost_inr: Optional[float] = 0.0
    in_dpdp_scope: Optional[bool] = False
    vulnerabilities: List[VulnerabilityResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ControlResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = "General"
    cost_inr: float
    risk_reduction_inr: float
    framework_mapping: str
    is_active: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class OptimizeRequest(BaseModel):
    budget_inr: float

class SelectedControl(BaseModel):
    id: int
    name: str
    cost_inr: float
    risk_reduction_inr: float
    framework_mapping: str

    model_config = ConfigDict(from_attributes=True)

class OptimizeResponse(BaseModel):
    budget_inr: float
    total_spent_inr: float
    total_risk_reduced_inr: float
    remaining_budget_inr: float
    rosi_percentage: float
    selected_controls: List[SelectedControl]
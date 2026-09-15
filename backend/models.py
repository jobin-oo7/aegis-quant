from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=True)
    criticality = Column(String(20), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    hourly_downtime_cost_inr = Column(Float, nullable=False, default=100000.0)
    in_dpdp_scope = Column(Boolean, default=True)      # Indian DPDP compliance trigger
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    vulnerabilities = relationship("Vulnerability", back_populates="asset", cascade="all, delete-orphan")
    simulations = relationship("SimulationRun", back_populates="asset", cascade="all, delete-orphan")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    cve_id = Column(String(50), nullable=False)        # e.g., CVE-2023-44487
    title = Column(String(255), nullable=False)
    cvss_score = Column(Float, nullable=False)         # Technical severity (0.0 - 10.0)
    epss_score = Column(Float, default=0.01)           # Exploit likelihood (0.0 - 1.0)
    is_mitigated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    asset = relationship("Asset", back_populates="vulnerabilities")

class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)  # e.g., CTRL_MFA
    name = Column(String(255), nullable=False)
    cost_inr = Column(Float, nullable=False)
    risk_reduction_inr = Column(Float, nullable=False)     # Expected financial loss averted
    category = Column(String(50), default="PREVENTION")    # PREVENTION, DETECTION, RECOVERY

class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    annualized_loss_expectancy_inr = Column(Float, nullable=False)
    var_95_inr = Column(Float, nullable=False)
    var_99_inr = Column(Float, nullable=False)
    iterations = Column(Integer, default=10000)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    asset = relationship("Asset", back_populates="simulations")
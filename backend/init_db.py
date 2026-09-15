from database import engine, Base, SessionLocal
from models import Asset, Vulnerability, Control, SimulationRun

def init_and_seed():
    print("Creating all tables in PostgreSQL...")
    Base.metadata.drop_all(bind=engine)  # Fresh start for clean migrations
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    db = SessionLocal()
    try:
        # 1. Seed Assets
        payment_db = Asset(
            name="Production Payment Gateway DB",
            ip_address="10.0.1.15",
            criticality="CRITICAL",
            hourly_downtime_cost_inr=500000.0,
            in_dpdp_scope=True
        )
        hr_portal = Asset(
            name="Internal Employee HR Portal",
            ip_address="10.0.2.80",
            criticality="MEDIUM",
            hourly_downtime_cost_inr=50000.0,
            in_dpdp_scope=True
        )
        db.add_all([payment_db, hr_portal])
        db.commit()
        db.refresh(payment_db)
        db.refresh(hr_portal)

        # 2. Seed Vulnerabilities
        vulns = [
            Vulnerability(
                asset_id=payment_db.id,
                cve_id="CVE-2023-38606",
                title="Kernel Remote Code Execution via RPC Interface",
                cvss_score=9.8,
                epss_score=0.82
            ),
            Vulnerability(
                asset_id=payment_db.id,
                cve_id="CVE-2023-44487",
                title="HTTP/2 Rapid Reset Denial of Service",
                cvss_score=7.5,
                epss_score=0.67
            ),
            Vulnerability(
                asset_id=hr_portal.id,
                cve_id="CVE-2024-21626",
                title="Container Escape File Descriptor Leak",
                cvss_score=8.6,
                epss_score=0.35
            ),
        ]
        db.add_all(vulns)

        # 3. Seed Security Controls for the Optimizer
        controls = [
            Control(
                code="CTRL_MFA",
                name="Hardware Token Phishing-Resistant MFA",
                cost_inr=200000.0,
                risk_reduction_inr=850000.0,
                category="PREVENTION"
            ),
            Control(
                code="CTRL_EDR",
                name="Real-time Endpoint Detection & Response (EDR)",
                cost_inr=500000.0,
                risk_reduction_inr=1800000.0,
                category="DETECTION"
            ),
            Control(
                code="CTRL_ENC",
                name="Database Field-Level Encryption & Key Vault",
                cost_inr=350000.0,
                risk_reduction_inr=1400000.0,
                category="PREVENTION"
            ),
            Control(
                code="CTRL_CSPM",
                name="Cloud Security Posture Management & Drift Remediation",
                cost_inr=400000.0,
                risk_reduction_inr=1200000.0,
                category="PREVENTION"
            ),
            Control(
                code="CTRL_AUDIT",
                name="External Third-Party Red Team Penetration Test",
                cost_inr=600000.0,
                risk_reduction_inr=900000.0,
                category="DETECTION"
            ),
        ]
        db.add_all(controls)
        db.commit()

        print(f"Database seeded successfully with {len(vulns)} vulnerabilities and {len(controls)} controls.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_and_seed()
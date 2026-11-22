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
        # 3. Seed Candidate Security Controls (with SIH required framework mappings)
        controls = [
            Control(
                name="Deploy Phishing-Resistant MFA",
                category="Identity",
                cost_inr=200000.0,
                risk_reduction_inr=850000.0,
                framework_mapping="NIST: PR.AA-1 | RBI: AC-02 | SEBI: IA-02"
            ),
            Control(
                name="Endpoint Detection & Response (EDR)",
                category="Endpoint",
                cost_inr=500000.0,
                risk_reduction_inr=1800000.0,
                framework_mapping="NIST: DE.CM-1 | RBI: IR-04 | SEBI: IR-04"
            ),
            Control(
                name="Cloud Security Posture Management",
                category="Cloud",
                cost_inr=400000.0,
                risk_reduction_inr=1200000.0,
                framework_mapping="NIST: PR.IP-1 | RBI: CA-03 | SEBI: CM-02"
            ),
            Control(
                name="Database Column-Level Encryption",
                category="Data",
                cost_inr=350000.0,
                risk_reduction_inr=1400000.0,
                framework_mapping="NIST: PR.DS-1 | RBI: MP-04 | DPDP Act Sec. 8"
            ),
            Control(
                name="Privileged Access Management (PAM)",
                category="Identity",
                cost_inr=300000.0,
                risk_reduction_inr=110000.0,
                framework_mapping="NIST: PR.AC-4 | RBI: AC-06 | SEBI: AC-06"
            ),
            Control(
                name="Automated Patching Pipeline",
                category="Infrastructure",
                cost_inr=150000.0,
                risk_reduction_inr=600000.0,
                framework_mapping="NIST: PR.IP-12 | RBI: CM-02 | SEBI: CM-02"
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
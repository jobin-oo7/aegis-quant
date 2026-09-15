import numpy as np
from scipy import stats

def simulate_fair_risk(
    threat_event_freq_min: float,
    threat_event_freq_mode: float,
    threat_event_freq_max: float,
    vulnerability_prob: float,
    loss_magnitude_min_inr: float,
    loss_magnitude_mode_inr: float,
    loss_magnitude_max_inr: float,
    iterations: int = 10000
) -> dict:
    """
    Executes a Monte Carlo simulation using the Open FAIR model ontology.
    
    - Threat Event Frequency (TEF): Modeled via Beta-PERT distribution.
    - Loss Event Frequency (LEF): TEF * Vulnerability (Exploit probability).
    - Loss Magnitude (LM): Modeled via Lognormal distribution (financial loss).
    """
    # 1. PERT Distribution parameters for Threat Event Frequency (TEF)
    # PERT uses Min, Mode, Max to model real-world expert uncertainty
    a, m, b = threat_event_freq_min, threat_event_freq_mode, threat_event_freq_max
    alpha = 1 + 4 * ((m - a) / (b - a)) if b != a else 1
    beta = 1 + 4 * ((b - m) / (b - a)) if b != a else 1
    
    # Generate TEF samples (how many times per year an adversary attacks)
    tef_samples = a + (b - a) * np.random.beta(alpha, beta, iterations)
    
    # 2. Derive Loss Event Frequency (LEF)
    # LEF = TEF * Vulnerability (the probability that the defense fails)
    lef_samples = tef_samples * vulnerability_prob
    
    # 3. Model Loss Magnitude (LM) in INR
    # Financial losses are right-skewed; we fit a lognormal distribution to min and max
    # Assume min is ~10th percentile and max is ~90th percentile
    log_min = np.log(max(loss_magnitude_min_inr, 1))
    log_max = np.log(max(loss_magnitude_max_inr, 1))
    mu = (log_min + log_max) / 2
    sigma = (log_max - log_min) / 3.29  # ~90% confidence spread
    
    lm_samples = np.random.lognormal(mean=mu, sigma=sigma, size=iterations)
    
    # 4. Total Annual Loss Vector
    annual_loss = lef_samples * lm_samples
    
    # 5. Core Actuarial Metrics
    ale = float(np.mean(annual_loss))
    var_95 = float(np.percentile(annual_loss, 95))
    var_99 = float(np.percentile(annual_loss, 99))
    
    return {
        "ale_inr": round(ale, 2),
        "var_95_inr": round(var_95, 2),
        "var_99_inr": round(var_99, 2),
        "iterations": iterations
    }

if __name__ == "__main__":
    # Test Scenario: Critical Payment Gateway Database (DPDP Act Scope)
    # Attacked between 2 to 12 times a year, most likely 5 times.
    # Vulnerability likelihood = 0.40 (40% chance of successful exploit without patch).
    # Loss Magnitude: Min ₹5,00,000 | Likely ₹25,00,000 | Max ₹1,00,00,000 (Statutory + downtime).
    
    print("--- Running AegisQuant FAIR Engine Test ---")
    results = simulate_fair_risk(
        threat_event_freq_min=2.0,
        threat_event_freq_mode=5.0,
        threat_event_freq_max=12.0,
        vulnerability_prob=0.40,
        loss_magnitude_min_inr=500000.0,
        loss_magnitude_mode_inr=2500000.0,
        loss_magnitude_max_inr=10000000.0,
        iterations=10000
    )
    
    print(f"Annualized Loss Expectancy (ALE): ₹{results['ale_inr']:,}")
    print(f"Value at Risk (95% Confidence):   ₹{results['var_95_inr']:,}")
    print(f"Extreme Loss (99% Confidence):   ₹{results['var_99_inr']:,}")
    print("--- Simulation Complete ---")
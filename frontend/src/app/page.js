"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { 
  ShieldCheck, 
  TrendingUp, 
  IndianRupee, 
  CheckCircle2, 
  Layers,
  ArrowDownRight,
  Server,
  AlertOctagon,
  ShieldAlert,
  Activity,
  FileText
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function AegisQuantPlatform() {
  // Navigation State: 'cfo' (Boardroom) or 'ciso' (SecOps Telemetry)
  const [activeTab, setActiveTab] = useState("cfo");

  // CFO State
  const [budget, setBudget] = useState(1000000); // ₹10 Lakhs default
  const [optimization, setOptimization] = useState({
    budget_inr: 1000000,
    total_spent_inr: 0,
    total_risk_reduced_inr: 0,
    remaining_budget_inr: 0,
    rosi_percentage: 0,
    selected_controls: []
  });

  // CISO State
  const [assets, setAssets] = useState([]);
  const [loadingAssets, setLoadingAssets] = useState(false);

  const BASELINE_VAR_INR = 5800000; // Baseline: ₹58 Lakhs

  // Fetch Optimization
  const fetchOptimization = async (currentBudget) => {
    try {
      const res = await axios.post("http://localhost:8000/api/v1/optimize", {
        budget_inr: Number(currentBudget)
      });
      setOptimization(res.data);
    } catch (err) {
      console.error("Backend optimizer failed:", err);
    }
  };

  // Fetch Asset & Vulnerability Telemetry
  const fetchAssets = async () => {
    try {
      setLoadingAssets(true);
      const res = await axios.get("http://localhost:8000/api/v1/assets");
      setAssets(res.data);
    } catch (err) {
      console.error("Failed to load telemetry:", err);
    } finally {
      setLoadingAssets(false);
    }
  };

  useEffect(() => {
    fetchOptimization(budget);
    fetchAssets();
  }, [budget]);

  const residualRisk = Math.max(0, BASELINE_VAR_INR - optimization.total_risk_reduced_inr);

  const chartData = [
    { loss: "₹10L", baseline: 92, residual: Math.max(10, 92 - (optimization.total_risk_reduced_inr / BASELINE_VAR_INR) * 80) },
    { loss: "₹25L", baseline: 75, residual: Math.max(8, 75 - (optimization.total_risk_reduced_inr / BASELINE_VAR_INR) * 70) },
    { loss: "₹50L", baseline: 45, residual: Math.max(5, 45 - (optimization.total_risk_reduced_inr / BASELINE_VAR_INR) * 42) },
    { loss: "₹1Cr+", baseline: 20, residual: Math.max(2, 20 - (optimization.total_risk_reduced_inr / BASELINE_VAR_INR) * 19) }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6 md:p-10">
      {/* Platform Header with Viewport Switcher */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center pb-6 border-b border-slate-800 gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <span className="p-2 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
            </span>
            <h1 className="text-2xl font-black tracking-tight text-white">AegisQuant</h1>
            <span className="text-xs font-mono uppercase bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2 py-0.5 rounded">
              SIH26105
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Continuous Cyber Risk Quantification & Capital Optimization Platform
          </p>
        </div>

        {/* Dual-Persona View Switcher */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab("cfo")}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === "cfo"
                ? "bg-indigo-600 text-white shadow-lg"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" />
            <span>CFO Boardroom</span>
          </button>
          <button
            onClick={() => setActiveTab("ciso")}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === "ciso"
                ? "bg-indigo-600 text-white shadow-lg"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Server className="w-3.5 h-3.5" />
            <span>CISO Attack Surface</span>
          </button>
        </div>
      </header>

      {/* VIEWPORT 1: CFO BOARDROOM VIEW */}
      {activeTab === "cfo" && (
        <div className="animate-in fade-in duration-300">
          {/* Hero Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl shadow-lg">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Baseline Enterprise VaR
              </span>
              <div className="text-2xl font-bold text-red-400 mt-2">
                ₹{BASELINE_VAR_INR.toLocaleString("en-IN")}
              </div>
              <span className="text-xs text-slate-500 mt-1 block">Unmitigated Exposure (95% CI)</span>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl shadow-lg">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Optimized Residual Risk
              </span>
              <div className="text-2xl font-bold text-emerald-400 mt-2 flex items-center">
                ₹{Math.round(residualRisk).toLocaleString("en-IN")}
                <ArrowDownRight className="w-5 h-5 ml-1 text-emerald-400" />
              </div>
              <span className="text-xs text-emerald-500/80 mt-1 block">
                -₹{optimization.total_risk_reduced_inr.toLocaleString("en-IN")} Averted
              </span>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl shadow-lg">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Capital Deployed
              </span>
              <div className="text-2xl font-bold text-indigo-400 mt-2">
                ₹{optimization.total_spent_inr.toLocaleString("en-IN")}
              </div>
              <span className="text-xs text-slate-500 mt-1 block">
                Unspent: ₹{optimization.remaining_budget_inr.toLocaleString("en-IN")}
              </span>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl shadow-lg">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Projected RoSI
              </span>
              <div className="text-2xl font-bold text-amber-400 mt-2 flex items-center">
                {optimization.rosi_percentage}%
                <TrendingUp className="w-5 h-5 ml-2 text-amber-400" />
              </div>
              <span className="text-xs text-slate-500 mt-1 block">Return on Security Investment</span>
            </div>
          </div>

          {/* Budget Allocation Studio */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
            <div className="lg:col-span-1 space-y-6">
              {/* Slider Card */}
              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm font-bold text-white flex items-center">
                    <IndianRupee className="w-4 h-4 mr-1 text-indigo-400" />
                    Approved Security Budget
                  </span>
                  <span className="text-lg font-mono font-bold text-indigo-300">
                    ₹{Number(budget).toLocaleString("en-IN")}
                  </span>
                </div>

                <input
                  type="range"
                  min="0"
                  max="2000000"
                  step="50000"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                />

                <div className="flex justify-between text-[11px] font-mono text-slate-500 mt-2">
                  <span>₹0</span>
                  <span>₹10L</span>
                  <span>₹20L</span>
                </div>

                <p className="text-xs text-slate-400 mt-4 leading-relaxed">
                  Drag the slider to test board allocations. The Knapsack ILP engine evaluates trade-offs in real time.
                </p>
              </div>

              {/* Prescribed Controls */}
              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl">
                <span className="text-sm font-bold text-white flex items-center mb-4">
                  <Layers className="w-4 h-4 mr-2 text-emerald-400" />
                  Prescribed Control Allocations ({optimization.selected_controls.length})
                </span>

                {optimization.selected_controls.length === 0 ? (
                  <div className="text-center py-8 text-slate-500 text-xs">
                    Budget insufficient to fund any defensive controls.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {optimization.selected_controls.map((ctrl) => (
                      <div
                        key={ctrl.id}
                        className="p-3 bg-slate-950 border border-slate-800/80 rounded-lg flex justify-between items-center"
                      >
                        <div>
                          <div className="text-xs font-semibold text-slate-200 flex items-center">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 mr-1.5 flex-shrink-0" />
                            {ctrl.name}
                          </div>
                          <span className="text-[10px] text-slate-500 ml-5 block mt-0.5">
                            Mitigates ₹{ctrl.risk_reduction_inr.toLocaleString("en-IN")} exposure
                          </span>
                        </div>
                        <span className="text-xs font-mono font-bold text-slate-300">
                          ₹{ctrl.cost_inr.toLocaleString("en-IN")}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Recharts Exceedance Curve */}
            <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <h2 className="text-base font-bold text-white">Loss Exceedance Probability Curve</h2>
                  <span className="text-[11px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                    FAIR Actuarial Model
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-6">
                  Probability (%) of annual financial loss exceeding threshold amounts under current mitigation posture.
                </p>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="baselineGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="residualGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.5} />
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="loss" stroke="#64748b" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 12 }} unit="%" />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                    />
                    <Area
                      type="monotone"
                      dataKey="baseline"
                      name="Unmitigated Risk"
                      stroke="#ef4444"
                      strokeWidth={2}
                      fillOpacity={1}
                      fill="url(#baselineGrad)"
                    />
                    <Area
                      type="monotone"
                      dataKey="residual"
                      name="Residual Risk (Optimized)"
                      stroke="#10b981"
                      strokeWidth={2}
                      fillOpacity={1}
                      fill="url(#residualGrad)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="flex items-center justify-end space-x-6 pt-4 border-t border-slate-800 text-xs">
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-0.5 bg-red-500 inline-block"></span>
                  <span className="text-slate-400">Baseline Exposure</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-0.5 bg-emerald-500 inline-block"></span>
                  <span className="text-slate-300 font-semibold">Post-Optimization Posture</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEWPORT 2: CISO ATTACK SURFACE & TELEMETRY VIEW */}
      {activeTab === "ciso" && (
        <div className="mt-8 space-y-6 animate-in fade-in duration-300">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center">
                <Server className="w-5 h-5 mr-2 text-indigo-400" />
                Monitored Enterprise Infrastructure & Vulnerabilities
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Real-time mapping of technical telemetry enriched with Exploit Prediction Scoring System (EPSS) probabilities.
              </p>
            </div>
            <span className="text-xs font-mono bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-slate-300 flex items-center">
              <Activity className="w-3.5 h-3.5 mr-1.5 text-emerald-400" />
              {assets.length} Core Nodes Audited
            </span>
          </div>

          {/* Assets Grid */}
          <div className="grid grid-cols-1 gap-4">
            {assets.map((asset) => (
              <div 
                key={asset.id} 
                className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                  <div className="flex items-center space-x-3">
                    <span className="font-bold text-sm text-white">{asset.name}</span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                      asset.criticality_tier === "Tier 1"
                        ? "bg-red-500/10 text-red-400 border-red-500/20"
                        : "bg-slate-800 text-slate-300 border-slate-700"
                    }`}>
                      {asset.criticality_tier}
                    </span>
                    {asset.in_dpdp_scope && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center">
                        <FileText className="w-2.5 h-2.5 mr-1" />
                        DPDP Scope (Statutory Fines)
                      </span>
                    )}
                  </div>
                  <div className="text-xs font-mono text-slate-400">
                    Downtime Cost: <span className="text-slate-200 font-semibold">₹{asset.hourly_downtime_cost_inr.toLocaleString("en-IN")}/hr</span>
                  </div>
                </div>

                {/* Mapped CVEs Table */}
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="text-slate-500 border-b border-slate-800/50">
                        <th className="pb-2 font-medium">CVE Identifier</th>
                        <th className="pb-2 font-medium">Description</th>
                        <th className="pb-2 font-medium">Technical Severity (CVSS)</th>
                        <th className="pb-2 font-medium">Weaponization Prob. (EPSS)</th>
                        <th className="pb-2 font-medium">Remediation Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/40">
                      {asset.vulnerabilities.map((vuln) => (
                        <tr key={vuln.id} className="text-slate-300">
                          <td className="py-2.5 font-mono font-bold text-indigo-400">
                            {vuln.cve_id}
                          </td>
                          <td className="py-2.5 text-slate-400 max-w-xs truncate">
                            {vuln.description}
                          </td>
                          <td className="py-2.5">
                            <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold ${
                              vuln.cvss_score >= 9.0 
                                ? "bg-red-500/20 text-red-400" 
                                : vuln.cvss_score >= 7.0 
                                ? "bg-amber-500/20 text-amber-400" 
                                : "bg-slate-800 text-slate-400"
                            }`}>
                              {vuln.cvss_score} Critical
                            </span>
                          </td>
                          <td className="py-2.5 font-mono">
                            <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                              vuln.epss_probability >= 0.70
                                ? "bg-red-500/20 text-red-300 border border-red-500/30 animate-pulse"
                                : "bg-slate-800 text-slate-400"
                            }`}>
                              {(vuln.epss_probability * 100).toFixed(1)}% Likelihood
                            </span>
                          </td>
                          <td className="py-2.5 font-mono">
                            <span className="text-[10px] text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded">
                              {vuln.remediation_status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
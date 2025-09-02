import React, { useState } from 'react'

export type Model = 'gbm' | 'bootstrap' | 'startup_costs' | 'credit_risk'

export default function ConfigPanel({ onRun }: { onRun: (config: any) => void }) {
  const [model, setModel] = useState<Model>('gbm')
  const [trials, setTrials] = useState(20000)
  const [horizon, setHorizon] = useState(252)
  const [confidence, setConfidence] = useState(0.95)
  const [mu, setMu] = useState(0.08)
  const [sigma, setSigma] = useState(0.2)

  return (
    <div className="grid gap-3 md:grid-cols-2">
      <label className="flex items-center gap-2">Model
        <select value={model} onChange={e=>setModel(e.target.value as Model)} className="border p-2 rounded">
          <option value="gbm">Stock (GBM)</option>
          <option value="bootstrap">Stock (Bootstrap)</option>
          <option value="startup_costs">Startup Costs</option>
          <option value="credit_risk">Credit Risk</option>
        </select>
      </label>
      <label className="flex items-center gap-2">Trials
        <input type="number" value={trials} onChange={e=>setTrials(+e.target.value)} className="border p-2 rounded w-28" />
      </label>
      <label className="flex items-center gap-2">Horizon (days)
        <input type="number" value={horizon} onChange={e=>setHorizon(+e.target.value)} className="border p-2 rounded w-28" />
      </label>
      <label className="flex items-center gap-2">Confidence
        <input type="number" step="0.01" value={confidence} onChange={e=>setConfidence(+e.target.value)} className="border p-2 rounded w-28" />
      </label>
      {model==='gbm' && (
        <>
          <label className="flex items-center gap-2">mu (annual)
            <input type="number" step="0.01" value={mu} onChange={e=>setMu(+e.target.value)} className="border p-2 rounded w-28" />
          </label>
          <label className="flex items-center gap-2">sigma (annual)
            <input type="number" step="0.01" value={sigma} onChange={e=>setSigma(+e.target.value)} className="border p-2 rounded w-28" />
          </label>
        </>
      )}
      <button onClick={() => onRun({ model, trials, horizon_days: horizon, confidence, mu, sigma })} className="col-span-full bg-black text-white rounded px-4 py-2">Run Simulation</button>
    </div>
  )
}

import React, { useState } from 'react'
import Upload from './components/Upload'
import ConfigPanel from './components/ConfigPanel'
import Results from './components/Results'
import { useStore } from './store'

export default function App() {
  const { apiURL, loading, setLoading, result, setResult } = useStore()
  const [prices, setPrices] = useState<number[] | null>(null)

  async function run(config: any) {
    setLoading(true)
    try {
      const body: any = { ...config }
      if ((config.model === 'gbm' || config.model === 'bootstrap') && prices?.length) {
        body.prices = prices
        body.start_price = prices[prices.length-1]
      }
      const r = await fetch(`${apiURL}/simulate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      const json = await r.json()
      setResult(json)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6 grid gap-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Risk Analysis Dashboard</h1>
        <span className="text-sm text-gray-500">API: {apiURL}</span>
      </header>

      <section className="grid gap-3">
        <h2 className="font-semibold">1) Upload CSV (optional for stock models)</h2>
        <Upload onData={setPrices} />
        {prices && <div className="text-xs text-gray-500">Loaded {prices.length} rows.</div>}
      </section>

      <section className="grid gap-3">
        <h2 className="font-semibold">2) Configure & Run</h2>
        <ConfigPanel onRun={run} />
        {loading && <div className="text-blue-600">Running simulations…</div>}
      </section>

      <section className="grid gap-3">
        <h2 className="font-semibold">3) Results</h2>
        <Results res={result} />
      </section>
    </div>
  )
}

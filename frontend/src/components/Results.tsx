import React from 'react'
import { DistChart, FanChart } from './Charts'

export default function Results({ res }: { res: any | null }) {
  if (!res) return <div className="text-gray-500">No results yet</div>
  const model = res.model

  if (model === 'gbm' || model === 'bootstrap') {
    return (
      <div className="grid gap-4">
        <div className="text-sm">VaR: {res.metrics?.VaR?.toFixed?.(2)} | ES: {res.metrics?.ES?.toFixed?.(2)}</div>
        <FanChart paths={res.paths_sample}/>
        <DistChart data={res.pnl} var95={res.metrics?.VaR} es95={res.metrics?.ES} />
      </div>
    )
  }

  if (model === 'startup_costs') {
    return (
      <div className="grid gap-4">
        <div className="text-sm">Terminal Cost — VaR: {res.metrics?.VaR?.toFixed?.(2)} | ES: {res.metrics?.ES?.toFixed?.(2)}</div>
        <FanChart paths={res.cum_paths_sample}/>
        <DistChart data={res.terminal} var95={res.metrics?.VaR} es95={res.metrics?.ES} />
      </div>
    )
  }

  if (model === 'credit_risk') {
    return (
      <div className="grid gap-4">
        <div className="text-sm">Portfolio Loss — VaR: {res.metrics?.VaR?.toFixed?.(2)} | ES: {res.metrics?.ES?.toFixed?.(2)}</div>
        <DistChart data={res.portfolio_loss} var95={res.metrics?.VaR} es95={res.metrics?.ES} />
      </div>
    )
  }

  return <div>Unknown model</div>
}

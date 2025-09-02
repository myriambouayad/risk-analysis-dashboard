import React from 'react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid } from 'recharts'

export function DistChart({ data, var95, es95 }: { data: number[], var95?: number, es95?: number }) {
  const hist = histogram(data, 50)
  return (
    <div className="h-64 border rounded p-2">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={hist.map(([x,y])=>({x,y}))} margin={{ left: 10, right: 10, top: 10, bottom: 10 }}>
          <XAxis dataKey="x"/>
          <YAxis/>
          <Tooltip/>
          <Area type="monotone" dataKey="y" fillOpacity={0.3}/>
        </AreaChart>
      </ResponsiveContainer>
      {var95 !== undefined && (
        <div className="text-sm mt-2">VaR: {var95.toFixed(2)} | ES: {es95?.toFixed(2)}</div>
      )}
    </div>
  )
}

export function FanChart({ paths }: { paths: number[][] }) {
  const subset = paths.slice(0, 20)
  const series = subset.map((row) => row.map((y, t) => ({ t, y })))

  return (
    <div className="h-64 border rounded p-2">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="t" type="number" allowDecimals={false} domain={[0, subset[0]?.length ?? 0]} />
          <YAxis />
          <Tooltip />
          {series.map((s, i) => (
            <Line key={i} data={s} dataKey="y" dot={false} strokeWidth={1} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

function histogram(arr: number[], bins: number): [number, number][] {
  if (!arr.length) return []
  const min = Math.min(...arr)
  const max = Math.max(...arr)
  const width = (max - min) / bins || 1
  const counts = new Array(bins).fill(0)
  for (const v of arr) {
    let idx = Math.floor((v - min) / width)
    if (idx >= bins) idx = bins - 1
    counts[idx]++
  }
  return counts.map((c, i) => [Number((min + i*width).toFixed(2)), c])
}

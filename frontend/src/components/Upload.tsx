import React, { useRef } from 'react'

type Props = { onData: (arr: number[]) => void }

export default function Upload({ onData }: Props) {
  const ref = useRef<HTMLInputElement | null>(null)
  return (
    <div className="flex items-center gap-2">
      <input ref={ref} type="file" accept=".csv" className="border p-2 rounded" onChange={async (e) => {
        const file = e.target.files?.[0]
        if (!file) return
        const text = await file.text()
        const lines = text.trim().split(/\r?\n/)
        const values: number[] = []
        for (let i=0;i<lines.length;i++) {
          const first = lines[i].split(',')[0].trim()
          const x = Number(first)
          if (!Number.isFinite(x)) continue
          values.push(x)
        }
        onData(values)
      }} />
      <button className="px-3 py-2 rounded bg-gray-100" onClick={() => ref.current?.click()}>Upload CSV</button>
    </div>
  )
}

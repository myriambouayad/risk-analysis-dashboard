import { create } from 'zustand'

type State = {
  apiURL: string,
  loading: boolean,
  result: any | null,
  setURL: (u: string) => void,
  setLoading: (b: boolean) => void,
  setResult: (r: any) => void,
}

export const useStore = create<State>((set) => ({
  apiURL: (import.meta as any).env.VITE_API_URL || 'http://localhost:8000',
  loading: false,
  result: null,
  setURL: (apiURL) => set({ apiURL }),
  setLoading: (loading) => set({ loading }),
  setResult: (result) => set({ result }),
}))

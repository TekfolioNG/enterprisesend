// Every call carries the signed-in user's token. The server decides the client (tenant) from it.
export const useApi = () => {
  const { $auth } = useNuxtApp()
  const base = useRuntimeConfig().public.apiBase

  async function call(path: string, opts: any = {}) {
    const token = await ($auth as any).currentUser?.getIdToken()
    return fetch(`${base}${path}`, {
      ...opts,
      headers: { ...(opts.headers || {}), Authorization: `Bearer ${token}` }
    })
  }
  return { call }
}

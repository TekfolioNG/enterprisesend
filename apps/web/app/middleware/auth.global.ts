import { multiFactor } from 'firebase/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return
  const { $authReady, $auth } = useNuxtApp()
  await $authReady
  const user = useState<any>('user')
  if (!user.value && to.path !== '/login') return navigateTo('/login')
  if (user.value && to.path === '/login') return navigateTo('/')

  const required = useRuntimeConfig().public.requireMfa === 'true'
  const current = ($auth as any).currentUser
  if (user.value && required && to.path !== '/security' && current && multiFactor(current).enrolledFactors.length === 0) {
    return navigateTo('/security')
  }
})

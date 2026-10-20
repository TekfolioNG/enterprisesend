export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return
  const { $authReady } = useNuxtApp()
  await $authReady
  const user = useState<any>('user')
  if (!user.value && to.path !== '/login') return navigateTo('/login')
  if (user.value && to.path === '/login') return navigateTo('/')
})

import { useUserStore } from "~/store/user"

export default defineNuxtRouteMiddleware((to, from) => {
    const aviailableRoutes = ['/user/login', '/user/terms']
    if (aviailableRoutes.includes(to.path)) {
        return
    }
    
    const userStore = useUserStore()
    if (! userStore.logined) {
        return navigateTo('/user/login')
    }
})
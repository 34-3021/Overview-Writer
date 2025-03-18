import { defineStore } from "pinia"

export const useUserStore = defineStore('user', () => {
    const access_token = ref("")
    const refresh_token = ref("")
    const username = ref("")
    const logined = computed(() => access_token.value != "" && refresh_token.value != "")

    function login(access: string, refresh: string) {
        if (access == "" || refresh == "") {
            return false;
        }
        access_token.value = access;
        refresh_token.value = refresh;
        return true;
    }

    function logout() {
        access_token.value = ""
        refresh_token.value = ""
    }

    function setUsername(name: string) {
        username.value = name
    }

    return {
        // fields
        access_token,
        refresh_token,
        username,
        logined,

        // actions
        login,
        logout,
        setUsername,
    }
})
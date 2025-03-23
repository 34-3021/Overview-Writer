import { defineStore } from "pinia"

export const useUserStore = defineStore('user', () => {
    const token = ref("")
    const username = ref("")
    const logined = computed(() => token.value != "")

    function login(token_: string) {
        if (token_ == "") {
            return false;
        }
        token.value = token_;
        return true;
    }

    function logout() {
        token.value = ""
    }

    function setUsername(name: string) {
        username.value = name
    }

    return {
        // fields
        token,
        username,
        logined,

        // actions
        login,
        logout,
        setUsername,
    }
})
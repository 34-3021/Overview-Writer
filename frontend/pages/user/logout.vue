<template>
    <div></div>
</template>

<script setup lang="ts">

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

userStore.logout()
router.push('/user/login')

toast.add({ title: '已成功登出，请重新登陆', color: 'green' })
</script>
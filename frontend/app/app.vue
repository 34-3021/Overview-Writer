<script lang="ts" setup>
import type { NavigationMenuItem } from '@nuxt/ui'
import colors from 'tailwindcss/colors'

const route = useRoute()
const user = useUserStore()
const appConfig = useAppConfig()
const colorMode = useColorMode()

const color = computed(() => colorMode.value === 'dark' ? (colors as any)[appConfig.ui.colors.neutral][900] : 'white')
const radius = computed(() => `:root { --ui-radius: ${appConfig.theme.radius}rem; }`)
const blackAsPrimary = computed(() => appConfig.theme.blackAsPrimary ? `:root { --ui-primary: black; } .dark { --ui-primary: white; }` : ':root {}')

useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { key: 'theme-color', name: 'theme-color', content: color }
  ],
  style: [
    { innerHTML: radius, id: 'nuxt-ui-radius', tagPriority: -2 },
    { innerHTML: blackAsPrimary, id: 'nuxt-ui-black-as-primary', tagPriority: -2 }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})

const links = computed<NavigationMenuItem[]>(() => {
  const unlogined_links = [
    {
      label: "登录",
      icon: "i-material-symbols-login-rounded",
      to: "/user/login",
      active: route.path.startsWith("/user/login"),
    },
  ];

  if (!user.logined) {
    return unlogined_links;
  }

  const default_links = [
    {
      label: "主页",
      icon: "i-material-symbols-home-outline",
      to: "/",
      active: route.path === "/",
    },
    {
      label: "文献管理",
      icon: "i-material-symbols-folder-managed-outline",
      to: "/files",
      active: route.path.startsWith("/files"),
    },
    {
      label: "我的论文",
      icon: "i-material-symbols-document-scanner-outline",
      to: "/documents",
      active: route.path.startsWith("/documents"),
    },
    {
      label: "椅子",
      icon: "i-material-symbols-chair-alt-outline-rounded",
      to: "/chair",
      active: route.path.startsWith("/chair"),
    },
    {
      label: "登出",
      icon: "i-material-symbols-logout-rounded",
      to: "/user/logout",
      active: route.path.startsWith("/user/logout"),
    },
  ];

  return default_links;
});
</script>

<template>
  <UApp>
    <Header :links="links" />

    <NuxtLayout>
      <div
        class="flex items-center justify-center"
        style="min-height: calc(100vh - 204px)"
      >
        <NuxtPage />
      </div>
    </NuxtLayout>

    <Footer />
  </UApp>
</template>

<style>
/* Safelist (do not remove): [&>div]:*:my-0 [&>div]:*:w-full h-64 !px-0 !py-0 !pt-0 !pb-0 !p-0 !justify-start !justify-end !min-h-96 h-136 */

.page-enter-active,
.page-leave-active {
  transition: all 0.2s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

</style>

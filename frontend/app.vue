<script lang="ts" setup>
import type { NavigationMenuItem } from '@nuxt/ui'

const route = useRoute();
const user = useUserStore();

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
      label: "椅子",
      icon: "i-material-symbols-chair-alt-outline-rounded",
      to: "/chair",
      active: route.path.startsWith("/chair"),
    },
    {
      label: "椅子",
      icon: "i-material-symbols-chair-alt-outline-rounded",
      to: "/chair",
      active: route.path.startsWith("/chair"),
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
</style>

<script lang="ts" setup>
import type { HeaderLink } from "#ui-pro/types";

const route = useRoute();
const user = useUserStore();

const links = computed<HeaderLink[]>(() => {
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
  <div>
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

    <UNotifications />
    <UModals />
    <USlideovers />
  </div>
</template>

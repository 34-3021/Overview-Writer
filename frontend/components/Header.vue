<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

defineProps<{
  links: NavigationMenuItem[]
}>()

// const route = useRoute()
const { $ui } = useNuxtApp()

const route = useRoute()
</script>

<template>
  <UHeader :ui="{ left: 'min-w-0' }" :menu="{ shouldScaleBackground: true }">
    <template #left>
      <NuxtLink to="/" class="flex items-end gap-2 font-bold text-xl text-gray-900 dark:text-white min-w-0" aria-label="Overview Writer">
        <p>综述写作助手</p>
      </NuxtLink>
    </template>

    <UNavigationMenu :items="links" variant="link" />

    <template #right>
      <ThemePicker />

      <UButton
        color="neutral"
        to="https://github.com/34-3021/Overview-Writer"
        variant="ghost"
        target="_blank"
        icon="i-simple-icons-github"
        aria-label="GitHub"
      />
    </template>

    <template #body>
      <UAsideLinks :links="links" />

      <!-- <USeparator type="dashed" class="mt-4 mb-6" /> -->
    </template>
  </UHeader>
</template>

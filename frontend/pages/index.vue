<script setup lang="ts">

// 定义页面的数据
const page = ref({
  title: '综述写作助手',
  description: '邦邦卡邦！欢迎来到综述写作助手喵！', // will not show on page
  hero: {
    title: 'DeepReview: AI-Powered Research Writing',
    description: 'Transform Raw Data into Publication-Ready Manuscripts via Neural Network-Driven Analysis of 10M+ CS Publications.',
    links: [
      {
        'label': 'Get started',
        // icon: 'i-heroicons-arrow-right-20-solid',
        // icon: 'i-heroicons-rocket-launch',
        // trailing: true,
        'trailing-icon': 'i-heroicons-arrow-small-right',
        'to': '#utils',
        'size': 'xl',
        // style: {
        //   borderRadius: '9999px',
        //   padding: '1rem 2rem',
        // },
      },
    ],
  },
  utils: {
    // headline: 'Utilities',
    title: 'Quick Access',
    description: '',
    items: [
      {
        title: '我也不知道写什么了先放把椅子在这里',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
        link: '/chair',
        icon: 'i-material-symbols-chair-alt-outline-rounded',
      },
      {
        title: '我也不知道写什么了先放把椅子在这里',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
        link: '/chair',
        icon: 'i-material-symbols-chair-alt-outline-rounded',
      },
      {
        title: '我也不知道写什么了先放把椅子在这里',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
        link: '/chair',
        icon: 'i-material-symbols-chair-alt-outline-rounded',
      },
      {
        title: '我也不知道写什么了先放把椅子在这里',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
        link: '/chair',
        icon: 'i-material-symbols-chair-alt-outline-rounded',
      },
    ],
  },
})
</script>

<template>
  <div>
    <!-- Hero Section -->
    <ULandingHero
      :title="page.hero.title"
      :description="page.hero.description"
      :links="page.hero.links"
    />

    <!-- utils Section -->
    <ULandingSection

      icon="i-heroicons-rocket-launch"
      :title="page.utils.title"
      :description="page.utils.description"
    >
      <ULandingGrid>
        <ULandingCard
          v-for="(item, index) in page.utils.items"
          id="utils"
          :key="index"
          class="col-span-6 row-span-2"
          :title="item.title"
          :description="item.description"
          :to="item.link"
          :icon="item.icon"
        />
      </ULandingGrid>
    </ULandingSection>
  </div>
</template>

<style scoped>
</style>

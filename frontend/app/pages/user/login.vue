<script setup lang="ts">
import { useUserStore } from "~/store/user";
import { callApi } from "~/../api/api";
import { loginSchema } from "~/../api/user/login";

const fields = [
  {
    name: "username",
    type: "text",
    label: "用户名",
    placeholder: "请输入您的用户名",
    required: true,
  },
  {
    name: "password",
    type: "password",
    label: "密码",
    placeholder: "请输入您的密码",
    required: true,
  },
];

// 定义验证函数
function validate(state: any) {
  const errors = [];
  if (!state.username) {
    errors.push({ path: "username", message: "用户名为必填项" });
  }
  if (!state.password) {
    errors.push({ path: "password", message: "密码为必填项" });
  }
  return errors;
}

// 定义错误信息
const errorMessage = ref("");

// 定义加载状态
const loading = ref(false);

// 使用路由进行跳转
const router = useRouter();

const toast = useToast();

// 添加密码哈希函数
async function hashPassword(password: string): Promise<string> {
  // 使用Web Crypto API进行哈希
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  
  // 将ArrayBuffer转换为十六进制字符串
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function onSubmit(field: any) {
  loading.value = true;
  errorMessage.value = "";

  const { type, data } = await callApi(loginSchema, {
    ...field,
    // password: await hashPassword(field.password)
  });

  console.log(type, data);

  if (type === "success") {
    loading.value = false;
    const userStore = useUserStore();
    if (userStore.login(data.token)) {
      router.push("/");
      toast.add({ title: "登录成功", color: "primary" });
    } else {
      errorMessage.value = "后端返回的数据无效";
    }
  } else {
    errorMessage.value = data.message;
  }

  loading.value = false;
}
</script>

<template>
  <UCard class="max-w-sm w-full mx-auto p-6 rounded-lg shadow-md">
    <UAuthForm
      :fields="fields"
      :validate="validate"
      title="欢迎回来！"
      align="top"
      icon="i-heroicons-lock-closed"
      :ui="{ base: 'text-center', footer: 'text-center' }"
      :loading="loading"
      :submit-button="{
        label: '登录',
        icon: 'i-material-symbols-login-rounded',
      }"
      @submit="onSubmit"
    >
      <template #validation>
        <UAlert
          v-if="errorMessage"
          color="error"
          icon="i-heroicons-information-circle-20-solid"
          :title="errorMessage"
        />
      </template>

      <template #footer>
        登录即表示您同意我们的
        <NuxtLink to="/user/terms" class="text-primary font-medium">
          服务条款 </NuxtLink
        >。
      </template>
    </UAuthForm>
  </UCard>
</template>

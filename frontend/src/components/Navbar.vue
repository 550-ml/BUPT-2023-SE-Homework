<template>
  <nav class="w-screen flex justify-around py-8 mx-auto bg-white border-b">
    <div>
      <h3 class="text-2xl font-medium text-blue-500">LOGO</h3>
    </div>
    <div class="flex items-center space-x-8">
      <RouterLink to="/">主页</RouterLink>
      <RouterLink to="/login">登录</RouterLink>
      <RouterLink to="/register">注册</RouterLink>
      <button @click="Logout" class="justify-end">退出</button>
    </div>
  </nav>
</template>
   
<script lang="ts">
import { useRouter } from 'vue-router';
export default {
  setup() {
    const router = useRouter();
    const Logout = () => {
      localStorage.clear();
      router.push({ path: '/login' });
    };
    return { Logout };
  },
};
</script>
   
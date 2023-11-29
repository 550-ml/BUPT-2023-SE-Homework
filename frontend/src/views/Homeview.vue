<!-- YourMainComponent.vue -->
<template>
  <div class="flex">
    <!-- 左侧 1/4 - 侧边栏 -->
    <div class="w-1/4 p-4 mr-4 bg-white rounded-xl shadow-md">
      <aside class="h-full bg-gray-800 text-white flex flex-col rounded-xl overflow-y-auto">
        <div class="p-4 bg-gray-900">
          <h2 class="text-2xl font-semibold">Sidebar</h2>
        </div>
        <div class="flex-1 p-4">
          <router-link to="/panel1" class="block py-2 hover:bg-gray-700 text-blue-500">客房管理</router-link>
          <router-link to="/panel2" class="block py-2 hover:bg-gray-700 text-blue-500">账单查看</router-link>
          <router-link to="/panel3" class="block py-2 hover:bg-gray-700 text-blue-500">酒店管理</router-link>
        </div>
        <div class="p-4 bg-gray-900">
          <p class="text-sm">&copy; 2023 My Website</p>
        </div>
      </aside>
    </div>

    <!-- 右侧 3/4 - 内容区域 -->
    <div class="flex-3 p-8 bg-gray-100 rounded-xl shadow-md">
      <!-- 根据 selectedPanel 动态渲染不同的组件 -->
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { useRouter } from "vue-router";

export default {
  name: "HomeView",
  setup() {
    const router = useRouter();
    const Logout = () => {
      localStorage.clear();
      router.push({ path: "/login" });
    };
    return { Logout };
  },
};
</script>

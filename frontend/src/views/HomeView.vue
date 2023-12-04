<!-- YourMainComponent.vue -->
<template>
  <div class="">
    <!-- 左侧 1/4 - 侧边栏 -->
    <div class="w-1/4 h-full bg-white rounded-xl shadow-md fixed">
      <aside class="h-full bg-gray-800 text-white flex flex-col rounded-xl">
        <div class="py-4 pl-4 bg-gray-900">
          <router-link to="/login" class="block py-2 hover:bg-gray-700 text-blue-500"
            ><h2 class="text-2xl font-semibold">Sidebar</h2></router-link
          >
        </div>
        <div class="flex-1 py-4 pl-4">
          <router-link to="/airconditionermanage" class="block py-2 hover:bg-gray-700 text-blue-500">空调管理</router-link>
          <router-link to="/check" class="block py-2 hover:bg-gray-700 text-blue-500">房间管理</router-link>
          <router-link to="/panel3" class="block py-2 hover:bg-gray-700 text-blue-500">酒店管理</router-link>
        </div>
        <div class="p-4 bg-gray-900">
          <p class="text-sm">&copy; 2023 My Website</p>
        </div>
      </aside>
    </div>

    <!-- 右侧 3/4 - 内容区域 -->
    <div class="w-3/4 right-0 absolute bg-white rounded-xl">
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
  }
};
</script>

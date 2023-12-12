<template>
  <div class="">
    <div class="w-1/5 h-full bg-white shadow-md fixed">
      <aside class="h-full bg-gray-800 text-white flex flex-col">
        <div class="py-4 pl-4 bg-gray-900">
          <router-link to="/login" class="block py-2 hover:bg-gray-700"
            ><h2 class="text-2xl font-semibold">Sidebar</h2></router-link
          >
        </div>
        <div class="flex-1 py-4 pl-4">
          <router-link to="/airconditionermanage" class="block py-2 hover:bg-gray-700">空调管理</router-link>
          <router-link to="/check" class="block py-2 hover:bg-gray-700">房间管理</router-link>
          <router-link to="/manager" class="block py-2 hover:bg-gray-700">酒店管理</router-link>
        </div>
        <div class="p-4 bg-gray-900">
          <p class="text-sm">&copy; 2023 My Website</p>
        </div>
      </aside>
    </div>

    <div class="w-4/5 right-0 absolute bg-white rounded-xl">
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

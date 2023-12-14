<template>
  <div class="w-full px-2 my-4">
    <div class="flex items-center justify-between mb-4 mr-4">
      <div class="flex justify-start">
        <button @click="openAdd" class="py-2 px-4 rounded cursor-pointer">
          <span class="">添加房间</span>
        </button>
        <button @click="openDelete" class="py-2 px-4 rounded cursor-pointer">
          <span class="">删除房间</span>
        </button>
      </div>
    </div>

    <table class="w-full">
      <tbody class="relative flex flex-col h-full min-w-0 break-words border-0 shadow-xl rounded-2xl">
        <tr
          v-for="deviceId in allDevices"
          :key="deviceId"
          class="flex justify-between items-center px-6 py-4 border-b border-solid rounded-t-2xl border-b-slate-100"
        >
          <td>{{ deviceId }}</td>
          <td>
            <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="getSingleDevice(deviceId)">
              查看收入状况
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div v-if="isAddOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-8 max-w-md rounded shadow-md">
      <h2 class="text-2xl font-bold mb-4">添加房间</h2>

      <!-- 输入框 -->
      <input
        v-model="roomToAdd"
        class="p-2 border border-gray-300 rounded w-full mb-4"
        placeholder="请输入待添加房间"
      />

      <!-- 按钮组 -->
      <div class="flex justify-end">
        <button @click="addRoom" class="bg-blue-500 text-white py-2 px-4 rounded mr-2">添加房间</button>
        <button @click="closeAdd" class="bg-gray-300 text-gray-700 py-2 px-4 rounded">取消</button>
      </div>
    </div>
  </div>

  <div v-if="isDeleteOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-8 max-w-md rounded shadow-md">
      <h2 class="text-2xl font-bold mb-4">添加房间</h2>

      <!-- 输入框 -->
      <input
        v-model="roomToDelete"
        class="p-2 border border-gray-300 rounded w-full mb-4"
        placeholder="请输入待删除房间"
      />

      <!-- 按钮组 -->
      <div class="flex justify-end">
        <button @click="deleteRoom" class="bg-blue-500 text-white py-2 px-4 rounded mr-2">删除房间</button>
        <button @click="closeDelete" class="bg-gray-300 text-gray-700 py-2 px-4 rounded">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const isAddOpen = ref(false);
    const isDeleteOpen = ref(false);
    const allDevices = ref([]);
    const roomId = ref(null);
    const csrfToken = ref("abcde12345"); // 替换为实际的 CSRF token
    const requestData = ref({
      room: "2-233",
      public_key: "your_rsa_public_key_here" // 替换为实际的 RSA 4096 公钥
    });
    const roomToDelete = ref("");

    // 获取所有设备
    const getAllDevices = async () => {
      // try {
      //   const response = await axios.get("/admin/devices", {
      //     headers: {
      //       "X-CSRF-Token": csrfToken.value
      //     }
      //   });
      //   allDevices.value = response.data;
      // } catch (error) {
      //   console.error("Failed to get devices:", error.response.data);
      // }
      allDevices.value = ["101", "102", "103"];
    };

    // 打开添加房间对话框
    const openAdd = () => {
      isAddOpen.value = true;
    };

    // 关闭添加房间对话框
    const closeAdd = () => {
      isAddOpen.value = false;
    };

    const openDelete = () => {
      isDeleteOpen.value = true;
    };

    // 关闭添加房间对话框
    const closeDelete = () => {
      isDeleteOpen.value = false;
    };

    // 添加房间
    const addRoom = async () => {
      try {
        const response = await axios.put("/admin/device", requestData.value, {
          headers: {
            "X-CSRF-Token": csrfToken.value
          }
        });
        const addedDevice = response.data;
        console.log("添加设备成功:", addedDevice);
        closeAdd(); // 添加成功后关闭对话框
      } catch (error) {
        console.error("添加设备失败:", error.response.data);
      }
    };

    const deleteRoom = async () => {
      try {
        await axios.delete("/admin/device", {
          headers: {
            "X-CSRF-Token": csrfToken.value
          },
          data: {
            room: roomToDelete.value
          }
        });

        console.log("删除设备成功");
      } catch (error) {
        console.error("删除设备失败:", error.response.data);
      }
    };

    // 生命周期钩子，mounted
    onMounted(() => {
      getAllDevices();
    });

    // 返回需要在模板中使用的变量和方法
    return {
      isAddOpen,
      isDeleteOpen,
      allDevices,
      roomId,
      roomToDelete,
      openAdd,
      closeAdd,
      openDelete,
      closeDelete,
      addRoom,
      deleteRoom,
      getAllDevices
    };
  }
};
</script>

<style scoped>
button span::after {
  content: "";
  display: block;
  width: 0;
  height: 2px;
  background-color: #3182ce;
  transition: width 0.1s ease;
}

button:hover span::after,
button:focus span::after {
  width: 100%;
}
</style>

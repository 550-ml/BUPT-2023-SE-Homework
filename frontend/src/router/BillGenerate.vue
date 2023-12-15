<template>
  <div class="w-full px-2 my-4">
    <div class="flex items-center justify-between mb-4 mr-4">
      <div class="flex justify-start">
        <button @click="changeTab('tab1')" class="py-2 px-4 rounded cursor-pointer">
          <span class="">未入住房间</span>
        </button>
        <button @click="changeTab('tab2')" class="py-2 px-4 rounded cursor-pointer">
          <span class="">已入住房间</span>
        </button>
      </div>

      <div class="flex justify-end">
        <input
          type="text"
          placeholder="请输入房间号"
          class="p-2 border border-gray-300 rounded mr-2"
          v-model="searchTerm"
          @input="emitSearch"
        />
        <button class="bg-blue-500 text-white py-2 px-4 rounded" @click="executeSearch">搜索</button>
      </div>
    </div>

    <div v-if="searchedDeviceData">
      <div class="flex justify-center">
        <table class="border-collapse w-60 mt-8 shadow-md rounded-md overflow-hidden">
          <tbody>
            <tr v-for="(value, key) in searchedDeviceData" :key="key">
              <th class="border p-2 bg-gray-100">{{ key }}</th>
              <td class="border p-2">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex justify-center items-center py-4 space-x-4">
        <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="openCheckOut">退房</button>
        <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="cancelSearch">返回房间列表</button>
      </div>
    </div>

    <div v-else>
      <div class="flex justify-center">
        <div v-if="activeTab === 'tab1'" class="mt-4 w-1/2">
          <table class="w-full">
            <tbody class="relative flex flex-col h-full min-w-0 break-words border-0 shadow-xl rounded-2xl">
              <tr
                v-for="deviceId in allUnCheckedDevices"
                :key="deviceId"
                class="flex justify-between items-center px-6 py-4 border-b border-solid rounded-t-2xl border-b-slate-100"
              >
                <td>{{ deviceId }}</td>
                <td>
                  <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="openCheckIn">
                    入住
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else-if="activeTab === 'tab2'" class="mt-4 w-1/2">
          <table class="w-full">
            <tbody class="relative flex flex-col h-full min-w-0 break-words border-0 shadow-xl rounded-2xl">
              <tr
                v-for="deviceId in allDevices"
                :key="deviceId"
                class="flex justify-between items-center px-6 py-4 border-b border-solid rounded-t-2xl border-b-slate-100"
              >
                <td>{{ deviceId }}</td>
                <td>
                  <button
                    class="bg-blue-500 text-white py-2 px-4 rounded item-center"
                    @click="getSingleDevice(deviceId)"
                  >
                    退房
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="errorMessage" class="modal">
      <div class="modal-content">
        <p>{{ errorMessage }}</p>
        <button @click="closeModal" class="bg-blue-500 text-white py-2 px-4 rounded mt-4">关闭</button>
      </div>
    </div>
  </div>

  <div v-if="isCheckInOpen" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div v-if="isUnCheckIn" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-8 max-w-md rounded shadow-md">
        <input
          v-model="initTemperature"
          class="p-2 border border-gray-300 rounded w-full mb-4"
          placeholder="请输入默认温度"
        />
        <div class="flex justify-end">
          <button @click="checkIn(roomId, initTemperature)" class="bg-blue-500 text-white py-2 px-4 rounded mr-2">
            入住
          </button>
          <button @click="closeCheckIn" class="bg-gray-300 text-gray-700 py-2 px-4 rounded">取消</button>
        </div>
      </div>
    </div>
    <div v-else class="bg-white p-6 rounded shadow-md">
      <h2>入住成功！</h2>
      <button @click="closeCheckIn" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">返回</button>
    </div>
  </div>

  <div v-if="isCheckOutOpen" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white p-6 rounded shadow-md">
      <div>
        <h2>xxx房间账单</h2>
      </div>
      <div>
        <h2>xxx房间详单</h2>
      </div>
      <button @click="closeCheckOut" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">返回</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUpdated } from "vue";
import RoomStates from "../components/RoomState.vue";
import axios from "axios";
import api from "../main.ts";

export default {
  components: {
    RoomStates
  },
  setup() {
    const searchTerm = ref("");
    const searchedDeviceData = ref(null);
    const isUnCheckIn = ref(true);
    const isCheckInOpen = ref(false);
    const isCheckOutOpen = ref(false);
    const isDetailedOrderOpen = ref(false);
    const activeTab = ref("tab1");
    const allDevices = ref([]);
    const allUnCheckedDevices = ref([]);
    const roomId = ref(null);
    const initTemperature = ref(0);

    const executeSearch = () => {
      // if (!searchTerm.value) {
      //   return;
      // }

      getSingleDevice(searchTerm.value);
    };

    const getSingleDevice = async roomId => {
      searchedDeviceData.value = {
        room: roomId,
        temperature: 26,
        wind_speed: 3,
        mode: "cold",
        sweep: true,
        is_on: true,
        last_update: "2023-09-18T11:45:14+08:00"
      };
    };

    const cancelSearch = () => {
      searchedDeviceData.value = null;
    };

    const openCheckIn = () => {
      isCheckInOpen.value = true;
    };

    const closeCheckIn = () => {
      isCheckInOpen.value = false;
      isUnCheckIn.value = true;
    };

    const openCheckOut = () => {
      isCheckOutOpen.value = true;
    };

    const closeCheckOut = () => {
      isCheckOutOpen.value = false;
    };

    const changeTab = tab => {
      searchedDeviceData.value = null;
      activeTab.value = tab;
      if (tab == "tab1") {
        getAllUnCheckedDevices();
      } else if (tab == "tab2") {
        getAllDevices();
      }
    };

    const getAllUnCheckedDevices = async () => {
      try {
        const response = await api.get("/admin/uncheck_in", {
          headers: {
            "X-CSRF-Token": "abcde12345" // Include the CSRF token if available
          }
        });
        console.log(response.data);
        allUnCheckedDevices.value = response.data;
      } catch (error) {
        console.error("Failed to get devices:", error.response.data);
      }
    };

    const getAllDevices = async () => {
      try {
        const response = await api.get("/admin/devices", {
          headers: {
            "X-CSRF-Token": "abcde12345" // Include the CSRF token if available
          }
        });

        allDevices.value = response.data;
      } catch (error) {
        console.error("Failed to get devices:", error.response.data);
      }
    };

    const checkIn = async (roomId, initTemperature) => {
      isUnCheckIn.value = false;
      console.log(initTemperature.value); // 输出温度值F
      try {
        const response = await api.post(
          "/room/check_in",
          {
            room: roomId
          },
          {
            headers: {
              "X-CSRF-Token": "abcde12345" // Include the CSRF token if available
            }
          }
        );

        const checkedInRoom = response.data.room;

        openCheckIn();
      } catch (error) {
        // Handle unauthorized or other errors
        console.error("Check-in failed:", error.response.data);
      }
    };

    const checkOut = async () => {
      try {
        const response = await api.post(
          "/room/check_out",
          {
            room: roomId
          },
          {
            headers: {
              "X-CSRF-Token": csrfToken.value
            }
          }
        );

        const { room, report } = response.data;
        console.log("Check-out 成功:", room, report);

        // 将返回的 report 数据存储在 checkoutReport 中
        checkoutReport.value = report;
      } catch (error) {
        console.error("Check-out 失败:", error.response.data);
      }
    };

    onMounted(() => {
      getAllDevices();
      getAllUnCheckedDevices();
    });

    return {
      // errorMessage,
      searchTerm,
      searchedDeviceData,
      isUnCheckIn,
      isCheckInOpen,
      isCheckOutOpen,
      isDetailedOrderOpen,
      activeTab,
      allDevices,
      allUnCheckedDevices,
      roomId,
      executeSearch,
      getSingleDevice,
      cancelSearch,
      openCheckIn,
      closeCheckIn,
      openCheckOut,
      closeCheckOut,
      changeTab,
      getAllUnCheckedDevices,
      getAllDevices,
      checkIn,
      checkOut
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

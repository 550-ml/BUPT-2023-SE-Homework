<!--
  文件名: BillGenerate.vue
  功能: 这个文件是用于入住、退房和产生账单详单的界面。
  作者: 鲁启航
  创建日期: 2023-11-11
-->
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
                  <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="openCheckIn(deviceId)">
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
                  <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="openCheckOut(deviceId)">
                    退房
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
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
          <button @click="checkIn(roomId)" class="bg-blue-500 text-white py-2 px-4 rounded mr-2">入住</button>
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
    <div v-if="isUnCheckOut">
      <div class="bg-white p-8 max-w-md rounded shadow-md">
        <p>确认退房？</p>
        <div class="flex justify-end">
          <button @click="checkOut(roomId)" class="bg-blue-500 text-white py-2 px-4 rounded mr-2">确认</button>
          <button @click="closeCheckOut" class="bg-gray-300 text-gray-700 py-2 px-4 rounded">取消</button>
        </div>
      </div>
    </div>
    <div v-else class="bg-white p-6 rounded shadow-md">
      <div>
        <h2 class="text-center py-4">{{ roomId }}号房间账单</h2>
        <table class="w-full border-collapse border shadow-md">
          <thead>
            <tr class="bg-gray-200">
              <th class="p-4">total cost</th>
              <th class="p-4">total time</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="p-4 text-center border">{{ billReport.total_cost }}</td>
              <td class="p-4 text-center border">{{ billReport.total_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-center py-4">{{ roomId }}号房间详单</h2>
        <table class="w-full border-collapse border shadow-md">
          <thead>
            <tr class="bg-gray-200">
              <th class="p-4">Cost</th>
              <th class="p-4">Duration</th>
              <th class="p-4">End Time</th>
              <th class="p-4">Mode</th>
              <th class="p-4">Start Time</th>
              <th class="p-4">Wind Speed</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="detail in detailedReport" :key="detail.id">
              <td v-for="(value, key) in detail" :key="key" class="p-4 text-center border">
                {{ value }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="saveToExcel" class="mr-2 mt-4 bg-blue-500 text-white py-2 px-4 rounded">保存</button>
      <button @click="closeCheckOut" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">返回</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUpdated } from "vue";
import RoomStates from "../components/RoomState.vue";
import api from "../main.ts";
import * as XLSX from "xlsx";

export default {
  components: {
    RoomStates
  },
  setup() {
    const searchTerm = ref("");
    const searchedDeviceData = ref(null);
    const isUnCheckIn = ref(true);
    const isUnCheckOut = ref(true);
    const isCheckInOpen = ref(false);
    const isCheckOutOpen = ref(false);
    const activeTab = ref("tab1");
    const allDevices = ref([]);
    const allUnCheckedDevices = ref([]);
    const initTemperature = ref(0);
    const checkoutReport = ref("");
    const billReport = ref(null);
    const detailedReport = ref(null);

    let roomId = ref("");

    const executeSearch = () => {
      console.log(searchTerm.value);
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

    /**
     * 定义一系列函数更改状态变量，用于控制对话框的弹出
     */
    const cancelSearch = () => {
      searchedDeviceData.value = null;
    };

    const openCheckIn = deviceId => {
      roomId = deviceId;
      isCheckInOpen.value = true;
    };

    const closeCheckIn = () => {
      isCheckInOpen.value = false;
      isUnCheckIn.value = true;
    };

    const openCheckOut = deviceId => {
      roomId.value = deviceId;
      isCheckOutOpen.value = true;
    };

    const closeCheckOut = () => {
      isCheckOutOpen.value = false;
      isUnCheckOut.value = true;
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

    /**
     * 获取所有未入住房间
     * @function getAllUnCheckedDevices
     * @description 发送请求，获取所有未入住房间的列表
     * @returns {void}
     */
    const getAllUnCheckedDevices = async () => {
      try {
        const response = await api.get("/admin/uncheck_in", {
          headers: {
            "X-CSRF-Token": "abcde12345"
          }
        });
        allUnCheckedDevices.value = response.data;
      } catch (error) {
        console.error("Failed to get devices:", error.response.data);
      }
    };

    /**
     * 获取所有已入住房间
     * @function getAllDevices
     * @description 发送请求，获取所有已入住房间的列表
     * @returns {void}
     */
    const getAllDevices = async () => {
      try {
        const response = await api.get("/admin/devices", {
          headers: {
            "X-CSRF-Token": "abcde12345"
          }
        });

        allDevices.value = response.data;
      } catch (error) {
        console.error("Failed to get devices:", error.response.data);
      }
    };

    /**
     * 入住
     * @function checkIn
     * @description 发送请求，入住指定房间
     * @returns {void}
     */
    const checkIn = async () => {
      console.log(roomId);
      try {
        const response = await api.post(
          "/room/check_in",
          {
            room: roomId,
            temperature: initTemperature.value
          },
          {
            headers: {
              "X-CSRF-Token": "abcde12345"
            }
          }
        );

        const checkedInRoom = response.data.room;
        isUnCheckIn.value = false;
        openCheckIn();
      } catch (error) {
        console.error("Check-in failed:", error.response.data);
      }
    };

    /**
     * 退房并生成账单详单
     * @function checkOut
     * @description 发送请求，对指定房间进行退房，并产生账单与详单
     * @returns {void}
     */
    const checkOut = async () => {
      try {
        const response = await api.post(
          "/room/check_out",
          {
            room: roomId.value
          },
          {
            headers: {
              "X-CSRF-Token": "abcde12345"
            }
          }
        );

        console.log("Check-out 成功:", response.data);

        checkoutReport.value = response.data;
        billReport.value = checkoutReport.value;
        detailedReport.value = checkoutReport.value.details;
        isUnCheckOut.value = false;
      } catch (error) {
        console.error("Check-out 失败:", error.response.data);
      }
      isUnCheckOut.value = false;
    };

    /**
     * 保存账单与详单
     * @function saveToExcel
     * @description 将账单与详单保存为一个excel中的两个表格
     * @returns {void}
     */
    const saveToExcel = () => {
      const billSheet = XLSX.utils.json_to_sheet(checkoutReport.value.details);

      const totalSheet = XLSX.utils.json_to_sheet([
        {
          "Total Cost": checkoutReport.value.total_cost,
          "Total Time": checkoutReport.value.total_time
        }
      ]);

      let wb = XLSX.utils.book_new();

      XLSX.utils.book_append_sheet(wb, totalSheet, "Bill");

      const detailsSheet = XLSX.utils.json_to_sheet(checkoutReport.value.details);
      XLSX.utils.book_append_sheet(wb, detailsSheet, "Details");
      const blob = XLSX.writeFile(wb, "report" + roomId.value + ".xlsx");
      URL.createObjectURL(blob.files);
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
      isUnCheckOut,
      isCheckInOpen,
      isCheckOutOpen,
      activeTab,
      allDevices,
      allUnCheckedDevices,
      roomId,
      initTemperature,
      checkoutReport,
      billReport,
      detailedReport,
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
      checkOut,
      saveToExcel
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

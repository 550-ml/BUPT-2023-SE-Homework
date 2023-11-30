<template>
    <tr @click="showDetails" class="hover:bg-gray-100 cursor-pointer">
      <td class="py-2 px-4 border border-gray-300">
        {{ thumbnailInfo }}
      </td>
      <td v-if="showDialog" colspan="2" class="dialog bg-white p-6 border border-gray-300 shadow-lg">
        {{ fullInfo }}
        <button @click="closeDialog" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">关闭</button>
      </td>
    </tr>
  </template>
  
  <script>
  export default {
    name: "RoomState",
    data() {
      return {
        showDialog: false,
        thumbnailInfo: '缩略信息...',
        fullInfo: '完整信息...'
      };
    },
    methods: {
      showDetails() {
        this.showDialog = true;
      },
      closeDialog() {
        this.showDialog = false;
      }
    }
  };
  </script>
  
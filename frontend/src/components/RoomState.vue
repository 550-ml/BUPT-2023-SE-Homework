<template>
  <tr class="hover:bg-gray-100 cursor-pointer">
    <td class="py-2 px-4 border border-gray-300">
      {{ thumbnailInfo }}
    </td>
    <td class="dialog p-6 border border-gray-300">
      {{ fullInfo }}
      <!-- <button @click="closeDialog" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">关闭</button> -->
    </td>
    <td class="py-2 px-4 border border-gray-300">
      {{ para3 }}
    </td>
  </tr>
</template>

<script>
export default {
  name: "RoomStates",
  data() {
    return {
      showDialog: false,
      thumbnailInfo: "缩略信息...",
      fullInfo: "完整信息...",
      para3: "some message",
    };
  },
  // props: {
  //   rows: Array // 表格数据
  // },
  // data() {
  //   return {
  //     searchTerm: "123" // 用于存储搜索框的值
  //   };
  // },
  // computed: {
  //   filteredRows() {
  //     // 使用搜索框的值（this.searchTerm）来过滤数据
  //     return this.rows.filter(row => row.column1.toLowerCase().includes(this.searchTerm.toLowerCase()));
  //   }
  // },
  // methods: {
  //   updateSearchTerm(newSearchTerm) {
  //     // 更新搜索框的值
  //     this.searchTerm = newSearchTerm;
  //   }
  // },
  // created() {
  //   // 监听来自 SearchBox 组件的搜索事件
  //   this.$root.$on("search", this.updateSearchTerm);
  // },
  // beforeDestroy() {
  //   // 在组件销毁前移除事件监听，防止内存泄漏
  //   this.$root.$off("search", this.updateSearchTerm);
  // }
};
</script>

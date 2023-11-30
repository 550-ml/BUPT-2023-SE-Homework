<!-- <template>
  <div>
    <h1 class="text-3xl font-semibold mb-4">Panel 2 Content</h1>
    <p>Panel 2 的内容...</p>
  </div>
</template> -->
<template>
    <table class="table-auto w-full">
      <thead>
      </thead>
      <tbody>
        <RoomState v-for="index in 3" :key="index" />
      </tbody>
    </table>
  </template>
  
  <script>
  import RoomState from '../components/RoomStateHistory.vue';
  
  export default {
    components: {
      RoomState
    }
  };
  </script>

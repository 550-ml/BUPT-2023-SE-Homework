<template>
    <el-row>
        <el-col v-for="(room, index) in roomsInfo" :key="index" :span="8" :offset="index > 0 ? 3 : 0">
            <el-card :body-style="{ padding: '0px' }">
                <img src="../../assets/room1.jpg" class="image" />
                <div style="padding: 14px">
                    <span>{{ room.roomId }}</span>
                    <div class="bottom">
                        <p>空调模式: {{ room.mode }}</p>
                        <p>当前风速: {{ room.speed }}</p>
                        <p>当前温度: {{ room.currTemp }}</p>
                        <p>目标温度: {{ room.targetTemp }}</p>
                        <p>服务时间: {{ room.servedTime }}</p>
                        <p>服务费用: {{ room.fee }}</p>
                        <el-button text class="button">操作</el-button>
                    </div>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const roomsInfo = ref([
    {
        roomId: 'Room 1',
        mode: 'Cold',
        speed: 'Medium',
        currTemp: '20°C',
        targetTemp: '25°C',
        servedTime: '2 hours',
        fee: '$15'
    },
    {
        roomId: 'Room 2',
        mode: 'Hot',
        speed: 'High',
        currTemp: '30°C',
        targetTemp: '28°C',
        servedTime: '3 hours',
        fee: '$20'
    },
    {
        roomId: 'Room 2',
        mode: 'Hot',
        speed: 'High',
        currTemp: '30°C',
        targetTemp: '28°C',
        servedTime: '3 hours',
        fee: '$20'
    }, {
        roomId: 'Room 1',
        mode: 'Cold',
        speed: 'Medium',
        currTemp: '20°C',
        targetTemp: '25°C',
        servedTime: '2 hours',
        fee: '$15'
    },
    // Add more rooms as needed...
])

// This code keeps track of the current date and time
const currentDate = ref(new Date())
setInterval(() => {
    currentDate.value = new Date()
}, 1000)
</script>

<style>
.time {
    font-size: 12px;
    color: #999;
}

.bottom {
    margin-top: 13px;
    line-height: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.button {
    padding: 0;
    min-height: auto;
}

.image {
    width: 100%;
    display: block;
}
</style>

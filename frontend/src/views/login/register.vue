<!--
  文件名: register.vue
  功能: 这个文件是用于用户注册的界面。
  作者: 王拓
  创建日期: 2023-11-11
-->
<template>
  <div class="register-container">
    <el-form :model="form" label-width="120px" class="register-form">
      <div class="title-container">
        <h3 class="title">注册</h3>
      </div>
      <div class="input-container">
        <el-form-item>
          <el-icon :size="20" class="svg-container icon-user">
            <User />
          </el-icon>
          <el-input v-model="form.username" placeholder="Username" class="custom-input"></el-input>
        </el-form-item>
        <el-form-item>
          <el-icon :size="20" class="svg-container icon-email">
            <Edit />
          </el-icon>
          <el-input v-model="form.email" placeholder="Email" class="custom-input"></el-input>
        </el-form-item>
        <el-form-item>
          <el-icon :size="20" class="svg-container icon-password">
            <Edit />
          </el-icon>
          <el-input v-model="form.password" placeholder="Password" class="custom-input" show-password></el-input>
        </el-form-item>
      </div>
      <el-form-item>
        <el-button class="register-button" type="primary" @click="register">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { User, Edit } from "@element-plus/icons-vue";
const form = ref({
  username: "",
  email: "",
  password: ""
});

const register = () => {
  // Add registration functionality here
};
</script>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;
$cursor: #fff;

.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: $bg;
}

.register-form {
  width: 400px;
  padding: 40px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

  .title-container {
    margin-bottom: 30px;

    .title {
      font-size: 28px;
      color: $dark_gray;
      text-align: center;
      font-weight: bold;
    }
  }

  .input-container {
    .el-form-item {
      border: 1px solid $light_gray;
      border-radius: 4px;
      margin-bottom: 20px;

      .svg-container {
        padding: 6px 5px 6px 15px;
        color: $dark_gray;
        vertical-align: middle;
        display: inline-block;
        margin-right: 5px;
      }

      .el-input {
        display: inline-block;
        height: 48px;
        border: none;
        border-radius: 4px;

        input {
          padding: 0 15px;
          color: $dark_gray;
          background-color: $light_gray;
          border: none;
          border-radius: 4px;
        }
      }
    }
  }

  .register-button {
    width: 100%;
    height: 48px;
    background-color: $dark_gray;
    border: none;
    border-radius: 4px;
    color: #fff;
    font-weight: bold;

    &:hover {
      background-color: darken($dark_gray, 10%);
    }
  }
}
</style>

<template>
  <div class="login-container">
    <el-form :model="form" label-width="120px" class="login-form">
      <div class="title-container">
        <h3 class="title">登录</h3>
      </div>
      <el-form-item>
        <el-icon :size="20" class="svg-container icon-user">
          <User />
        </el-icon>
        <el-input v-model="form.name" placeholder="Username" class="custom-input"></el-input>
      </el-form-item>
      <el-form-item>
        <el-icon :size="20" class="svg-container icon-edit">
          <Edit />
        </el-icon>
        <el-input v-model="form.password" placeholder="Password" class="custom-input" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button class="login-button" type="primary" @click="login">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { User, Edit } from "@element-plus/icons-vue";
const form = ref({
  name: "",
  password: ""
});
import axios from "axios";
import api from "../../main.ts";

const login = () => {
  const loginData = {
    username: form.value.name,
    password: form.value.password
  };
  const jsonData = JSON.stringify(loginData);

  api.post("/login", jsonData)
    .then(response => {
      const { username, role } = response.data;
      console.log("登录成功，角色是:", role);

      // 根据角色进行页面跳转
      switch (role) {
        case 'manager':
          router.push('/manager'); // 跳转到经理仪表盘页面
          break;
        case 'checkout':
          router.push('/check'); // 跳转到结账仪表盘页面
          break;
        case 'AC admin':
          router.push('/airconditionermanage'); // 跳转到空调管理员仪表盘页面
          break;
        default:
          router.push('/airconditionermanage'); // 跳转到默认仪表盘页面，处理其他角色
          break;
      }
    })
    .catch(error => {
      console.error("登录失败", error);
      // 处理登录失败的情况
    });
};
</script>

<style lang="scss" scoped>
// Define your color variables
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;
$cursor: #fff;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;

    :v-deep(.el-form-item) {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }

    :v-deep(.el-input) {
      display: inline-block;
      height: 47px;
      width: 85%;

      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;
      }
    }

    .login-button {
      width: 100%;
      box-sizing: border-box;
    }
  }

  .tips {
    font-size: 16px;
    line-height: 28px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    :v-deep().lang-select {
      position: absolute;
      top: 4px;
      right: 0;
      background-color: white;
      font-size: 22px;
      padding: 4px;
      border-radius: 4px;
      cursor: pointer;
    }
  }

  .show-pwd {
    // position: absolute;
    // right: 10px;
    // top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>

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

const login = () => {
  const loginData = {
    username: form.value.name,
    password: form.value.password
  };
  const jsonData = JSON.stringify(loginData);
  axios
    .post("http://10.129.37.107:11451/api/login", jsonData)
    .then(response => {
      // 处理后端返回的数据
      const { error, role } = response.data;
      if (!error) {
        // username
        // role
        // 登录成功，处理角色信息
        console.log("登录成功，角色是:", role);
        // 可以将角色信息存储在前端，进行后续操作
      } else {
        // 登录失败，处理错误信息
        console.error("登录失败");
        // 可以根据错误信息给用户相应提示
      }
    })
    .catch(error => {
      // 处理网络请求失败等情况
      console.error("登录失败", error);
      // 可以显示一般性错误信息给用户
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

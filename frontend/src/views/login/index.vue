<!--
  文件名: index.vue
  功能: 这个文件是应用的主入口文件, 用于渲染登录界面页面
  作者: 王拓
  创建日期: 2023-11-11
-->
<template>
  <div class="login-background">
    <div class="login-header-text">波普特廉价酒店管理系统</div>
    <div class="hotel-management">
      <img src="../../assets/hotel2.jpg" class="hotel-img">
      <div class="login-container">
        <el-form :model="form" label-width="120px" class="login-form">
          <div class="title-container">
            <h3 class="title">酒店登录</h3>
          </div>
          <el-form-item>
            <el-input v-model="form.name" placeholder="Username" class="custom-input">
              <template #prepend>
                <el-icon :size="20" class="svg-container icon-user">
                  <User />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.password" placeholder="Password" class="custom-input" show-password>
              <template #prepend>
                <el-icon :size="20" class="svg-container icon-edit">
                  <Edit />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="login-button" type="primary" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
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
import { useRouter } from 'vue-router';
const router = useRouter();

/**
 * 登录函数
 * 1. 获取表单中的用户名和密码
 * 2. 将用户名和密码组成 JSON 数据
 * 3. 发送登录请求到后端 API
 * 4. 根据登录成功后返回的角色信息进行页面跳转
 *    - 如果角色是经理，跳转到经理仪表盘页面
 *    - 如果角色是结账员，跳转到结账仪表盘页面
 *    - 如果角色是空调管理员，跳转到空调管理员仪表盘页面
 *    - 其他角色，跳转到默认仪表盘页面
 * 5. 处理登录失败的情况
 */
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
.login-background {
  background: linear-gradient(to top, #edeff1, #5a9be1);
  /* 蓝色渐变背景 */
  height: 100vh;
  /* 设置高度，确保填满整个视口 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.hotel-management {
  background: white;
  /* 白色底色 */
  padding: 20px;
  border-radius: 120px 8px;
  /* 可以根据需要调整边框圆角 */
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  /* 添加阴影效果 */
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 350px;
  margin-right: 350px;
  height: 400px;
  /* 设置更高的高度 */
}

.login-header-text {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 70px;
  font-weight: bold;
  color: #f9f3f3;
  /* 文本颜色 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  /* 添加文本阴影 */
  text-transform: uppercase;
  /* 转换为大写字母 */
  letter-spacing: 2px;
  /* 字符间距 */
  font-family: 'Arial', sans-serif;
  /* 字体样式 */
}


.login-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.hotel-img {
  position: relative;
  max-width: 50%;
  margin-left: 20px;
  border-radius: 20px 5px;
  mix-blend-mode: multiply;
}

.login-container {
  display: flex;
  align-items: center;
}

.hotel-img {
  max-width: 50%;
  margin-right: 20px;
  border-radius: 20px;
  mix-blend-mode: multiply;
  /* 调整混合模式 */
}


.login-form {
  width: 90%;
}

.title-container {
  text-align: center;
  margin-bottom: 20px;
  margin-left: 80px;
  font-size: 40px;
  font-family: Arial, sans-serif;
  /* 通用字体 */
}

.custom-input {
  width: 100%;
  margin-bottom: 15px;
}

.login-button {
  margin-left: 30px;
  width: 70%;
}


// .login-container {
//   width: 100%;
//   background-color: $bg;
//   overflow: hidden;

//   .login-form {
//     position: relative;
//     width: 520px;
//     max-width: 100%;
//     padding: 160px 35px 0;
//     margin: 0 auto;
//     overflow: hidden;

//     :v-deep(.el-form-item) {
//       border: 1px solid rgba(255, 255, 255, 0.1);
//       background: rgba(0, 0, 0, 0.1);
//       border-radius: 5px;
//       color: #454545;
//     }

//     :v-deep(.el-input) {
//       display: inline-block;
//       height: 47px;
//       width: 85%;

//       input {
//         background: transparent;
//         border: 0px;
//         -webkit-appearance: none;
//         border-radius: 0px;
//         padding: 12px 5px 12px 15px;
//         color: $light_gray;
//         height: 47px;
//         caret-color: $cursor;
//       }
//     }

//     .login-button {
//       width: 100%;
//       box-sizing: border-box;
//     }
//   }

//   .tips {
//     font-size: 16px;
//     line-height: 28px;
//     color: #fff;
//     margin-bottom: 10px;

//     span {
//       &:first-of-type {
//         margin-right: 16px;
//       }
//     }
//   }

//   .svg-container {
//     padding: 6px 5px 6px 15px;
//     color: $dark_gray;
//     vertical-align: middle;
//     display: inline-block;
//   }

//   .title-container {
//     position: relative;

//     .title {
//       font-size: 26px;
//       color: $light_gray;
//       margin: 0px auto 40px auto;
//       text-align: center;
//       font-weight: bold;
//     }

//     :v-deep().lang-select {
//       position: absolute;
//       top: 4px;
//       right: 0;
//       background-color: white;
//       font-size: 22px;
//       padding: 4px;
//       border-radius: 4px;
//       cursor: pointer;
//     }
//   }

//   .show-pwd {
//     // position: absolute;
//     // right: 10px;
//     // top: 7px;
//     font-size: 16px;
//     color: $dark_gray;
//     cursor: pointer;
//     user-select: none;
//   }
// }
</style>

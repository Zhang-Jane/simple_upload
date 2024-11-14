<template>

    <el-row class="app-container" justify="center" align="middle">
      <el-col :span="12">
    <h1>欢迎使用文件上传应用</h1>
        <p>请点击下面的按钮上传文件或查看已上传的文件。</p>
        <router-link to="/upload">
          <el-button type="primary" >
            <el-icon><UploadFilled /></el-icon>
            <i class="el-icon-upload"></i> 上传文件
          </el-button>
        </router-link>
        <router-link to="/list">
          <el-button type="success">
            
            <i class="el-icon-folder-opened"></i> 查看已上传文件
          </el-button>
        </router-link>
      </el-col>
    </el-row>
  </template>

  
  <style>
  .app-container {
    height: 100vh; /* 使容器充满视口高度 */
    text-align: center; /* 使文本居中 */
  }
  
  .el-button {
    margin: 10px; /* 按钮之间的间距 */
  }
  </style>
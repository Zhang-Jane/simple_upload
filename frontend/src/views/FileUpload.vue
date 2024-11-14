<template>
  <div>
    <el-upload
      class="upload-info"
      drag
      :action=getUploadUrl()
      :before-upload=handleBeforeUpload
      :on-success=handleUploadSuccess
      :on-error=handleUploadError
      :file-list=fileList
      :show-file-list=false
      ref="upload"
    >
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text" :style="{ color: uploadStatus.color }">
        {{ uploadStatus.message || '将文件拖放到这里，或点击上传' }}
      </div>
    </el-upload>
    
    <div v-if="files.length">
      <h3>已上传文件列表:</h3>
      <ul>
        <li v-for="file in files" :key="file">{{ file }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { uploadFile } from '@/apis/fileApi';
import { BACKEND_BASE_URL } from '@/apis/axios'; // 确保路径正确

export default {
  data() {
    return {
      fileList: [],
      files: [],
      uploadStatus: {
        message: '',
        color: 'black', // 默认颜色
      },
    };
  },
  methods: {
    getUploadUrl() {
      return `${BACKEND_BASE_URL}/upload`; // 动态拼接 URL
    },
    handleBeforeUpload(file) {
      this.fileList.push(file);
      this.uploadStatus.message = `准备上传文件: ${file.name}`;
      this.uploadStatus.color = 'black'; // 重置颜色
      this.submitForm(); // 直接提交表单
    },
    async submitForm() {
      if (this.fileList.length === 0) return; // 确保有文件上传
      try {
        const response = await uploadFile(this.fileList[0].raw); // 上传第一个文件
        this.uploadStatus.message = `文件 "${this.fileList[0].name}" 上传成功: ${response.message}`;
        this.uploadStatus.color = 'green'; // 上传成功，设置为绿色
        this.files.push(this.fileList[0].name); // 将成功上传的文件添加到文件列表
        this.fileList = []; // 清空文件列表
      } catch (error) {
        this.uploadStatus.message = `文件 "${this.fileList[0].name}" 上传失败`;
        this.uploadStatus.color = 'red'; // 上传失败，设置为红色
      }
    },
    handleUploadSuccess(response, file) {
      console.log('Upload success:', response);
      this.uploadStatus.message = `文件 "${file.name}" 上传成功`;
      this.uploadStatus.color = 'green'; // 上传成功，设置为绿色
      this.files.push(file.name); // 将成功上传的文件添加到文件列表
    },
    handleUploadError(err, file) {
      console.error('Upload error:', err);
      this.uploadStatus.message = `文件 "${file.name}" 上传失败`;
      this.uploadStatus.color = 'red'; // 上传失败，设置为红色
    },
  },
};
</script>
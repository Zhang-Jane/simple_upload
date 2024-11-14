<template>
  <div class="file-list">
    <h2>已上传文件列表</h2>
    <el-input v-model="searchQuery" placeholder="搜索文件名" @input="searchFiles"></el-input>
    <el-table :data="paginatedFiles" style="width: 100%">
      <el-table-column prop="file_name" label="文件名称" />
      <el-table-column prop="file_size" label="文件大小" />
      <el-table-column prop="file_type" label="文件格式" />
      <el-table-column prop="created_time" label="上传时间" />
      <el-table-column width="150px" label="操作">
        <template #default="{ row }">
          <el-button size="small" type="text" @click="downloadFile(row.file_name)">下载</el-button>
          <el-button size="small" type="text" @click="deleteFile(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-controls">
      <el-button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</el-button>
      <span>第 {{ currentPage }} 页</span>
      <el-button @click="changePage(currentPage + 1)" :disabled="currentPage * pageSize >= totalFiles">下一页</el-button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { getPaginatedFileList, downloadFile as apiDownloadFile, deleteFile as apiDeleteFile } from '@/apis/fileApi';

export default {
  name: 'FileList',
  setup() {
    const files = ref([]);
    const searchQuery = ref('');
    const currentPage = ref(1);
    const pageSize = ref(5);
    const totalFiles = ref(0);

    const fetchFiles = async (page, limit) => {
      try {
        const skip = (page - 1) * limit;
        const response = await getPaginatedFileList(skip, limit);
        if (response && Array.isArray(response.result)) {
          files.value = response.result; // 更新文件列表
          totalFiles.value = response.total_count; // 更新总文件数
        } else {
          console.error('未返回有效数据:', response);
        }
      } catch (error) {
        console.error('获取文件列表失败:', error);
      }
    };

    const filteredFiles = computed(() => {
      return files.value.filter(file => file.is_deleted === 0 && file.file_name.includes(searchQuery.value));
    });

    const paginatedFiles = computed(() => {
      return filteredFiles.value;
    });

    const searchFiles = async () => {
      currentPage.value = 1; // 重置当前页为1
      await fetchFiles(currentPage.value, pageSize.value); // 重新获取文件列表
    };

    const downloadFile = async (fileName) => {
      try {
        await apiDownloadFile(fileName);
      } catch (error) {
        console.error('下载文件失败:', error);
      }
    };

    const deleteFile = async (id) => {
      const confirmDelete = confirm('确定要删除该文件吗？');
      if (confirmDelete) {
        try {
          await apiDeleteFile(id);
          await fetchFiles(currentPage.value, pageSize.value); // 重新获取文件列表
        } catch (error) {
          console.error('删除文件失败:', error);
        }
      }
    };

    const changePage = (page) => {
      if (page < 1 || page > Math.ceil(totalFiles.value / pageSize.value)) return; // 确保页码在有效范围内
      currentPage.value = page;
      fetchFiles(currentPage.value, pageSize.value); // 每次页码变化时重新获取文件
    };

    onMounted(() => {
      fetchFiles(currentPage.value, pageSize.value); // 组件挂载时获取文件列表
    });

    return {
      files,
      searchQuery,
      totalFiles,
      currentPage,
      pageSize,
      paginatedFiles,
      searchFiles,
      downloadFile,
      deleteFile,
      changePage,
    };
  },
};
</script>

<style>
.file-list {
  margin-top: 50px;
}
.pagination-controls {
  margin-top: 20px;
  display: flex;
  align-items: center;
}
</style>
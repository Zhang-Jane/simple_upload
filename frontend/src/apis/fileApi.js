import axios from './axios';

// 通用请求函数
const makeRequest = async (method, url, data = null, config = {}) => {
  try {
    const response = await axios[method](url, data, config);
    return response.data;
  } catch (error) {
    console.error(`Error during ${method.toUpperCase()} request to ${url}:`, error);
    throw error;
  }
};
export const getPaginatedFileList = async (skip = 0, limit = 10) => {
  try {
    const response = await axios.get('/all_files', {
      params: {
        skip,
        limit
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching files:', error);
    throw error;
  }
};


/** 上传文件 */
export const uploadFile = (file) => {
  if (!file) {
    throw new Error('未选择文件，请选择一个文件进行上传。');
  }

  const formData = new FormData();
  formData.append('file', file);

  return makeRequest('post', '/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/** 删除文件 */
export const deleteFile = (pk_id) => {
  return makeRequest('delete', `/delete/${pk_id}`);
};

/** 搜索文件 */
export const searchFile = (file_name) => {
  return makeRequest('get', `/search/${file_name}`);
};

/** 下载文件 */
export const downloadFile = async (file_name) => {
  try {
    const response = await axios.get(`/download/${file_name}`, {
      responseType: 'blob', // 设置响应类型为 blob
    });

    // 创建一个 URL 对象并下载文件
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', file_name); // 设置下载文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // 移除链接元素
    window.URL.revokeObjectURL(url); // 释放内存
  } catch (error) {
    console.error('Error downloading file:', error);
    throw error;
  }
};
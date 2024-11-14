import axios from 'axios';
import { BACKEND_BASE_URL } from "@/assets/js/global";


// 设置默认配置
axios.defaults.timeout = 5000; // 响应超时时间
axios.defaults.baseURL = BACKEND_BASE_URL; // 请求的根路径

export default axios;
export { BACKEND_BASE_URL };
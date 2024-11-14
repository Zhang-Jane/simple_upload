import { createApp } from 'vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import locale from 'element-plus/es/locale/lang/zh-cn';
import 'element-plus/dist/index.css'; // 引入 Element Plus 样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue'



const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}


app.use(router);
// 语言汉化
app.use(ElementPlus, {
    locale: locale,
  })
app.use(VueAxios, axios)

app.mount('#app');

import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import FileUpload from '../views/FileUpload.vue';
import ListFile from '../views/ListFile.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/upload',
    name: 'FileUpload',
    component: FileUpload,
  },
  {
    path: '/list',
    name: 'ListFile',
    component: ListFile,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
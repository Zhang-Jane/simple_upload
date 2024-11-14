# 文件上传的demo
## 运行
```bash
# dev本地运行
cd simple-upload-file
npm install
npm run dev
```
## 项目目录说明
├── README.md
├── index.html
├── package.json（项目配置和包管理文件）
├── public（存放静态资源公共资源）
├── src（项目主目录）
│   ├── App.vue（root组件）
│   ├── assets（存放静态文件）
│   ├── components（组件）
│   ├── main.js（项目启动的入口js文件）
│   ├── router（路由管理）
│   └── views（页面组件）
└── vite.config.js

参考目录结构：
```bash
├── README.md                     # 项目的说明文档
├── index.html                    # 入口 HTML 文件
├── package.json                  # 项目配置和包管理文件
├── public                        # 存放静态资源公共资源
│   ├── favicon.ico               # 网站图标
│   └── assets                    # 其他静态资源（如图片、字体等）
├── src                           # 项目主目录
│   ├── App.vue                   # 根组件
│   ├── assets                     # 存放静态文件（如图片、图标等）
│   ├── components                # 组件目录
│   │   ├── common                # 公共组件（如按钮、输入框等）
│   │   ├── layout                # 布局组件（如头部、侧边栏等）
│   │   └── specific              # 特定功能组件
│   ├── main.js                   # 项目启动的入口 JS 文件
│   ├── router                    # 路由管理
│   │   ├── index.js              # 路由配置文件
│   ├── store                     # 状态管理（如 Vuex）
│   │   └── index.js              # Vuex 状态管理配置
│   ├── styles                    # 样式文件
│   │   ├── global.css            # 全局样式
│   │   └── variables.scss        # SCSS 变量文件
│   └── views                     # 页面组件
│       ├── Home.vue              # 首页组件
│       ├── About.vue             # 关于页面组件
│       └── NotFound.vue          # 404 页面组件
└── vite.config.js                # Vite 配置文件
```
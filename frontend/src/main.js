import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import Vue3Toastify from 'vue3-toastify';
//import "bootstrap/dist/css/bootstrap.min.css"
import "bootswatch/dist/flatly/bootstrap.min.css"
import "bootstrap-icons/font/bootstrap-icons.css";
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import "bootstrap"
import '@/assets/main.css'
import 'vue3-easy-data-table/dist/style.css';
import 'vue3-toastify/dist/index.css';

const app = createApp(App);
app.use(router);
app.use(Vue3Toastify, {
    autoClose: 3000,
    position: "top-right"
});
app.component('EasyDataTable', Vue3EasyDataTable);
app.mount('#app');
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vue3EasyDataTable from 'vue3-easy-data-table';
//import "bootstrap/dist/css/bootstrap.min.css"
import "bootswatch/dist/zephyr/bootstrap.min.css"
import "bootstrap-icons/font/bootstrap-icons.css";
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import "bootstrap"
import '@/assets/main.css'
import 'vue3-easy-data-table/dist/style.css';

const app = createApp(App);
app.use(router);
app.component('EasyDataTable', Vue3EasyDataTable);
app.mount('#app');
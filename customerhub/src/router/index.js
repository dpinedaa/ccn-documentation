import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddCustomer from '../views/AddCustomer.vue'
import CustomerList from '../views/CustomerList.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/add',
    name: 'add',
    component: AddCustomer
  },
  {
    path: '/list',
    name: 'list',
    component: CustomerList
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

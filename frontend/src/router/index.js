import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/pages/Login.vue';
import Tasks from '@/pages/Tasks.vue';

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/tasks',
        name: 'Tasks',
        component: Tasks,
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/login',
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
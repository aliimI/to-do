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
        meta: {requiresAuth: true},
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

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token');
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('login');
    } else {
        next();
    }
});

export default router;
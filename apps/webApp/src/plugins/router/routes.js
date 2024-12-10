export const routes = [
    { path: '/', redirect: '/dashboard' },

    {
        path: '/',
        component: () => import('@/layouts/default.vue'),
        children: [
            {
                path: 'dashboard',
                component: () => import('@/pages/dashboard.vue')
            },
            {
                path: 'dashboard/crm',
                component: () => import('@/pages/crm-submenu.vue')
            },
            {
                path: 'dashboard/ecommerce',
                component: () => import('@/pages/ecommerce-submenu.vue')
            },
            {
                path: 'dashboard/academy',
                component: () => import('@/pages/academy-submenu.vue')
            },
            {
                path: 'sentiments-data/popular-instructors',
                component: () => import('@/pages/popularInstructors-submenu.vue')
            }
        ]
    },

    {
        path: '/',
        component: () => import('@/layouts/default.vue'),
        children: [
            {
                path: 'Popular Instructor',
                component: () => import('@/pages/popularInstructors-submenu.vue')
            }
        ]
    },

    {
        path: '/',
        component: () => import('@/layouts/blank.vue'),
        children: [
            {
                path: 'login',
                component: () => import('@/pages/login.vue')
            },
            {
                path: 'register',
                component: () => import('@/pages/register.vue')
            },
            {
                path: '/:pathMatch(.*)*',
                component: () => import('@/pages/[...error].vue')
            }
        ]
    }
];

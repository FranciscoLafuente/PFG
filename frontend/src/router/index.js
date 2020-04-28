import Vue from "vue";
import VueRouter from "vue-router";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";

Vue.config.productionTip = false;

Vue.component("l-map", LMap);
Vue.component("l-tile-layer", LTileLayer);
Vue.component("l-marker", LMarker);

Vue.use(VueRouter);

const routes = [{
        path: "/",
        name: "home",
        component: () =>
            import ( /* webpackChunkName: "home" */ "../pages/Home.vue"),
        meta: {
            Auth: false,
            title: "Home",
        },
    },
    {
        path: "/search",
        name: "search",
        component: () =>
            import ( /* webpackChunkName: "Search" */ "../pages/Search.vue"),
        meta: {
            Auth: false,
            title: "Search",
        },
    },
    {
        path: "/myproject",
        name: "myproject",
        component: () =>
            import ( /* webpackChunkName: "Myproject" */ "../pages/Projects.vue"),
        meta: {
            Auth: true,
            title: "Myproject",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
    {
        path: "/myproject=:id",
        name: "scans",
        component: () =>
            import ( /* webpackChunkName: "Scans" */ "../pages/Scans.vue"),
        meta: {
            Auth: true,
            title: "Scans",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
    {
        path: "/myproject=:id/scan=:id_scan",
        name: "info-scan",
        component: () =>
            import ( /* webpackChunkName: "Info Scan" */ "../pages/InfoScan.vue"),
        meta: {
            Auth: true,
            title: "InfoScan",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
    {
        path: "/myproject=:id/scan=:id_scan/host=:ip/:index",
        name: "view_host",
        component: () =>
            import ( /* webpackChunkName: "View Host" */ "../pages/ViewScan2.vue"),
        meta: {
            Auth: true,
            title: "View Host",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
    {
        path: "/myproject=:id/scan=:id_scan/timeline/host=:ip",
        name: "time_line",
        component: () =>
            import ( /* webpackChunkName: "Time Line" */ "../pages/TimeLine.vue"),
        meta: {
            Auth: true,
            title: "Time Line",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
    {
        path: "/bots",
        name: "bots",
        component: () =>
            import ( /* webpackChunkName: "bots" */ "../pages/Bots.vue"),
        meta: {
            Auth: true,
            title: "Bots",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
    {
        path: "/signup",
        name: "signup",
        component: () =>
            import ( /* webpackChunkName: "signup" */ "../pages/Signup.vue"),
        meta: {
            Auth: false,
            title: "Signup",
        },
    },
    {
        path: "/login",
        name: "login",
        component: () =>
            import ( /* webpackChunkName: "login" */ "../pages/Login.vue"),
        meta: {
            Auth: false,
            title: "Login",
        },
        beforeEnter: (to, from, next) => {
            delete localStorage.token;
            next();
        },
    },
    {
        path: "/forgot",
        name: "forgot",
        component: () =>
            import ( /* webpackChunkName: "recover" */ "../pages/Forgot.vue"),
        meta: {
            Auth: false,
            title: "Forgot",
        },
    },
    {
        path: "/reset/:reset_token",
        name: "reset",
        component: () =>
            import ( /* webpackChunkName: "recover" */ "../pages/Reset.vue"),
        meta: {
            Auth: false,
            title: "Reset",
        },
    },
    {
        path: "/myprofile",
        name: "myprofile",
        component: () =>
            import ( /* webpackChunkName: "myproject" */ "../pages/Profile.vue"),
        meta: {
            Auth: true,
            title: "Myprofile",
        },
        beforeEnter: (to, from, next) => {
            if (!window.localStorage.getItem("access_token")) {
                next(false);
            } else {
                next();
            }
        },
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title;
    if (to.meta.Auth && !window.localStorage.getItem("access_token")) {
        next(false);
    } else {
        next();
    }
});

export default router;
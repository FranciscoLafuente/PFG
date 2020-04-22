import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import JwtService from "./jwt.service";
import { API_URL } from "./config";

const ApiService = {
    init() {
        Vue.use(VueAxios, axios);
        Vue.axios.defaults.baseURL = API_URL;
    },

    setHeader() {
        Vue.axios.defaults.headers.common[
            "Authorization"
        ] = `Bearer ${JwtService.getToken()}`;
    },

    query(resource) {
        return Vue.axios.get(resource).catch((error) => {
            throw new Error(`[RWV] ApiService ${error}`);
        });
    },

    get(resource, slug = "") {
        return Vue.axios.get(`${resource}/${slug}`).catch((error) => {
            throw new Error(`[RWV] ApiService ${error}`);
        });
    },

    post(resource, params) {
        return Vue.axios.post(`${resource}`, params);
    },

    update(resource, slug, params) {
        return Vue.axios.put(`${resource}/${slug}`, params);
    },

    put(resource) {
        return Vue.axios.put(`${resource}`);
    },

    delete(resource, params) {
        return Vue.axios.delete(resource, params).catch((error) => {
            throw new Error(`[RWV] ApiService ${error}`);
        });
    },
};

export default ApiService;

export const ProjectService = {
    get() {
        return ApiService.query("myproject");
    },
    getScans(slug) {
        return ApiService.get("myproject", slug);
    },
    create(params) {
        return ApiService.post("myproject", params);
    },
    remove(id) {
        return ApiService.delete(`myproject/${id}`);
    },
};

export const ScanService = {
    get(id) {
        return ApiService.get("myproject", id);
    },
    getInfo(id) {
        return ApiService.get("scan", id);
    },
    getAllInfo(domain) {
        return ApiService.get("scan/host=", domain);
    },
    create(id, payload) {
        console.log("en ScanService payload", payload);

        return ApiService.post(`myproject/${id}`, payload);
    },
    update(id) {
        return ApiService.put(`myproject/scan/${id}`);
    },
    delete(id_project, id_scan) {
        return ApiService.delete(`myproject/${id_project}/${id_scan}`);
    },
};

export const BotService = {
    get() {
        return ApiService.query("bots");
    },
    create(params) {
        return ApiService.post("bots", params);
    },
    remove(slug) {
        return ApiService.delete(`bots/${slug}`);
    },
    generateToken(slug) {
        return ApiService.query(`bots/${slug}`);
    },
    renewToken(id) {
        return ApiService.put(`bots/${id}`);
    },
};
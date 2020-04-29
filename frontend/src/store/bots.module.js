import { BotService } from "../common/api.service";
import { ADD_BOT, FETCH_START, FETCH_END, DEL_BOT } from "./mutations.type";
import {
    FETCH_BOTS,
    BOT_CREATE,
    BOT_DELETE,
    BOT_TOKEN,
    TOKEN_RELUNCH,
    BOT_UPLOAD,
} from "./actions.type";

const state = {
    listBots: [],
    isLoading: true,
};

const actions = {
    async [FETCH_BOTS]({ commit }) {
        commit(FETCH_START);
        return BotService.get()
            .then((r) => {
                commit(FETCH_END, r.data);
            })
            .catch((error) => {
                throw new Error(error);
            });
    },
    async [BOT_CREATE]({ commit }, params) {
        return BotService.create(params)
            .then((r) => {
                commit(ADD_BOT, r.data);
            })
            .catch((error) => {
                if (error.request.status === 400) {
                    throw new Error(error.response.data.msg);
                }
            });
    },
    async [BOT_DELETE]({ commit }, params) {
        return BotService.remove(params.id).then(() => {
            commit(DEL_BOT, params.index);
        });
    },
    async [BOT_TOKEN](context, id) {
        return BotService.generateToken(id);
    },
    [TOKEN_RELUNCH](context, id) {
        return BotService.renewToken(id);
    },
    [BOT_UPLOAD](context, params) {
        return BotService.addBot(params.name, params.file);
    },
};

const mutations = {
    [FETCH_START](state) {
        state.isLoading = true;
    },
    [FETCH_END](state, data) {
        state.listBots = data;
        state.isLoading = false;
    },
    [ADD_BOT](state, bot) {
        state.listBots = state.listBots.concat([bot]);
    },
    [DEL_BOT](state, index) {
        state.listBots.splice(index, 1);
    },
};

const getters = {
    bots(state) {
        return state.listBots;
    },
    name(state) {
        let names = [];
        state.listBots.forEach((element) => {
            names.push(element.name);
        });
        return names;
    },
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters,
};
import { createStore } from "vuex";

const store = createStore({
  state: {
    user: {
      email: "",
      hashedPassword: "",
    },
  },
  mutations: {
    setUser(state, payload) {
      state.user.email = payload.email;
      state.user.hashedPassword = payload.hashedPassword;
    },
  },
  actions: {
    loginUser({ commit }, userData) {
      commit("setUser", userData);
    },
  },
  getters: {
    userEmail: (state) => state.user.email,
    userHashedPassword: (state) => state.user.hashedPassword,
  },
});

export default store;

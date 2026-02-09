import { defineStore } from "pinia";
import axios from "axios";
import { API } from "@/utils/constants";

export const useUserStore = defineStore("user", {
  state: () => ({
    userCredentials: {
      username: "",
      password: "",
    },
    user: null,
    error: null,
    loading: false,
    isLoggedIn: null,
  }),
  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.post(
          API.USERS.post_login,
          { username, password },
          { withCredentials: true }, // <-- important for cookies!
        );
        this.user = response.data.user;
        if (response.data.user) {
          this.isLoggedIn = true;

          // Fetch filters
          //   const siteSettingsStore = useSiteSettingsStore();
          //   await siteSettingsStore.fetchFilters();
        }
      } catch (err) {
        this.error =
          err.response?.data?.detail ||
          "Unauthorized account or invalid credentials. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    async checkAuth() {
      try {
        const response = await axios.get(API.USERS.get_me, {
          withCredentials: true, // <-- important for cookies!
        });
        this.isLoggedIn = true;
        this.user = response.data.user;
      } catch (err) {
        this.isLoggedIn = false;
        this.user = null;
        console.log(
          err.response?.data?.detail || "Authentication check failed",
        );
      }
    },
  },
});

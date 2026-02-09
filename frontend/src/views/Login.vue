<template>
    <div class="login-page d-flex justify-content-center align-items-center">
        <div class="login-card">
            <div class="card border-0 shadow text-center">
                <div class="card-body p-3 p-sm-4 p-md-5">

                    <h1 class="h5 h4-sm h3-md fw-normal mb-4 text-secondary">
                        <i class="bi bi-flask fs-2 me-3"></i>
                        myRequests
                    </h1>

                    <form autocomplete="off" @submit.prevent="handleLogin">


                        <!-- Error -->
                        <div class="alert alert-warning py-2" role="alert" v-if="displayError">
                            {{ displayError }}
                        </div>

                        <!-- Username -->
                        <div class="form-floating mb-2">
                            <input v-model="userCredentials.username" type="text" class="form-control form-control-lg"
                                id="floatingInput" placeholder="Username" autofocus />
                            <label for="floatingInput">Username</label>
                        </div>

                        <!-- Password -->
                        <div class="form-floating mb-2">
                            <input v-model="userCredentials.password" type="password"
                                class="form-control form-control-lg" id="floatingPassword" placeholder="Password" />
                            <label for="floatingPassword">Password</label>
                        </div>

                        <!-- Remember me -->
                        <div class="form-check text-start my-3">
                            <input class="form-check-input" type="checkbox" id="rememberMe" />
                            <label class="form-check-label" for="rememberMe">
                                Remember me
                            </label>
                        </div>

                        <!-- Submit -->
                        <button class="w-100 btn btn-lg btn-outline-primary" type="submit"
                            :disabled="userStore.loading">
                            <span v-if="!userStore.loading">Sign in</span>
                            <span v-else class="spinner-border spinner-border-sm"></span>
                        </button>
                    </form>
                </div>

                <!-- Footer -->
                <div class="card-footer border-0 bg-white py-3">
                    <div class="small text-muted text-primary">
                        &copy; {{ new Date().getFullYear() }} {{ appTitle }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { mapStores } from 'pinia'
import { toast } from 'vue3-toastify';

export default {
    name: 'Login',
    data() {
        return {
            userCredentials: {
                username: '',
                password: ''
            },
            displayError: '',
            appTitle: process.env.VUE_APP_APP_TITLE
        }
    },
    computed: {
        ...mapStores(useUserStore)
    },
    methods: {
        async handleLogin() {
            this.displayError = ''

            await this.userStore.login(
                this.userCredentials.username,
                this.userCredentials.password
            )

            if (this.userStore.isLoggedIn) {
                this.$router.push({ path: '/' })
            }

            if (this.userStore.error) {
                this.displayError = Array.isArray(this.userStore.error)
                    ? 'Password is less than 8 characters.'
                    : this.userStore.error || 'Login failed. Please try again.'
                toast.error(this.displayError)
            }
        }
    }
}
</script>

<style scoped>
.login-page {
    width: 100%;
    min-height: 100vh;
    min-height: 100dvh;
    /* mobile-safe viewport */
    padding: 1rem;
}

.login-card {
    width: 100%;
    max-width: 420px;
}

.card {
    border-radius: 0.75rem;
}

button:disabled {
    cursor: not-allowed;
}
</style>

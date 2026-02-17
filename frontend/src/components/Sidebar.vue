<template>
    <nav class="col-md-3 col-lg-2 d-md-block bg-body-tertiary sidebar offcanvas-md offcanvas-end" tabindex="-1"
        id="sidebarMenu" aria-labelledby="sidebarMenuLabel">
        <!-- Offcanvas header only for mobile -->
        <div class="offcanvas-header d-md-none">
            <h5 class="offcanvas-title" id="sidebarMenuLabel">{{ appName }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" data-bs-target="#sidebarMenu"
                aria-label="Close"></button>
        </div>
        <div class="offcanvas-body d-md-flex flex-column p-0 pt-lg-3 overflow-y-auto">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <RouterLink to="/" class="nav-link d-flex align-items-center gap-2" active-class="active" href="#">
                        <i class="bi bi-house" aria-hidden="true"></i>
                        Dashboard
                    </RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/requests" class="nav-link d-flex align-items-center gap-2" active-class="active"
                        href="#"> <i class="bi bi-file-earmark" aria-hidden="true"></i>
                        Requests
                    </RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/stickers" class="nav-link d-flex align-items-center gap-2" active-class="active"
                        href="#">
                        <i class="bi bi-stickies" aria-hidden="true"></i>
                        Stickers
                    </RouterLink>
                </li>
            </ul>
            <h6
                class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-body-secondary text-uppercase">
                <span>Master Data</span>
                <button class="btn btn-link p-0 text-dark" type="button" data-bs-toggle="collapse"
                    data-bs-target="#masterDataPageGroup" aria-expanded="true" aria-controls="masterDataPageGroup">
                    <i class="bi bi-plus-circle"></i>
                </button>
            </h6>
            <ul class="nav flex-column collapse show" id="masterDataPageGroup">
                <li class="nav-item">
                    <RouterLink to="/master-data/customer" class="nav-link d-flex align-items-center gap-2"
                        active-class="active">
                        <i class="bi bi-person" aria-hidden="true"></i>
                        Customer
                    </RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/master-data/area" class="nav-link d-flex align-items-center gap-2"
                        active-class="active">
                        <i class="bi bi-person-workspace" aria-hidden="true"></i>
                        Area
                    </RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/master-data/salesperson" class="nav-link d-flex align-items-center gap-2"
                        active-class="active">
                        <i class="bi bi-person-badge" aria-hidden="true"></i>
                        SalesPerson
                    </RouterLink>
                </li>

            </ul>
            <hr class="my-3">
            <ul class="nav flex-column mb-auto">
                <li class="nav-item"> <a class="nav-link d-flex align-items-center gap-2" href="#"> <i
                            class="bi bi-gear" aria-hidden="true"></i>
                        Settings
                    </a> </li>
                <li @click.prevent="logout" class="nav-item"> <a class="nav-link d-flex align-items-center gap-2"
                        href="/">
                        <i class="bi bi-door-closed" aria-hidden="true"></i>
                        Sign out
                    </a> </li>
            </ul>
        </div>
    </nav>
</template>
<script>
import { API } from '@/utils/constants';
import { RouterLink } from 'vue-router';
export default {
    name: 'Sidebar',
    methods: {
        async logout() {
            try {
                await fetch(API.USERS.post_logout, {
                    method: "POST",
                    credentials: "include"
                });
                this.$router.push("/login");
            } catch (err) {
                console.error("Logout failed", err);
            }
        }
    },
    data() {
        return {
            appName: process.env.VUE_APP_APP_TITLE
        }
    }
};
</script>
<style scoped>
a {
    color: #293630;
}

.active {
    /* color: #049679 !important; */
    text-shadow: h-shadow v-shadow blur-radius color;
    font-weight: bold !important;
}

.bi {
    display: inline-block;
    width: 1rem;
    height: 1rem;
}

/*
 * Sidebar
 */
.sidebar {
    min-height: 100vh
}

.sidebar hr {
    margin-left: 0;
    margin-right: 0;
}
</style>
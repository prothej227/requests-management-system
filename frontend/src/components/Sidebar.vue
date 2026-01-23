<template>
    <div class="sidebar border border-right col-md-3 col-lg-2 p-0 bg-body-tertiary">
        <div class="offcanvas-md offcanvas-end bg-body-tertiary" tabindex="-1" id="sidebarMenu"
            aria-labelledby="sidebarMenuLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="sidebarMenuLabel">Company name</h5> <button type="button"
                    class="btn-close" data-bs-dismiss="offcanvas" data-bs-target="#sidebarMenu"
                    aria-label="Close"></button>
            </div>
            <div class="offcanvas-body d-md-flex flex-column p-0 pt-lg-3 overflow-y-auto">
                <ul ul class="nav flex-column">
                    <li class="nav-item">
                        <a class="nav-link d-flex align-items-center gap-2 active" aria-current="page" href="#">
                            <i class="bi bi-house-fill" aria-hidden="true"></i>
                            Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link d-flex align-items-center gap-2" href="#"> <i class="bi bi-file-earmark"
                                aria-hidden="true"></i>
                            Requests
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link d-flex align-items-center gap-2" href="#">
                            <i class="bi bi-stickies" aria-hidden="true"></i>
                            Stickers
                        </a>
                    </li>
                </ul>
                <h6
                    class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-body-secondary text-uppercase">
                    <span>Master Data</span>
                    <a class="link-secondary" href="#" aria-label="Add a new report">
                        <i class="bi bi-plus-circle" aria-hidden="true">
                        </i>
                    </a>
                </h6>
                <ul class="nav flex-column mb-auto">
                    <li class="nav-item"> <a class="nav-link d-flex align-items-center gap-2" href="#">
                            <i class="bi bi-file-earmark-text" aria-hidden="true"></i>
                            Customer
                        </a>
                    </li>
                    <li class="nav-item"> <a class="nav-link d-flex align-items-center gap-2" href="#">
                            <i class="bi bi-file-earmark-text" aria-hidden="true"></i>
                            Area
                        </a>
                    </li>

                </ul>
                <hr class="my-3">
                <ul class="nav flex-column mb-auto">
                    <li class="nav-item"> <a class="nav-link d-flex align-items-center gap-2" href="#"> <i
                                class="bi bi-gear" aria-hidden="true"></i>
                            Settings
                        </a> </li>
                    <li class="nav-item"> <a class="nav-link d-flex align-items-center gap-2" href="#"> <i
                                class="bi bi-door-closed" aria-hidden="true"></i>
                            Sign out
                        </a> </li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
import { RouterLink } from 'vue-router';
export default {
    name: 'Sidebar',
};
</script>
<style scoped>
a {
    color: #293630;
}

.sidebar {
    position: fixed;
    top: 3em;
    /* Height of TopHeader */
    bottom: 0;
    left: 0;
    z-index: 100;
    padding: 0;
    /* Remove top padding since top is now set */
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
    height: calc(100% - 3em);
    /* Ensure sidebar doesn't overflow */
}
</style>
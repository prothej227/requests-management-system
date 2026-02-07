<template>
    <div class="col-sm-6 col-lg-3">
        <div class="card shadow-sm">
            <div class="card-body">
                <div class="d-flex align-items-center justify-content-between">
                    <div>
                        <div :class="`text-muted small`">{{ label }}</div>
                        <div :class="`fs-4 fw-semibold`">{{ value }}</div>
                    </div>

                    <div class="kpi-icon px-4">
                        <i :class="`bi ${icon} text-${variant} fs-2`"></i>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "KPICard",
    props: {
        label: {
            type: String,
            default: "Unknown"
        },
        value: {
            type: Number,
            default: 0
        },
        icon: {
            type: String,
            default: "bi bi-stickies"
        },
        iconColor: {
            type: String,
            default: "text-success"
        },
        variant: {
            type: String,
            default: 'primary'
        }
    }
}
</script>
<style scoped>
.kpi-icon {
    display: flex;
    align-items: center;
    justify-content: center;
}

.kpi-icon i {
    font-size: 2rem;
    line-height: 1;
}
</style>
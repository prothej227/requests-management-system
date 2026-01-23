<template>
    <div class="btn-group my-3 gap-1">
        <button v-if="visibility.create" @click="onCreate" class="btn btn-sm btn-outline-primary">
            <i class="bi bi-plus-circle"></i>
            Create
        </button>
        <button v-if="visibility.refresh" @click="$emit('refresh')" class="btn btn-sm btn-outline-success">
            <i class="bi bi-arrow-clockwise"></i>
            Refresh
        </button>
        <button v-if="visibility.import" @click="onImport" class="btn btn-sm btn-outline-secondary">
            <i class="bi bi-file-earmark-arrow-up"></i>
            Import
        </button>
        <button v-if="visibility.export" @click="onExport" class="btn btn-sm btn-outline-secondary">
            <i class="bi bi-file-earmark-arrow-down"></i>
            Export
        </button>
    </div>
</template>

<script>
export default {
    name: "ActionButton",
    props: {
        onCreate: {
            type: Function
        },
        onImport: {
            type: Function,
            default: () => { }
        },
        onExport: {
            type: Function,
            default: () => { }
        },
        visibility: {
            type: Object,
            default: () => ({
                create: true,
                refresh: true,
                import: true,
                export: true
            })
        }
    },
    setup() {
        return {}
    }
}
</script>

<style lang="scss" scoped></style>
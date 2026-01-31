<template>
    <form @submit.prevent="submitForm">
        <ActionButton :visibility="actionButtonEnabledConfig.visibility" @refresh="fetchRequests" />
        <EasyDataTable v-model:server-options="serverOptions" :headers="headers" :items="items"
            :key="serverOptions.page" :server-items-length="serverItemsLength" :loading="isDataTableLoading"
            :theme-color="'#007bff'" buttons-pagination border-cell alternating @click-row="onRowClick">
        </EasyDataTable>
        <hr>
        <span class="fw-bold my-1">Selected Requests for Sticker Canvas:</span>
        <EasyDataTable v-model:items="selectedRequestsTable.items" :headers="selectedRequestsTable.headers"
            rows-per-page="5" :theme-color="'#28a745'" border-cell alternating>
            <template #item-actions="{ rowNumber }">
                <button class="btn btn-sm btn-danger" @click.prevent="removeSelectedRequestRow(rowNumber)">
                    <i class="bi bi-trash"></i>
                </button>
            </template>
        </EasyDataTable>
    </form>
</template>

<script>
import axios from 'axios';
import ActionButton from '@/components/ActionButton.vue';
import { TableHeaders, API } from '@/utils/constants';
import { computed } from 'vue';

let nextRowNumber = 0;

export default {
    name: 'CreateStickerCanvasForm',
    components: {
        ActionButton,
        EasyDataTable: window['vue3-easy-data-table'],
    },
    data() {
        return {
            selectedRequestsTable: {
                headers: TableHeaders.STICKERS.selectedRequestsTable,
                items: []
            },
            items: [],
            headers: TableHeaders.REQUESTS,
            serverOptions: {
                page: 1,
                rowsPerPage: 5,
                sortBy: '',
                sortType: '',
                filters: {},
            },
            serverItemsLength: 0,
            isDataTableLoading: false,
            actionButtonEnabledConfig: {
                visibility: {
                    create: false,
                    refresh: true
                }
            }
        };
    },
    mounted() {
        this.fetchRequests();
    },
    computed: {
        stickers() {
            return this.selectedRequestsTable.items.map(row => ({
                request_id: row.id
            }));
        }
    },
    methods: {
        async submitForm() {
            try {
                const payload = { stickers: this.stickers }
                const response = await axios.post(`${API.STICKERS['create']}`, payload, { withCredentials: true });
                if (response.status === 200) {
                    toast.success("Record created successfully.")
                    this.$emit('request-created', response.data);
                }
            } catch (error) {
                console.error('Error creating request:', error);
            }
        },
        async fetchRequests() {
            this.isDataTableLoading = true;
            try {
                // Calculate start_index and batch_size
                const batch_size = this.serverOptions.rowsPerPage || 30;
                const start_index = ((this.serverOptions.page || 1) - 1) * batch_size;
                // Build query params
                const params = new URLSearchParams({
                    batch_size: batch_size,
                    start_index: start_index,
                });
                // Optionally add filters
                if (this.serverOptions.filters) {
                    Object.entries(this.serverOptions.filters).forEach(([key, value]) => {
                        if (value) params.append(key, value);
                    });
                }
                const url = `${API.REQUESTS['list']}?${params.toString()}`;
                const response = await axios.get(url);
                const data = response.data;
                // Expecting data.items and data.total
                this.items = data.records || [];
                this.serverItemsLength = data.total_count || 0;
            } catch (error) {
                this.items = [];
                this.serverItemsLength = 0;
                toast.error('Error fetching requests data.');
                // Optionally show error notification
            } finally {
                this.isDataTableLoading = false;
            }
        },
        async onRowClick(row) {
            this.selectedRequestsTable.items.push({
                ...row,
                rowNumber: nextRowNumber++

            })
        },
        async removeSelectedRequestRow(rowNumber) {
            this.selectedRequestsTable.items = this.selectedRequestsTable.items.filter(item => item.rowNumber !== rowNumber);
        },
    },
}
</script>

<style>
.vue3-easy-data-table__body tr {
    transition: all 0.25s ease;
}

.vue3-easy-data-table__body tr.v-enter-from {
    opacity: 0;
    transform: translateY(8px);
}

.vue3-easy-data-table__body tr.v-enter-to {
    opacity: 1;
    transform: translateY(0);
}

.vue3-easy-data-table__body tr.v-leave-from {
    opacity: 1;
    transform: translateY(0);
}

.vue3-easy-data-table__body tr.v-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}
</style>
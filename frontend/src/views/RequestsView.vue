<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 border-bottom">
        <h1 class="h4 d-flex">
            <i class="bi bi-file-earmark me-3"></i>
            Requests
        </h1>
    </div>
    <ActionButton :visibility="actionButtonEnabledConfig.visibility" :onCreate="showCreateRequestModal"
        @refresh="fetchRequests" />
    <EasyDataTable v-model:server-options="serverOptions" :headers="headers" :items="items" :key="serverOptions.page"
        :server-items-length="serverItemsLength" :loading="isDataTableLoading" :theme-color="'#007bff'"
        buttons-pagination border-cell alternating>
    </EasyDataTable>
    <Modal ref="createRequest" title="Create Request" biHeaderIcon="bi bi-plus-circle">
        <template #body>
            <CreateRequestsForm ref="createRequestForm" />
        </template>
        <template #footer>
            <button class="btn btn-primary" @click="submitCreateForm">
                <i class="bi bi-arrow-return-right"></i>
                Submit
            </button>
        </template>
    </Modal>
</template>
<script>


import { TableHeaders, API } from '@/utils/constants';
import ActionButton from '@/components/ActionButton.vue';
import CreateRequestsForm from '@/components/forms/CreateRequestsForm.vue';
import axios from 'axios';
import Modal from '@/components/Modal.vue';
import { toast } from 'vue3-toastify';

export default {
    name: 'RequestsView',
    components: {
        EasyDataTable: window['vue3-easy-data-table'],
        ActionButton,
        Modal,
        CreateRequestsForm
    },
    data() {
        return {
            items: [],
            headers: TableHeaders.REQUESTS,
            serverOptions: {
                page: 1,
                rowsPerPage: 30,
                sortBy: '',
                sortType: '',
                filters: {},
            },
            serverItemsLength: 0,
            isDataTableLoading: false,
            actionButtonEnabledConfig: {
                visibility: {
                    create: true,
                    refresh: true
                }
            }
        };
    },
    watch: {
        serverOptions: {
            handler: 'fetchRequests',
            deep: true,
        },
    },
    mounted() {
        this.fetchRequests();
    },
    methods: {
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
        async showCreateRequestModal() {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            const currentDate = `${yyyy}-${mm}-${dd}`;
            if (this.$refs.createRequestForm) {
                this.$refs.createRequestForm.requestForm = {
                    date_received: '',
                    customer_id: '',
                    area_id: '',
                    long_description: '',
                    short_description: '',
                    sales_person_id: '',
                    status: 'Not Started',
                    feedback: 'N/A',
                    quantity: '',
                    lpo_no: '',
                };
            }
            if (this.$refs.createRequest && typeof this.$refs.createRequest.show === 'function') {
                this.$refs.createRequest.show();
            }
        },
        async submitCreateForm() {
            if (this.$refs.createRequestForm && typeof this.$refs.createRequestForm.submitForm === 'function') {
                try {
                    await this.$refs.createRequestForm.submitForm();
                    if (this.$refs.createRequest && typeof this.$refs.createRequest.hide === 'function') {
                        this.$refs.createRequest.hide();
                    }
                    this.fetchRequests();
                } catch (error) {
                    console.error('Error submitting create request form:', error);
                }
            }
        },
    },
}
</script>
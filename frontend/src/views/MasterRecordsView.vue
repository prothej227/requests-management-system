<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 border-bottom">
        <h1 class="h4 d-flex">
            <i :class="`bi bi-${recordName === 'customer' ? 'person' : 'person-workspace'} me-3`"></i>
            {{ toProperCase(recordName) }}
        </h1>
    </div>
    <div v-if="isValidRecord">
        <ActionButton :visibility="actionButtonEnabledConfig.visibility" :onCreate="showCreateMasterRecordModal"
            @refresh="fetchRequests(tableListUrl)" />
        <EasyDataTable v-model:server-options="serverOptions" :headers="headers" :items="items"
            :key="serverOptions.page" :server-items-length="serverItemsLength" :loading="isDataTableLoading"
            :theme-color="'#007bff'" buttons-pagination border-cell alternating>
        </EasyDataTable>
        <Modal ref="createMasterRecordModal" :title="`Create ${toProperCase(recordName)}`"
            biHeaderIcon="bi bi-plus-circle">
            <template #body>
                <CreateCustomerForm v-if="recordName === 'customer'" ref="createCustomerForm"
                    @customer-created="fetchRequests(tableListUrl)" />
                <CreateAreaForm v-else-if="recordName === 'area'" ref="createAreaForm"
                    @area-created="fetchRequests(tableListUrl)" />
                <CreateSalesPersonForm v-else-if="recordName === 'salesperson'" ref="createSalesPersonForm"
                    @salesperson-created="fetchRequests(tableListUrl)" />
            </template>
            <template #footer>
                <button class="btn btn-primary" @click="submitCreateForm">
                    <i class="bi bi-arrow-return-right"></i>
                    Submit
                </button>
            </template>
        </Modal>
    </div>
    <div v-else>
        <h3 class="mt-4">Not Found Error</h3>
        <p>The record "{{ recordName }}" is not recognized.</p>
    </div>

</template>
<script>
import { toProperCase } from '@/utils/helpers';
import { TableHeaders } from '@/utils/constants';
import { API } from '@/utils/constants';
import ActionButton from '@/components/ActionButton.vue';
import axios from 'axios';
import Modal from '@/components/Modal.vue';
import CreateCustomerForm from '@/components/forms/CreateCustomerForm.vue';
import CreateAreaForm from '@/components/forms/CreateAreaForm.vue';
import CreateSalesPersonForm from '@/components/forms/CreeateSalesPersonForm.vue';
import { toast } from 'vue3-toastify';

export default {
    name: 'MasterRecordsView',
    components: {
        EasyDataTable: window['vue3-easy-data-table'],
        ActionButton,
        Modal,
        CreateCustomerForm,
        CreateAreaForm,
        CreateSalesPersonForm
    },
    data() {
        return {
            items: [],
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
    computed: {
        recordName() {
            return this.$route.params.record_name;
        },
        isValidRecord() {
            return ['customer', 'area', 'salesperson'].includes(this.recordName);
        },
        headers() {
            return TableHeaders.MASTER[this.recordName] || [];
        },
        tableListUrl() {
            return API.MASTER[this.recordName]['list'];
        }
    },
    watch: {
        async recordName(newVal, oldVal) {
            if (this.isValidRecord) {
                this.serverOptions = {
                    page: 1,
                    rowsPerPage: 30,
                    sortBy: '',
                    sortType: '',
                    filters: {},
                };
                await this.fetchRequests(this.tableListUrl);
            }
        }
    },
    mounted() {
        if (this.isValidRecord) {
            this.fetchRequests(this.tableListUrl);
        }
    },
    methods: {
        async fetchRequests(url) {
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
                const response = await axios.get(url + `?${params.toString()}`);
                const data = response.data;
                // Expecting data.items and data.total
                this.items = data.records || [];
                this.serverItemsLength = data.total_count || 0;
            } catch (error) {
                toast.error("Error encountered while fetching data", error);
                this.items = [];
                this.serverItemsLength = 0;
                // Optionally show error notification
            } finally {
                this.isDataTableLoading = false;
            }
        },
        async showCreateMasterRecordModal() {
            if (this.recordName === 'customer') {
                this.$.refs.createCustomerForm.customerForm = {
                    'name': ''
                }
                this.$refs.createMasterRecordModal.show();
            } else if (this.recordName === 'area') {
                this.$.refs.createAreaForm.areaForm = {
                    'name': ''
                }
            } else if (this.recordName === 'salesperson') {
                this.$.refs.createSalesPersonForm.salesPersonForm = {
                    'first_name': '',
                    'last_name': ''
                }
            }

            this.$refs.createMasterRecordModal.show();
        },
        async submitCreateForm() {
            if (this.recordName === 'customer') {
                try {
                    await this.$refs.createCustomerForm.submitForm();
                } catch (error) {
                    toast.error('Error submitting customer form:', error);
                }

            } else if (this.recordName === 'area') {
                try {
                    await this.$refs.createAreaForm.submitForm();
                } catch (error) {
                    toast.error('Error submitting area form:', error);
                }
            } else if (this.recordName === 'salesperson') {
                try {
                    await this.$refs.createSalesPersonForm.submitForm();
                } catch (error) {
                    toast.error('Error submitting salesperson form:', error);
                }
            }
            toast.success("Record created successfully.")
            this.$refs.createMasterRecordModal.hide();
        },
        toProperCase
    }

}
</script>
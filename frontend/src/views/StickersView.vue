<template>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 border-bottom">
        <h1 class="h4 d-flex">
            <i class="bi bi-stickies me-3"></i>
            Stickers
        </h1>
    </div>
    <ActionButton :visibility="actionButtonEnabledConfig.visibility" :onCreate="showCreateStickerCanvasModal"
        @refresh="fetchRequests" />
    <EasyDataTable v-model:server-options="serverOptions" :headers="headers" :items="items" :key="serverOptions.page"
        :server-items-length="serverItemsLength" :loading="isDataTableLoading" :theme-color="'#18bc9c'"
        buttons-pagination border-cell alternating>
        <template #header-status="header">
            <div class="d-flex justify-content-center align-items-center w-100 h-100">
                <span>{{ header.text }}</span>
            </div>
        </template>
        <template #item-actions="{ id }">
            <div class="d-flex align-items-center justify-items-center">
                <button type="button" class="btn btn-outline-primary btn-sm me-1" @click="generateStickerCanvas(id)">
                    <template v-if="loadingItemIds.has(id)">
                        <span class="spinner-border spinner-border-sm" role="status"></span>
                    </template>
                    <template v-else>
                        <i class="bi bi-file-earmark-plus-fill"></i>
                    </template>
                </button>
                <button type="button" disabled class="btn btn-outline-secondary btn-sm">
                    <i class="bi bi-eye-fill"></i>
                </button>
            </div>
        </template>
        <template #item-status="{ document_id }">
            <div class="d-flex justify-content-center align-items-center w-100 h-100">
                <span :class="`badge rounded-0 text-bg-${document_id ? 'success' : 'secondary'}`">
                    {{ document_id ? 'AVAILABLE' : 'N/A' }}
                </span>
            </div>
        </template>
        <template #item-document_id="{ document_id }">
            <span>
                {{ document_id === null || document_id === undefined ? "-" : document_id }}
            </span>
        </template>
        <template #item-get="{ document_id, id }">
            <button type="button" class="btn btn-outline-danger btn-sm rounded-0" :disabled="!document_id"
                @click="downloadStickerCanvas(id)">
                <i class="bi bi-file-pdf-fill"></i>
                GET
            </button>
        </template>
        <template #item-created_on="{ created_on }">
            {{ timeFormatter(created_on) }}
        </template>
    </EasyDataTable>
    <Modal ref="createStickerCanvas" title="Create Sticker Canvas" biHeaderIcon="bi bi-plus-circle" size="xl">
        <template #body>
            <CreateStickerCanvasForm ref="createStickerCanvasForm" />
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
import CreateStickerCanvasForm from '@/components/forms/CreateStickerCanvasForm.vue';
import axios from 'axios';
import Modal from '@/components/Modal.vue';
import { toast } from 'vue3-toastify';

export default {
    name: 'StickersView',
    components: {
        EasyDataTable: window['vue3-easy-data-table'],
        ActionButton,
        Modal,
        CreateStickerCanvasForm
    },
    data() {
        return {
            items: [],
            headers: TableHeaders.STICKERS.canvas,
            serverOptions: {
                page: 1,
                rowsPerPage: 15,
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
            },
            loadingItemIds: new Set(),
            stickerDownloadBaseUrl: API.STICKERS.sticker_download_base_url
        };
    },
    mounted() {
        this.fetchRequests();
    },
    watch: {
        serverOptions: {
            handler(newOptions) {
                this.fetchRequests();
            },
            deep: true
        }
    },
    methods: {
        async fetchRequests() {
            this.isDataTableLoading = true;
            try {

                // Calculate start_index and batch_size
                const batch_size = this.serverOptions.rowsPerPage || 15;
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
                const url = `${API.STICKERS['list']}?${params.toString()}`;
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
        async showCreateStickerCanvasModal() {
            if (this.$refs.createStickerCanvasForm) {
                this.$refs.createStickerCanvasForm.selectedRequestsTable = {
                    headers: TableHeaders.STICKERS.selectedRequestsTable,
                    items: []
                };
            }
            if (this.$refs.createStickerCanvas && typeof this.$refs.createStickerCanvas.show === 'function') {
                this.$refs.createStickerCanvas.show();
            }
        },
        async submitCreateForm() {
            if (this.$refs.createStickerCanvasForm && typeof this.$refs.createStickerCanvasForm.submitForm === 'function') {
                try {
                    await this.$refs.createStickerCanvasForm.submitForm();
                    if (this.$refs.createStickerCanvas && typeof this.$refs.createStickerCanvas.hide === 'function') {
                        this.$refs.createStickerCanvas.hide();
                    }
                    this.fetchRequests();
                } catch (error) {
                    console.error('Error submitting create request form:', error);
                }
            }
        },
        async generateStickerCanvas(id) {
            if (this.loadingItemIds.has(id)) return

            this.loadingItemIds.add(id)

            try {
                await new Promise(resolve => setTimeout(resolve, 2000));
                const params = new URLSearchParams({
                    sticker_canvas_id: id,
                    preview_only: false,
                })
                const url = `${API.STICKERS['generate_sticker_canvas']}?${params.toString()}`;
                const response = await axios.post(url);
                if (response.status === 200) {
                    toast.success("Sticker canvas successfully generated.")
                    this.fetchRequests()
                }
            } catch (err) {
                if ([422, 400].includes(err?.response?.status)) {
                    toast.error(err?.response?.data.detail)
                }
            } finally {
                this.loadingItemIds.delete(id)
            }

        },
        timeFormatter(timeString) {
            const dateObj = new Date(timeString)
            return dateObj.toLocaleString('en-PH', {
                timeZone: 'Asia/Manila'
            })
        },
        downloadStickerCanvas(id) {
            window.open(`${this.stickerDownloadBaseUrl}/${id}`, "_blank")
        }
    }
}
</script>
<template>
    <Modal ref="deleteRecord" title="Confirmation" biHeaderIcon="bi bi-trash">
        <template #body>
            Are you sure you want delete this record? Record ID = {{ this.idToDelete }}
        </template>
        <template #footer>
            <button class="btn btn-primary" @click.prevent="submitDeleteRequest">
                <i class="bi bi-arrow-return-right"></i>
                OK
            </button>
        </template>
    </Modal>
</template>

<script>
import Modal from './Modal.vue'
import axios from 'axios'

export default {
    name: "DeleteDialog",
    components: { Modal },

    emits: ['delete:success', 'delete:error'],

    props: {
        idToDelete: Number,
        deleteEndpointUrl: String,
        extraRequestParams: Object
    },

    methods: {
        showDeleteConfirmation() {
            this.$refs.deleteRecord?.show()
        },

        async submitDeleteRequest() {
            try {
                const response = await axios.delete(`${this.deleteEndpointUrl}${this.idToDelete}`, {
                    params: this.extraRequestParams
                });

                if (response.status === 200) {
                    this.$emit('delete:success', this.idToDelete)
                }
            } catch (error) {
                this.$emit('delete:error', {
                    id: this.idToDelete,
                    error
                })
            } finally {
                this.$refs.deleteRecord.hide()
            }
        }
    }
}
</script>

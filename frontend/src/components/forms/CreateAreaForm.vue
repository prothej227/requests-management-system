<template>
    <form @submit.prevent="submitForm">
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="shortDescription">Area Name</label>
            <div class="col-md-8 col-12">
                <input type="text" class="form-control" id="shortDescription" v-model="areaForm.name"
                    placeholder="Area Name">
            </div>
        </div>
        <div class="form-group row mb-3">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12">
                Logo
            </label>
            <div class="col-md-8 col-12">
                <input type="file" class="form-control" accept="image/*" :disabled="isLogoProcessing"
                    @change="onLogoChange" />

                <!-- Spinner -->
                <div v-if="isLogoProcessing" class="mt-2 d-flex align-items-center">
                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                    <span class="text-muted">Processing image…</span>
                </div>

                <!-- Preview -->
                <div v-if="logoPreview && !isLogoProcessing" class="mt-2">
                    <img :src="logoPreview" alt="Logo Preview" class="img-thumbnail p-1" style="max-height: 150px;" />
                </div>
            </div>
        </div>
    </form>
</template>

<script>
import axios from 'axios';
import { API } from '@/utils/constants';
import { toast } from 'vue3-toastify';

export default {
    name: 'CreateAreaForm',
    data() {
        return {
            areaForm: {
                'name': '',
                'logo': ''
            },
            logoPreview: null,
            isLogoProcessing: false
        };
    },
    mounted() { },
    computed: {
        logoPreview() {
            return this.areaForm.logo
        }
    },
    methods: {
        async submitForm() {
            try {
                const response = await axios.post(`${API.MASTER.area['create']}`, this.areaForm, { withCredentials: true });
                if (response.status === 200) {
                    this.$emit('area-created', response.data);
                }
            } catch (error) {
                console.error('Error creating area:', error);
            }
        },
        async onLogoChange(event) {
            const file = event.target.files[0]
            if (!file) return

            if (!file.type.startsWith('image/')) {
                toast.error('Please upload a valid image file')
                event.target.value = null
                return
            }

            this.isLogoProcessing = true

            try {
                await new Promise(resolve => setTimeout(resolve, 2000));
                const base64 = await this.readFileAsBase64(file)
                this.areaForm.logo = base64
            } catch (err) {
                toast.error('Failed to process image')
            } finally {
                this.isLogoProcessing = false
            }
        },

        async readFileAsBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader()
                reader.onload = () => resolve(reader.result)
                reader.onerror = reject
                reader.readAsDataURL(file)
            })
        },
    },
}
</script>

<style lang="scss" scoped></style>
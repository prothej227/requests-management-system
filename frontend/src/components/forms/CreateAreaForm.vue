<template>
    <form @submit.prevent="submitForm">
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="shortDescription">Area Name</label>
            <div class="col-md-8 col-12">
                <input type="text" class="form-control" id="shortDescription" v-model="areaForm.name"
                    placeholder="Area Name">
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
                'name': ''
            }
        };
    },
    mounted() { },
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
        }
    },
}
</script>

<style lang="scss" scoped></style>
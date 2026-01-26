<template>
    <form @submit.prevent="submitForm">
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="shortDescription">First Name</label>
            <div class="col-md-8 col-12">
                <input type="text" class="form-control" id="shortDescription" v-model="salesPersonForm.first_name"
                    placeholder="First Name">
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="shortDescription">Last Name</label>
            <div class="col-md-8 col-12">
                <input type="text" class="form-control" id="shortDescription" v-model="salesPersonForm.last_name"
                    placeholder="Last Name">
            </div>
        </div>
    </form>
</template>

<script>
import axios from 'axios';
import { API } from '@/utils/constants';
import { toast } from 'vue3-toastify';

export default {
    name: 'CreateSalesPersonForm',
    data() {
        return {
            salesPersonForm: {
                'first_name': '',
                'last_name': ''
            }
        };
    },
    mounted() { },
    methods: {
        async submitForm() {
            try {
                const response = await axios.post(`${API.MASTER.salesperson['create']}`, this.salesPersonForm, { withCredentials: true });
                if (response.status === 200) {
                    this.$emit('salesperson-created', response.data);
                }
            } catch (error) {
                console.error('Error creating salesperson:', error);
            }
        }
    },
}
</script>

<style lang="scss" scoped></style>
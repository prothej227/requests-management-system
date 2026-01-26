<template>
    <form @submit.prevent="submitForm">
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="shortDescription">Customer Name</label>
            <div class="col-md-8 col-12">
                <input type="text" class="form-control" id="shortDescription" v-model="customerForm.name"
                    placeholder="Customer Name">
            </div>
        </div>
    </form>
</template>

<script>
import axios from 'axios';
import { API } from '@/utils/constants';
export default {
    name: 'CreateCustomerForm',
    data() {
        return {
            customerForm: {
                'name': ''
            }
        };
    },
    mounted() { },
    methods: {
        async submitForm() {
            try {
                const response = await axios.post(`${API.MASTER.customer['create']}`, this.customerForm, { withCredentials: true });
                if (response.status === 200) {
                    this.$emit('customer-created', response.data);
                }
            } catch (error) {
                console.error('Error creating customer:', error);
            }
        }
    },
}
</script>

<style lang="scss" scoped></style>
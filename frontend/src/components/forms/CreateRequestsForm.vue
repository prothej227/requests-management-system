<template>
    <form @submit.prevent="submitForm">
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="dateReceived">Date Received</label>
            <div class="col-md-8 col-12">
                <input type="date" class="form-control" id="dateReceived" v-model="requestForm.date_received">
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="customerId">Customer</label>
            <div class="col-md-8 col-12">
                <select v-model="requestForm.customer_id" class="form-control" id="customerId">
                    <option value="" disabled selected>Select Customer</option>
                    <option v-if="dropDownValues.customer" v-for="value in dropDownValues.customer" :key="value.id"
                        :value="value.id">{{ value.name }}
                    </option>
                </select>
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="customerId">Area</label>
            <div class="col-md-8 col-12">
                <select v-model="requestForm.area_id" class="form-control" id="customerId">
                    <option value="" disabled selected>Select Area</option>
                    <option v-if="dropDownValues.area" v-for="value in dropDownValues.area" :key="value.id"
                        :value="value.id">{{ value.name }}</option>
                </select>
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="quantity">Quantity</label>
            <div class="col-md-8 col-12">
                <input type="number" class="form-control" id="quantity" v-model="requestForm.quantity"
                    placeholder="Quantity">
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="shortDescription">Short
                Description</label>
            <div class="col-md-8 col-12">
                <input type="text" class="form-control" id="shortDescription" v-model="requestForm.short_description"
                    placeholder="Short Description">
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="longDescription">Long
                Description</label>
            <div class="col-md-8 col-12">
                <textarea class="form-control" id="longDescription" v-model="requestForm.long_description"
                    placeholder="Long Description"></textarea>
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="salesPersonId">Sales Person</label>
            <div class="col-md-8 col-12">
                <select class="form-control" id="salesPersonId" v-model.number="requestForm.sales_person_id"
                    placeholder="Sales Person ID">
                    <option value="" disabled selected>Select Sales Person</option>
                    <option v-if="dropDownValues.area" v-for="value in dropDownValues.salesperson" :key="value.id"
                        :value="value.id">{{ value.name }}</option>
                </select>
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="status">Status</label>
            <div class="col-md-8 col-12">
                <select class="form-control" id="salesPersonId" v-model.number="requestForm.status"
                    placeholder="Status">
                    <option v-for="value in referenceValues.status" :key="value" :value="value">{{ value }}</option>
                </select>
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="feedback">Feedback</label>
            <div class="col-md-8 col-12">
                <select class="form-control" id="salesPersonId" v-model.number="requestForm.feedback"
                    placeholder="Feedback">
                    <option v-for="value in referenceValues.feedback" :key="value" :value="value">{{ value }}</option>
                </select>
            </div>
        </div>
        <div class="form-group row mb-2">
            <label class="text-secondary-emphasis fw-bold col-md-4 col-12" for="lpoNo">LPO No.</label>
            <div class="col-md-8 col-12">
                <input :disabled="requestForm.feedback !== 'Approved'" type="text" class="form-control" id="lpoNo"
                    v-model="requestForm.lpo_no" placeholder="LPO No.">
            </div>
        </div>
    </form>
</template>

<script>
import axios from 'axios';
import { API } from '@/utils/constants';
import { ReferenceValues } from '@/utils/constants';

export default {
    name: 'CreateRequestsForm',
    data() {
        return {
            requestForm: {
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
            },
            dropDownValues: {
                customer: [],
                area: []
            },
            referenceValues: {
                status: ReferenceValues.REQUESTS.STATUS,
                feedback: ReferenceValues.REQUESTS.FEEDBACK
            }
        };
    },
    mounted() {
        this.fetchAllDropdownValues();
    },
    methods: {
        async submitForm() {
            try {
                this.requestForm.customer_id = parseInt(this.requestForm.customer_id);
                this.requestForm.area_id = parseInt(this.requestForm.area_id);
                const response = await axios.post(`${API.REQUESTS['create']}`, this.requestForm, { withCredentials: true });
                if (response.status === 200) {
                    toast.success("Record created successfully.")
                    this.$emit('request-created', response.data);
                }
            } catch (error) {
                console.error('Error creating request:', error);
            }
        },
        async fetchAllDropdownValues() {
            try {
                const response = await axios.get(API.REQUESTS['create-all-dropdown-values'])
                if (response.status === 200) {
                    this.dropDownValues = response.data.response;
                }
            } catch (error) {
                console.error('Error fetching dropdown values:', error);
            }
        },
    },
}
</script>

<style lang="scss" scoped></style>
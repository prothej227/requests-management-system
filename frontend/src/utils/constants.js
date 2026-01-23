
const BASE_API_URL = process.env.VUE_APP_RMS_BACKEND_API;

const TableHeaders = {
    REQUESTS: [
        { text: 'ID', value: 'id' },
        { text: 'Lab Reference No.', value: 'ref_no' },
        { text: 'Date Received', value: 'date_received' },
        { text: 'Area Name', value: 'area_name' },
        { text: 'Customer Name', value: 'customer_name' },
        { text: 'Short Description', value: 'short_description' },
        { text: 'Long Description', value: 'long_description' },
        { text: 'Sales Person', value: 'sales_person_id' },
        { text: 'Status', value: 'status' },
        { text: 'Category', value: 'category' },
        { text: 'LPO No.', value: 'lpo_no' },
        { text: 'Created By', value: 'created_by' },
        { text: 'Created On', value: 'created_on' },
    ],
}

const API = {
    REQUESTS: {
        'list':`${BASE_API_URL}/records/requests/list`,
        'create':`${BASE_API_URL}/records/requests/create`,
        'create-all-dropdown-values': `${BASE_API_URL}/utils/all-dropdown-values`
    }
}
export { 
    TableHeaders, 
    API 
}
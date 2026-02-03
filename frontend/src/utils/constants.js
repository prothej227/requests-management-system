const BASE_API_URL = process.env.VUE_APP_RMS_BACKEND_API;

const TableHeaders = {
  REQUESTS: [
    { text: "ID", value: "id" },
    { text: "Lab Reference No.", value: "ref_no" },
    { text: "Date Received", value: "date_received" },
    { text: "Area Name", value: "area_name" },
    { text: "Customer Name", value: "customer_name" },
    { text: "Short Description", value: "short_description" },
    { text: "Long Description", value: "long_description" },
    { text: "Sales Person", value: "sales_person" },
    { text: "Status", value: "status" },
    { text: "Feedback", value: "feedback" },
    { text: "LPO No.", value: "lpo_no" },
    { text: "Created By", value: "created_by" },
    { text: "Created On", value: "created_on" },
  ],
  MASTER: {
    customer: [
      { text: "ID", value: "id" },
      { text: "Customer Name", value: "name" },
    ],
    area: [
      { text: "ID", value: "id", width: 1 },
      { text: "Logo", value: "logo", width: 100 },
      { text: "Area Name", value: "name" },
    ],
    salesperson: [
      { text: "ID", value: "id" },
      { text: "First Name", value: "first_name" },
      { text: "Last Name", value: "last_name" },
    ],
  },
  STICKERS: {
    canvas: [
      { text: "Actions", value: "actions", width: 50 },
      { text: "ID", value: "id", width: 10 },
      { text: "Status", value: "status", width: 50 },
      { text: "Stickers Count", value: "stickers_count" },
      { text: "Created On", value: "created_on" },
      { text: "GET", value: "get", width: 100 },
    ],
    selectedRequestsTable: [
      { text: "", value: "actions", sortable: false, width: 1 },
      { text: "ID", value: "id" },
      { text: "Lab Reference No.", value: "ref_no" },
      { text: "Customer Name", value: "customer_name" },
      { text: "Short Description", value: "short_description" },
      { text: "Status", value: "status" },
    ],
  },
};

const ReferenceValues = {
  REQUESTS: {
    STATUS: ["Not Started", "In Progress", "Completed"],
    FEEDBACK: ["N/A", "Approved", "Rejected", "Cancelled"],
  },
};

const API = {
  REQUESTS: {
    list: `${BASE_API_URL}/records/requests/list`,
    create: `${BASE_API_URL}/records/requests/create`,
    "create-all-dropdown-values": `${BASE_API_URL}/utils/all-dropdown-values`,
  },
  MASTER: {
    customer: {
      list: `${BASE_API_URL}/records/customers/list`,
      create: `${BASE_API_URL}/records/customers/create`,
    },
    area: {
      list: `${BASE_API_URL}/records/areas/list`,
      create: `${BASE_API_URL}/records/areas/create`,
    },
    salesperson: {
      list: `${BASE_API_URL}/records/sales-persons/list`,
      create: `${BASE_API_URL}/records/sales-persons/create`,
    },
  },
  STICKERS: {
    list: `${BASE_API_URL}/sticker-service/canvas/list`,
    create: `${BASE_API_URL}/sticker-service/canvas/create`,
    sticker_download_base_url: `${BASE_API_URL}/sticker-service/document`,
    generate_sticker_canvas: `${BASE_API_URL}/sticker-service/generate-sticker-pdf`,
  },
};
export { TableHeaders, API, ReferenceValues };

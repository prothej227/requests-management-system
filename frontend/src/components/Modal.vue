<template>
    <div class="modal fade" id="baseModal" tabindex="-1" ref="modalEle">
        <div :class="`modal-dialog modal-${size} modal-dialog-centered`">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="baseModalLabel">
                        <i :class="`${biHeaderIcon} me-1`"></i>
                        {{ title }}
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <slot name="body"></slot>
                </div>
                <div class="modal-footer">
                    <slot name="footer"></slot>
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { Modal } from "bootstrap";

// define props
defineProps({
    title: {
        type: String,
        default: "<<Title goes here>>",
    },
    biHeaderIcon: {
        type: String,
        default: "bi bi-info-circle",
    },
    size: {
        type: String,
        default: "lg", // sm, lg, xl, xxl
    },
});

// refs and variables
const modalEle = ref(null);
let thisModalObj = null;

// lifecycle
onMounted(() => {
    if (modalEle.value) {
        thisModalObj = new Modal(modalEle.value);
    }
});

// exposed methods
function _show() {
    thisModalObj?.show();
}
function _hide() {
    thisModalObj?.hide();
}

defineExpose({ show: _show, hide: _hide });
</script>
<style></style>
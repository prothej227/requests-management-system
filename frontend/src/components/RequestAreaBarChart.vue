<template>
    <div class="chart-wrapper">
        <Bar v-if="chartData" class="px-3" :data="chartData" :options="chartOptions" />
        <div v-else class="spinner-container">
            <VueSpinnerHourglass size="50" color="#0d6efd" />
        </div>
    </div>
</template>


<script>
import { Bar } from 'vue-chartjs'
import { VueSpinnerHourglass } from 'vue3-spinners';
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
} from 'chart.js'
import axios from 'axios'
import { API } from '@/utils/constants'

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
)

// random color with alpha
const randomColor = (alpha = 0.35) => {
    const r = Math.floor(180 + Math.random() * 60)
    const g = Math.floor(180 + Math.random() * 60)
    const b = Math.floor(180 + Math.random() * 60)
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

export default {
    name: 'RequestAreaBarChart',
    components: { Bar, VueSpinnerHourglass },

    data() {
        return {
            chartData: null,
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                // 🔹 Enhanced Animation Settings
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart',
                    // This makes the bars "grow" from the bottom on first load
                    onProgress: function (animation) {
                        // Optional: You can add custom logic here
                    }
                },
                // 🔹 Smooth transitions when data changes
                transitions: {
                    active: {
                        animation: {
                            duration: 400
                        }
                    }
                },
                // 🔹 Hover animations
                hover: {
                    mode: 'index',
                    intersect: false,
                    animationDuration: 400
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Requests Count'
                    }
                },
                scales: {
                    x: {
                        stacked: false
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }

        }
    },

    async mounted() {
        await this.getRequestByArea()
    },

    methods: {
        async getRequestByArea() {
            const { data } = await axios.get(API.DASHBOARD.request_by_area)
            const labels = ['Requests'] // single category
            const datasets = Object.entries(data).map(([area, count]) => ({
                label: area,
                data: [count],
                backgroundColor: randomColor(0.35),
                borderColor: randomColor(0.7),
                borderWidth: 1,
                borderRadius: 6
            }))

            this.chartData = { labels, datasets }

        }
    }
}
</script>


<style scoped>
/* give the chart height or it won’t show */
canvas {
    max-height: 25em;
    ;
}

.chart-wrapper {
    position: relative;
    height: 25em;
    /* match your canvas height */
}

.spinner-container {
    display: flex;
    justify-content: center;
    /* horizontal */
    align-items: center;
    /* vertical */
    height: 100%;
}
</style>

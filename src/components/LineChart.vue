<template>
  <LineChartGenerator
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>

<script>
import { Line as LineChartGenerator } from 'vue-chartjs/legacy'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
)

export default {
  name: 'LineChart',
  components: {
    LineChartGenerator
  },
  props: {
    chartId: {
      type: String,
      default: 'line-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 400
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => {}
    },
    plugins: {
      type: Array,
      default: () => []
    },
    externalChartData: {
      type: Object,
      default: () => ({})
    },
    externalChartOptions: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      chartData: this.externalChartData || {
        labels: [
          '2023-06-15T13:45:30',
          '2023-06-15T13:45:35',
          '2023-06-15T13:45:40',
          '2023-06-15T13:45:45',
          '2023-06-15T13:45:50',
          '2023-06-15T13:45:55',
          '2023-06-15T13:45:60'
        ],
        datasets: [
          {
            label: 'Emotion Time Series',
            backgroundColor: 'rgba(179,181,198,1)',
            borderColor:'rgba(179,181,198,1)',
            data: [50, 50, 50, 50, 50, 50, 50]
          }
        ]
      },
      chartOptions: this.externalChartOptions || {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  watch: {
    externalChartData: {
      deep: true,
      handler(newVal) {
        this.chartData = newVal;
        console.log("Updated chartData:", this.chartData);
      }
    }
  },
}
</script>

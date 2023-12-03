<template>
  <Radar
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
import { Radar } from 'vue-chartjs/legacy'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  RadialLinearScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  PointElement,
  RadialLinearScale,
  LineElement
)

export default {
  name: 'RadarChart',
  components: {
    Radar
  },
  props: {
    chartId: {
      type: String,
      default: 'radar-chart'
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
      chartData:  this.externalChartData ||{
        labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
        datasets: [
          {
            label: 'Emotions',
            backgroundColor: 'rgba(179,181,198,0.2)',
            borderColor: 'rgba(179,181,198,1)',
            pointBackgroundColor: 'rgba(179,181,198,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(179,181,198,1)',
            data: [65, 59, 90, 81, 56, 55, 40]
          },
          // {
          //   label: 'My Second dataset',
          //   backgroundColor: 'rgba(255,99,132,0.2)',
          //   borderColor: 'rgba(255,99,132,1)',
          //   pointBackgroundColor: 'rgba(255,99,132,1)',
          //   pointBorderColor: '#fff',
          //   pointHoverBackgroundColor: '#fff',
          //   pointHoverBorderColor: 'rgba(255,99,132,1)',
          //   data: [28, 48, 40, 19, 96, 27, 100]
          // }
        ]
      },
      chartOptions: this.externalChartOptions ||{
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
        // console.log("Updated chartData:", this.chartData);
      }
    }
  },
}
</script>

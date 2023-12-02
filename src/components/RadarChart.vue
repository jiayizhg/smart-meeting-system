<template>
  <div>
    <div class="chart-container">
        <radar-chart :chart-data="chartData" :options="chartOptions"/>
    </div>
  </div>
</template>
<style>
.chart-container {
  min-width: 400px;
}
</style>
<script>
import { Radar } from 'vue-chartjs/legacy'

export default {
  extends: Radar,
  props: ['chartData', 'options'],
  async mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script>

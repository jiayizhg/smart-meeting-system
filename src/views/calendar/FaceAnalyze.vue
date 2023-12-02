<template>
  <div>
    <radar-chart v-if="emotion" :chart-data="radarChartData" :options="radarChartOptions"/>
    <div v-if="emotion">
      <h3>Emotions:</h3>
      <ul>
        <li v-for="(value, key) in emotion" :key="key">
          {{ key }}: {{ value.toFixed(2) }}%
        </li>
      </ul>
    </div>
    <div v-if="eyes_status">
      <h3>Eyes Status:</h3>
      Left Eye: {{ eyes_status.left_eye }}<br>
      Right Eye: {{ eyes_status.right_eye }}
    </div>
    <select v-model="selectedCameraId">
      <option v-for="camera in cameras" :key="camera.deviceId" :value="camera.deviceId">
        {{ camera.label }}
      </option>
    </select>
    <button  v-if="!videoStream" @click="startCamera">Start Camera</button>
    <button v-if="videoStream" @click="stopCamera">Close Camera</button>
    <video v-if="videoStream" ref="videoElement" autoplay playsinline></video>
    <div class="cat"  :style="{ right: rightPos + 'px', bottom: bottomPos + 'px' }"
    @mousedown.prevent="startDrag"
    @mousemove="onDrag"
    @mouseup="endDrag"
    @mouseleave="endDrag">

    </div>
  </div>
</template>
<style>
.cat {
  position: fixed;
  background-color: aqua;
  cursor: grab;  
  cursor: -webkit-grab;
  animation: x 1s infinite;
  -webkit-animation: x 1s infinite;
  -moz-animation: x 1s infinite;
  -o-animation: x 1s infinite;
}

@keyframes x {
0%, 25%{
  box-shadow: 10px 10px 0 0 rgba(0,0,0,0), 20px 10px 0 0 rgba(0,0,0,0), 30px 10px 0 0 rgba(0,0,0,0), 40px 10px 0 0 rgba(0,0,0,0), 50px 10px 0 0 rgba(0,0,0,0), 60px 10px 0 0 rgba(0,0,0,0), 70px 10px 0 0 #ffffff, 80px 10px 0 0 rgba(0,0,0,0), 90px 10px 0 0 rgba(0,0,0,0), 100px 10px 0 0 rgba(0,0,0,0), 110px 10px 0 0 rgba(0,0,0,0), 120px 10px 0 0 #ffffff, 130px 10px 0 0 rgba(0,0,0,0), 140px 10px 0 0 rgba(0,0,0,0), 150px 10px 0 0 rgba(0,0,0,0), 160px 10px 0 0 rgba(0,0,0,0), 10px 20px 0 0 rgba(0,0,0,0), 20px 20px 0 0 rgba(0,0,0,0), 30px 20px 0 0 rgba(0,0,0,0), 40px 20px 0 0 rgba(0,0,0,0), 50px 20px 0 0 rgba(0,0,0,0), 60px 20px 0 0 #ffffff, 70px 20px 0 0 #ffcdd2, 80px 20px 0 0 #ffffff, 90px 20px 0 0 rgba(0,0,0,0), 100px 20px 0 0 rgba(0,0,0,0), 110px 20px 0 0 #ffffff, 120px 20px 0 0 #ffcdd2, 130px 20px 0 0 #ffffff, 140px 20px 0 0 rgba(0,0,0,0), 150px 20px 0 0 rgba(0,0,0,0), 160px 20px 0 0 rgba(0,0,0,0), 10px 30px 0 0 rgba(0,0,0,0), 20px 30px 0 0 rgba(0,0,0,0), 30px 30px 0 0 rgba(0,0,0,0), 40px 30px 0 0 rgba(0,0,0,0), 50px 30px 0 0 rgba(0,0,0,0), 60px 30px 0 0 #ffffff, 70px 30px 0 0 #ffcdd2, 80px 30px 0 0 #ffcdd2, 90px 30px 0 0 #ffffff, 100px 30px 0 0 #ffffff, 110px 30px 0 0 #ffcdd2, 120px 30px 0 0 #ffcdd2, 130px 30px 0 0 #ffffff, 140px 30px 0 0 rgba(0,0,0,0), 150px 30px 0 0 rgba(0,0,0,0), 160px 30px 0 0 rgba(0,0,0,0), 10px 40px 0 0 rgba(0,0,0,0), 20px 40px 0 0 rgba(0,0,0,0), 30px 40px 0 0 rgba(0,0,0,0), 40px 40px 0 0 rgba(0,0,0,0), 50px 40px 0 0 rgba(0,0,0,0), 60px 40px 0 0 #ffffff, 70px 40px 0 0 #ffcdd2, 80px 40px 0 0 #ffffff, 90px 40px 0 0 #ffffff, 100px 40px 0 0 #ffffff, 110px 40px 0 0 #ffffff, 120px 40px 0 0 #ffcdd2, 130px 40px 0 0 #ffffff, 140px 40px 0 0 rgba(0,0,0,0), 150px 40px 0 0 rgba(0,0,0,0), 160px 40px 0 0 rgba(0,0,0,0), 10px 50px 0 0 rgba(0,0,0,0), 20px 50px 0 0 rgba(0,0,0,0), 30px 50px 0 0 rgba(0,0,0,0), 40px 50px 0 0 rgba(0,0,0,0), 50px 50px 0 0 rgba(0,0,0,0), 60px 50px 0 0 #ffffff, 70px 50px 0 0 #ffffff, 80px 50px 0 0 #ffffff, 90px 50px 0 0 #ffffff, 100px 50px 0 0 #ffffff, 110px 50px 0 0 #ffffff, 120px 50px 0 0 #ffffff, 130px 50px 0 0 #ffffff, 140px 50px 0 0 rgba(0,0,0,0), 150px 50px 0 0 rgba(0,0,0,0), 160px 50px 0 0 rgba(0,0,0,0), 10px 60px 0 0 rgba(0,0,0,0), 20px 60px 0 0 rgba(0,0,0,0), 30px 60px 0 0 rgba(0,0,0,0), 40px 60px 0 0 rgba(0,0,0,0), 50px 60px 0 0 rgba(0,0,0,0), 60px 60px 0 0 #ffffff, 70px 60px 0 0 #000000, 80px 60px 0 0 #ffffff, 90px 60px 0 0 #ffffff, 100px 60px 0 0 #000000, 110px 60px 0 0 #ffffff, 120px 60px 0 0 #ffffff, 130px 60px 0 0 #ffffff, 140px 60px 0 0 rgba(0,0,0,0), 150px 60px 0 0 rgba(0,0,0,0), 160px 60px 0 0 rgba(0,0,0,0), 10px 70px 0 0 rgba(0,0,0,0), 20px 70px 0 0 rgba(0,0,0,0), 30px 70px 0 0 rgba(0,0,0,0), 40px 70px 0 0 rgba(0,0,0,0), 50px 70px 0 0 rgba(0,0,0,0), 60px 70px 0 0 #ffffff, 70px 70px 0 0 #ffffff, 80px 70px 0 0 #000000, 90px 70px 0 0 #ffffff, 100px 70px 0 0 #ffffff, 110px 70px 0 0 #ffffff, 120px 70px 0 0 #ffffff, 130px 70px 0 0 #ffffff, 140px 70px 0 0 rgba(0,0,0,0), 150px 70px 0 0 rgba(0,0,0,0), 160px 70px 0 0 rgba(0,0,0,0), 10px 80px 0 0 rgba(0,0,0,0), 20px 80px 0 0 rgba(0,0,0,0), 30px 80px 0 0 rgba(0,0,0,0), 40px 80px 0 0 rgba(0,0,0,0), 50px 80px 0 0 rgba(0,0,0,0), 60px 80px 0 0 #ffffff, 70px 80px 0 0 #ffffff, 80px 80px 0 0 #ffffff, 90px 80px 0 0 #ffffff, 100px 80px 0 0 #ffffff, 110px 80px 0 0 #ffffff, 120px 80px 0 0 #ffffff, 130px 80px 0 0 #ffffff, 140px 80px 0 0 rgba(0,0,0,0), 150px 80px 0 0 rgba(0,0,0,0), 160px 80px 0 0 rgba(0,0,0,0), 10px 90px 0 0 rgba(0,0,0,0), 20px 90px 0 0 rgba(0,0,0,0), 30px 90px 0 0 rgba(0,0,0,0), 40px 90px 0 0 rgba(0,0,0,0), 50px 90px 0 0 rgba(0,0,0,0), 60px 90px 0 0 rgba(0,0,0,0), 70px 90px 0 0 #ffffff, 80px 90px 0 0 #ffffff, 90px 90px 0 0 #ffffff, 100px 90px 0 0 #ffffff, 110px 90px 0 0 #ffffff, 120px 90px 0 0 #ffffff, 130px 90px 0 0 rgba(0,0,0,0), 140px 90px 0 0 rgba(0,0,0,0), 150px 90px 0 0 rgba(0,0,0,0), 160px 90px 0 0 rgba(0,0,0,0), 10px 100px 0 0 rgba(0,0,0,0), 20px 100px 0 0 rgba(0,0,0,0), 30px 100px 0 0 rgba(0,0,0,0), 40px 100px 0 0 rgba(0,0,0,0), 50px 100px 0 0 rgba(0,0,0,0), 60px 100px 0 0 rgba(0,0,0,0), 70px 100px 0 0 rgba(0,0,0,0), 80px 100px 0 0 #ffffff, 90px 100px 0 0 #ffffff, 100px 100px 0 0 #ffffff, 110px 100px 0 0 #ffffff, 120px 100px 0 0 rgba(0,0,0,0), 130px 100px 0 0 rgba(0,0,0,0), 140px 100px 0 0 #ffffff, 150px 100px 0 0 rgba(0,0,0,0), 160px 100px 0 0 rgba(0,0,0,0), 10px 110px 0 0 rgba(0,0,0,0), 20px 110px 0 0 rgba(0,0,0,0), 30px 110px 0 0 rgba(0,0,0,0), 40px 110px 0 0 rgba(0,0,0,0), 50px 110px 0 0 rgba(0,0,0,0), 60px 110px 0 0 rgba(0,0,0,0), 70px 110px 0 0 rgba(0,0,0,0), 80px 110px 0 0 #ffffff, 90px 110px 0 0 #ffffff, 100px 110px 0 0 #ffffff, 110px 110px 0 0 #ffffff, 120px 110px 0 0 rgba(0,0,0,0), 130px 110px 0 0 rgba(0,0,0,0), 140px 110px 0 0 rgba(0,0,0,0), 150px 110px 0 0 #ffffff, 160px 110px 0 0 rgba(0,0,0,0), 10px 120px 0 0 rgba(0,0,0,0), 20px 120px 0 0 rgba(0,0,0,0), 30px 120px 0 0 rgba(0,0,0,0), 40px 120px 0 0 rgba(0,0,0,0), 50px 120px 0 0 rgba(0,0,0,0), 60px 120px 0 0 rgba(0,0,0,0), 70px 120px 0 0 #ffffff, 80px 120px 0 0 #ffffff, 90px 120px 0 0 #ffffff, 100px 120px 0 0 #ffffff, 110px 120px 0 0 #ffffff, 120px 120px 0 0 #ffffff, 130px 120px 0 0 rgba(0,0,0,0), 140px 120px 0 0 rgba(0,0,0,0), 150px 120px 0 0 #ffffff, 160px 120px 0 0 rgba(0,0,0,0), 10px 130px 0 0 rgba(0,0,0,0), 20px 130px 0 0 rgba(0,0,0,0), 30px 130px 0 0 rgba(0,0,0,0), 40px 130px 0 0 rgba(0,0,0,0), 50px 130px 0 0 #ffffff, 60px 130px 0 0 #ffffff, 70px 130px 0 0 #ffffff, 80px 130px 0 0 #ffffff, 90px 130px 0 0 #ffffff, 100px 130px 0 0 #ffffff, 110px 130px 0 0 #ffffff, 120px 130px 0 0 #ffffff, 130px 130px 0 0 rgba(0,0,0,0), 140px 130px 0 0 rgba(0,0,0,0), 150px 130px 0 0 #ffffff, 160px 130px 0 0 rgba(0,0,0,0), 10px 140px 0 0 rgba(0,0,0,0), 20px 140px 0 0 rgba(0,0,0,0), 30px 140px 0 0 rgba(0,0,0,0), 40px 140px 0 0 rgba(0,0,0,0), 50px 140px 0 0 #ffffff, 60px 140px 0 0 #ffffff, 70px 140px 0 0 #ffffff, 80px 140px 0 0 #ffffff, 90px 140px 0 0 #ffffff, 100px 140px 0 0 #ffffff, 110px 140px 0 0 #ffffff, 120px 140px 0 0 #ffffff, 130px 140px 0 0 rgba(0,0,0,0), 140px 140px 0 0 #ffffff, 150px 140px 0 0 #ffffff, 160px 140px 0 0 rgba(0,0,0,0), 10px 150px 0 0 rgba(0,0,0,0), 20px 150px 0 0 rgba(0,0,0,0), 30px 150px 0 0 rgba(0,0,0,0), 40px 150px 0 0 #ffffff, 50px 150px 0 0 #ffffff, 60px 150px 0 0 #ffffff, 70px 150px 0 0 #ffffff, 80px 150px 0 0 #ffffff, 90px 150px 0 0 #ffffff, 100px 150px 0 0 #ffffff, 110px 150px 0 0 #ffffff, 120px 150px 0 0 #ffffff, 130px 150px 0 0 #ffffff, 140px 150px 0 0 #ffffff, 150px 150px 0 0 rgba(0,0,0,0), 160px 150px 0 0 rgba(0,0,0,0), 10px 160px 0 0 #607d8b, 20px 160px 0 0 #607d8b, 30px 160px 0 0 #607d8b, 40px 160px 0 0 #607d8b, 50px 160px 0 0 #607d8b, 60px 160px 0 0 #ffffff, 70px 160px 0 0 #ffffff, 80px 160px 0 0 #607d8b, 90px 160px 0 0 #607d8b, 100px 160px 0 0 #607d8b, 110px 160px 0 0 #ffffff, 120px 160px 0 0 #ffffff, 130px 160px 0 0 #607d8b, 140px 160px 0 0 #607d8b, 150px 160px 0 0 #607d8b, 160px 160px 0 0 #607d8b;height: 10px; width: 10px;
  }
25.01%, 50%{
  box-shadow: 10px 10px 0 0 rgba(0,0,0,0), 20px 10px 0 0 rgba(0,0,0,0), 30px 10px 0 0 rgba(0,0,0,0), 40px 10px 0 0 rgba(0,0,0,0), 50px 10px 0 0 rgba(0,0,0,0), 60px 10px 0 0 rgba(0,0,0,0), 70px 10px 0 0 #ffffff, 80px 10px 0 0 rgba(0,0,0,0), 90px 10px 0 0 rgba(0,0,0,0), 100px 10px 0 0 rgba(0,0,0,0), 110px 10px 0 0 rgba(0,0,0,0), 120px 10px 0 0 #ffffff, 130px 10px 0 0 rgba(0,0,0,0), 140px 10px 0 0 rgba(0,0,0,0), 150px 10px 0 0 rgba(0,0,0,0), 160px 10px 0 0 rgba(0,0,0,0), 10px 20px 0 0 rgba(0,0,0,0), 20px 20px 0 0 rgba(0,0,0,0), 30px 20px 0 0 rgba(0,0,0,0), 40px 20px 0 0 rgba(0,0,0,0), 50px 20px 0 0 rgba(0,0,0,0), 60px 20px 0 0 #ffffff, 70px 20px 0 0 #ffcdd2, 80px 20px 0 0 #ffffff, 90px 20px 0 0 rgba(0,0,0,0), 100px 20px 0 0 rgba(0,0,0,0), 110px 20px 0 0 #ffffff, 120px 20px 0 0 #ffcdd2, 130px 20px 0 0 #ffffff, 140px 20px 0 0 rgba(0,0,0,0), 150px 20px 0 0 rgba(0,0,0,0), 160px 20px 0 0 rgba(0,0,0,0), 10px 30px 0 0 rgba(0,0,0,0), 20px 30px 0 0 rgba(0,0,0,0), 30px 30px 0 0 rgba(0,0,0,0), 40px 30px 0 0 rgba(0,0,0,0), 50px 30px 0 0 rgba(0,0,0,0), 60px 30px 0 0 #ffffff, 70px 30px 0 0 #ffcdd2, 80px 30px 0 0 #ffcdd2, 90px 30px 0 0 #ffffff, 100px 30px 0 0 #ffffff, 110px 30px 0 0 #ffcdd2, 120px 30px 0 0 #ffcdd2, 130px 30px 0 0 #ffffff, 140px 30px 0 0 rgba(0,0,0,0), 150px 30px 0 0 rgba(0,0,0,0), 160px 30px 0 0 rgba(0,0,0,0), 10px 40px 0 0 rgba(0,0,0,0), 20px 40px 0 0 rgba(0,0,0,0), 30px 40px 0 0 rgba(0,0,0,0), 40px 40px 0 0 rgba(0,0,0,0), 50px 40px 0 0 rgba(0,0,0,0), 60px 40px 0 0 #ffffff, 70px 40px 0 0 #ffcdd2, 80px 40px 0 0 #ffffff, 90px 40px 0 0 #ffffff, 100px 40px 0 0 #ffffff, 110px 40px 0 0 #ffffff, 120px 40px 0 0 #ffcdd2, 130px 40px 0 0 #ffffff, 140px 40px 0 0 rgba(0,0,0,0), 150px 40px 0 0 rgba(0,0,0,0), 160px 40px 0 0 rgba(0,0,0,0), 10px 50px 0 0 rgba(0,0,0,0), 20px 50px 0 0 rgba(0,0,0,0), 30px 50px 0 0 rgba(0,0,0,0), 40px 50px 0 0 rgba(0,0,0,0), 50px 50px 0 0 rgba(0,0,0,0), 60px 50px 0 0 #ffffff, 70px 50px 0 0 #ffffff, 80px 50px 0 0 #ffffff, 90px 50px 0 0 #ffffff, 100px 50px 0 0 #ffffff, 110px 50px 0 0 #ffffff, 120px 50px 0 0 #ffffff, 130px 50px 0 0 #ffffff, 140px 50px 0 0 rgba(0,0,0,0), 150px 50px 0 0 rgba(0,0,0,0), 160px 50px 0 0 rgba(0,0,0,0), 10px 60px 0 0 rgba(0,0,0,0), 20px 60px 0 0 rgba(0,0,0,0), 30px 60px 0 0 rgba(0,0,0,0), 40px 60px 0 0 rgba(0,0,0,0), 50px 60px 0 0 rgba(0,0,0,0), 60px 60px 0 0 #ffffff, 70px 60px 0 0 #ffffff, 80px 60px 0 0 #000000, 90px 60px 0 0 #ffffff, 100px 60px 0 0 #ffffff, 110px 60px 0 0 #000000, 120px 60px 0 0 #ffffff, 130px 60px 0 0 #ffffff, 140px 60px 0 0 rgba(0,0,0,0), 150px 60px 0 0 rgba(0,0,0,0), 160px 60px 0 0 rgba(0,0,0,0), 10px 70px 0 0 rgba(0,0,0,0), 20px 70px 0 0 rgba(0,0,0,0), 30px 70px 0 0 rgba(0,0,0,0), 40px 70px 0 0 rgba(0,0,0,0), 50px 70px 0 0 rgba(0,0,0,0), 60px 70px 0 0 #ffffff, 70px 70px 0 0 #ffffff, 80px 70px 0 0 #ffffff, 90px 70px 0 0 #ffffff, 100px 70px 0 0 #000000, 110px 70px 0 0 #ffffff, 120px 70px 0 0 #ffffff, 130px 70px 0 0 #ffffff, 140px 70px 0 0 rgba(0,0,0,0), 150px 70px 0 0 rgba(0,0,0,0), 160px 70px 0 0 rgba(0,0,0,0), 10px 80px 0 0 rgba(0,0,0,0), 20px 80px 0 0 rgba(0,0,0,0), 30px 80px 0 0 rgba(0,0,0,0), 40px 80px 0 0 rgba(0,0,0,0), 50px 80px 0 0 rgba(0,0,0,0), 60px 80px 0 0 #ffffff, 70px 80px 0 0 #ffffff, 80px 80px 0 0 #ffffff, 90px 80px 0 0 #ffffff, 100px 80px 0 0 #ffffff, 110px 80px 0 0 #ffffff, 120px 80px 0 0 #ffffff, 130px 80px 0 0 #ffffff, 140px 80px 0 0 rgba(0,0,0,0), 150px 80px 0 0 rgba(0,0,0,0), 160px 80px 0 0 rgba(0,0,0,0), 10px 90px 0 0 rgba(0,0,0,0), 20px 90px 0 0 rgba(0,0,0,0), 30px 90px 0 0 rgba(0,0,0,0), 40px 90px 0 0 rgba(0,0,0,0), 50px 90px 0 0 rgba(0,0,0,0), 60px 90px 0 0 rgba(0,0,0,0), 70px 90px 0 0 #ffffff, 80px 90px 0 0 #ffffff, 90px 90px 0 0 #ffffff, 100px 90px 0 0 #ffffff, 110px 90px 0 0 #ffffff, 120px 90px 0 0 #ffffff, 130px 90px 0 0 rgba(0,0,0,0), 140px 90px 0 0 rgba(0,0,0,0), 150px 90px 0 0 rgba(0,0,0,0), 160px 90px 0 0 rgba(0,0,0,0), 10px 100px 0 0 rgba(0,0,0,0), 20px 100px 0 0 rgba(0,0,0,0), 30px 100px 0 0 rgba(0,0,0,0), 40px 100px 0 0 rgba(0,0,0,0), 50px 100px 0 0 rgba(0,0,0,0), 60px 100px 0 0 rgba(0,0,0,0), 70px 100px 0 0 rgba(0,0,0,0), 80px 100px 0 0 #ffffff, 90px 100px 0 0 #ffffff, 100px 100px 0 0 #ffffff, 110px 100px 0 0 #ffffff, 120px 100px 0 0 rgba(0,0,0,0), 130px 100px 0 0 rgba(0,0,0,0), 140px 100px 0 0 #ffffff, 150px 100px 0 0 rgba(0,0,0,0), 160px 100px 0 0 rgba(0,0,0,0), 10px 110px 0 0 rgba(0,0,0,0), 20px 110px 0 0 rgba(0,0,0,0), 30px 110px 0 0 rgba(0,0,0,0), 40px 110px 0 0 rgba(0,0,0,0), 50px 110px 0 0 rgba(0,0,0,0), 60px 110px 0 0 rgba(0,0,0,0), 70px 110px 0 0 rgba(0,0,0,0), 80px 110px 0 0 #ffffff, 90px 110px 0 0 #ffffff, 100px 110px 0 0 #ffffff, 110px 110px 0 0 #ffffff, 120px 110px 0 0 rgba(0,0,0,0), 130px 110px 0 0 rgba(0,0,0,0), 140px 110px 0 0 rgba(0,0,0,0), 150px 110px 0 0 #ffffff, 160px 110px 0 0 rgba(0,0,0,0), 10px 120px 0 0 rgba(0,0,0,0), 20px 120px 0 0 rgba(0,0,0,0), 30px 120px 0 0 rgba(0,0,0,0), 40px 120px 0 0 rgba(0,0,0,0), 50px 120px 0 0 rgba(0,0,0,0), 60px 120px 0 0 rgba(0,0,0,0), 70px 120px 0 0 #ffffff, 80px 120px 0 0 #ffffff, 90px 120px 0 0 #ffffff, 100px 120px 0 0 #ffffff, 110px 120px 0 0 #ffffff, 120px 120px 0 0 #ffffff, 130px 120px 0 0 rgba(0,0,0,0), 140px 120px 0 0 rgba(0,0,0,0), 150px 120px 0 0 #ffffff, 160px 120px 0 0 rgba(0,0,0,0), 10px 130px 0 0 rgba(0,0,0,0), 20px 130px 0 0 rgba(0,0,0,0), 30px 130px 0 0 rgba(0,0,0,0), 40px 130px 0 0 rgba(0,0,0,0), 50px 130px 0 0 #ffffff, 60px 130px 0 0 #ffffff, 70px 130px 0 0 #ffffff, 80px 130px 0 0 #ffffff, 90px 130px 0 0 #ffffff, 100px 130px 0 0 #ffffff, 110px 130px 0 0 #ffffff, 120px 130px 0 0 #ffffff, 130px 130px 0 0 rgba(0,0,0,0), 140px 130px 0 0 rgba(0,0,0,0), 150px 130px 0 0 #ffffff, 160px 130px 0 0 rgba(0,0,0,0), 10px 140px 0 0 rgba(0,0,0,0), 20px 140px 0 0 rgba(0,0,0,0), 30px 140px 0 0 rgba(0,0,0,0), 40px 140px 0 0 rgba(0,0,0,0), 50px 140px 0 0 #ffffff, 60px 140px 0 0 #ffffff, 70px 140px 0 0 #ffffff, 80px 140px 0 0 #ffffff, 90px 140px 0 0 #ffffff, 100px 140px 0 0 #ffffff, 110px 140px 0 0 #ffffff, 120px 140px 0 0 #ffffff, 130px 140px 0 0 rgba(0,0,0,0), 140px 140px 0 0 #ffffff, 150px 140px 0 0 #ffffff, 160px 140px 0 0 rgba(0,0,0,0), 10px 150px 0 0 rgba(0,0,0,0), 20px 150px 0 0 rgba(0,0,0,0), 30px 150px 0 0 rgba(0,0,0,0), 40px 150px 0 0 #ffffff, 50px 150px 0 0 #ffffff, 60px 150px 0 0 #ffffff, 70px 150px 0 0 #ffffff, 80px 150px 0 0 #ffffff, 90px 150px 0 0 #ffffff, 100px 150px 0 0 #ffffff, 110px 150px 0 0 #ffffff, 120px 150px 0 0 #ffffff, 130px 150px 0 0 #ffffff, 140px 150px 0 0 #ffffff, 150px 150px 0 0 rgba(0,0,0,0), 160px 150px 0 0 rgba(0,0,0,0), 10px 160px 0 0 #607d8b, 20px 160px 0 0 #607d8b, 30px 160px 0 0 #607d8b, 40px 160px 0 0 #607d8b, 50px 160px 0 0 #607d8b, 60px 160px 0 0 #ffffff, 70px 160px 0 0 #ffffff, 80px 160px 0 0 #607d8b, 90px 160px 0 0 #607d8b, 100px 160px 0 0 #607d8b, 110px 160px 0 0 #ffffff, 120px 160px 0 0 #ffffff, 130px 160px 0 0 #607d8b, 140px 160px 0 0 #607d8b, 150px 160px 0 0 #607d8b, 160px 160px 0 0 #607d8b;height: 10px; width: 10px;
  }
50.01%, 75%{
  box-shadow: 10px 10px 0 0 rgba(0,0,0,0), 20px 10px 0 0 rgba(0,0,0,0), 30px 10px 0 0 rgba(0,0,0,0), 40px 10px 0 0 rgba(0,0,0,0), 50px 10px 0 0 rgba(0,0,0,0), 60px 10px 0 0 rgba(0,0,0,0), 70px 10px 0 0 #ffffff, 80px 10px 0 0 rgba(0,0,0,0), 90px 10px 0 0 rgba(0,0,0,0), 100px 10px 0 0 rgba(0,0,0,0), 110px 10px 0 0 rgba(0,0,0,0), 120px 10px 0 0 #ffffff, 130px 10px 0 0 rgba(0,0,0,0), 140px 10px 0 0 rgba(0,0,0,0), 150px 10px 0 0 rgba(0,0,0,0), 160px 10px 0 0 rgba(0,0,0,0), 10px 20px 0 0 rgba(0,0,0,0), 20px 20px 0 0 rgba(0,0,0,0), 30px 20px 0 0 rgba(0,0,0,0), 40px 20px 0 0 rgba(0,0,0,0), 50px 20px 0 0 rgba(0,0,0,0), 60px 20px 0 0 #ffffff, 70px 20px 0 0 #ffcdd2, 80px 20px 0 0 #ffffff, 90px 20px 0 0 rgba(0,0,0,0), 100px 20px 0 0 rgba(0,0,0,0), 110px 20px 0 0 #ffffff, 120px 20px 0 0 #ffcdd2, 130px 20px 0 0 #ffffff, 140px 20px 0 0 rgba(0,0,0,0), 150px 20px 0 0 rgba(0,0,0,0), 160px 20px 0 0 rgba(0,0,0,0), 10px 30px 0 0 rgba(0,0,0,0), 20px 30px 0 0 rgba(0,0,0,0), 30px 30px 0 0 rgba(0,0,0,0), 40px 30px 0 0 rgba(0,0,0,0), 50px 30px 0 0 rgba(0,0,0,0), 60px 30px 0 0 #ffffff, 70px 30px 0 0 #ffcdd2, 80px 30px 0 0 #ffcdd2, 90px 30px 0 0 #ffffff, 100px 30px 0 0 #ffffff, 110px 30px 0 0 #ffcdd2, 120px 30px 0 0 #ffcdd2, 130px 30px 0 0 #ffffff, 140px 30px 0 0 rgba(0,0,0,0), 150px 30px 0 0 rgba(0,0,0,0), 160px 30px 0 0 rgba(0,0,0,0), 10px 40px 0 0 rgba(0,0,0,0), 20px 40px 0 0 rgba(0,0,0,0), 30px 40px 0 0 rgba(0,0,0,0), 40px 40px 0 0 rgba(0,0,0,0), 50px 40px 0 0 rgba(0,0,0,0), 60px 40px 0 0 #ffffff, 70px 40px 0 0 #ffcdd2, 80px 40px 0 0 #ffffff, 90px 40px 0 0 #ffffff, 100px 40px 0 0 #ffffff, 110px 40px 0 0 #ffffff, 120px 40px 0 0 #ffcdd2, 130px 40px 0 0 #ffffff, 140px 40px 0 0 rgba(0,0,0,0), 150px 40px 0 0 rgba(0,0,0,0), 160px 40px 0 0 rgba(0,0,0,0), 10px 50px 0 0 rgba(0,0,0,0), 20px 50px 0 0 rgba(0,0,0,0), 30px 50px 0 0 rgba(0,0,0,0), 40px 50px 0 0 rgba(0,0,0,0), 50px 50px 0 0 rgba(0,0,0,0), 60px 50px 0 0 #ffffff, 70px 50px 0 0 #ffffff, 80px 50px 0 0 #ffffff, 90px 50px 0 0 #ffffff, 100px 50px 0 0 #ffffff, 110px 50px 0 0 #ffffff, 120px 50px 0 0 #ffffff, 130px 50px 0 0 #ffffff, 140px 50px 0 0 rgba(0,0,0,0), 150px 50px 0 0 rgba(0,0,0,0), 160px 50px 0 0 rgba(0,0,0,0), 10px 60px 0 0 rgba(0,0,0,0), 20px 60px 0 0 rgba(0,0,0,0), 30px 60px 0 0 rgba(0,0,0,0), 40px 60px 0 0 rgba(0,0,0,0), 50px 60px 0 0 rgba(0,0,0,0), 60px 60px 0 0 #ffffff, 70px 60px 0 0 #ffffff, 80px 60px 0 0 #000000, 90px 60px 0 0 #ffffff, 100px 60px 0 0 #ffffff, 110px 60px 0 0 #000000, 120px 60px 0 0 #ffffff, 130px 60px 0 0 #ffffff, 140px 60px 0 0 rgba(0,0,0,0), 150px 60px 0 0 rgba(0,0,0,0), 160px 60px 0 0 rgba(0,0,0,0), 10px 70px 0 0 rgba(0,0,0,0), 20px 70px 0 0 rgba(0,0,0,0), 30px 70px 0 0 rgba(0,0,0,0), 40px 70px 0 0 rgba(0,0,0,0), 50px 70px 0 0 rgba(0,0,0,0), 60px 70px 0 0 #ffffff, 70px 70px 0 0 #ffffff, 80px 70px 0 0 #ffffff, 90px 70px 0 0 #ffffff, 100px 70px 0 0 #000000, 110px 70px 0 0 #ffffff, 120px 70px 0 0 #ffffff, 130px 70px 0 0 #ffffff, 140px 70px 0 0 rgba(0,0,0,0), 150px 70px 0 0 rgba(0,0,0,0), 160px 70px 0 0 rgba(0,0,0,0), 10px 80px 0 0 rgba(0,0,0,0), 20px 80px 0 0 rgba(0,0,0,0), 30px 80px 0 0 rgba(0,0,0,0), 40px 80px 0 0 rgba(0,0,0,0), 50px 80px 0 0 rgba(0,0,0,0), 60px 80px 0 0 #ffffff, 70px 80px 0 0 #ffffff, 80px 80px 0 0 #ffffff, 90px 80px 0 0 #ffffff, 100px 80px 0 0 #ffffff, 110px 80px 0 0 #ffffff, 120px 80px 0 0 #ffffff, 130px 80px 0 0 #ffffff, 140px 80px 0 0 rgba(0,0,0,0), 150px 80px 0 0 rgba(0,0,0,0), 160px 80px 0 0 rgba(0,0,0,0), 10px 90px 0 0 rgba(0,0,0,0), 20px 90px 0 0 rgba(0,0,0,0), 30px 90px 0 0 rgba(0,0,0,0), 40px 90px 0 0 rgba(0,0,0,0), 50px 90px 0 0 rgba(0,0,0,0), 60px 90px 0 0 rgba(0,0,0,0), 70px 90px 0 0 #ffffff, 80px 90px 0 0 #ffffff, 90px 90px 0 0 #ffffff, 100px 90px 0 0 #ffffff, 110px 90px 0 0 #ffffff, 120px 90px 0 0 #ffffff, 130px 90px 0 0 rgba(0,0,0,0), 140px 90px 0 0 rgba(0,0,0,0), 150px 90px 0 0 rgba(0,0,0,0), 160px 90px 0 0 rgba(0,0,0,0), 10px 100px 0 0 rgba(0,0,0,0), 20px 100px 0 0 rgba(0,0,0,0), 30px 100px 0 0 rgba(0,0,0,0), 40px 100px 0 0 rgba(0,0,0,0), 50px 100px 0 0 rgba(0,0,0,0), 60px 100px 0 0 rgba(0,0,0,0), 70px 100px 0 0 rgba(0,0,0,0), 80px 100px 0 0 #ffffff, 90px 100px 0 0 #ffffff, 100px 100px 0 0 #ffffff, 110px 100px 0 0 #ffffff, 120px 100px 0 0 rgba(0,0,0,0), 130px 100px 0 0 rgba(0,0,0,0), 140px 100px 0 0 rgba(0,0,0,0), 150px 100px 0 0 rgba(0,0,0,0), 160px 100px 0 0 #ffffff, 10px 110px 0 0 rgba(0,0,0,0), 20px 110px 0 0 rgba(0,0,0,0), 30px 110px 0 0 rgba(0,0,0,0), 40px 110px 0 0 rgba(0,0,0,0), 50px 110px 0 0 rgba(0,0,0,0), 60px 110px 0 0 rgba(0,0,0,0), 70px 110px 0 0 rgba(0,0,0,0), 80px 110px 0 0 #ffffff, 90px 110px 0 0 #ffffff, 100px 110px 0 0 #ffffff, 110px 110px 0 0 #ffffff, 120px 110px 0 0 rgba(0,0,0,0), 130px 110px 0 0 rgba(0,0,0,0), 140px 110px 0 0 rgba(0,0,0,0), 150px 110px 0 0 #ffffff, 160px 110px 0 0 rgba(0,0,0,0), 10px 120px 0 0 rgba(0,0,0,0), 20px 120px 0 0 rgba(0,0,0,0), 30px 120px 0 0 rgba(0,0,0,0), 40px 120px 0 0 rgba(0,0,0,0), 50px 120px 0 0 rgba(0,0,0,0), 60px 120px 0 0 rgba(0,0,0,0), 70px 120px 0 0 #ffffff, 80px 120px 0 0 #ffffff, 90px 120px 0 0 #ffffff, 100px 120px 0 0 #ffffff, 110px 120px 0 0 #ffffff, 120px 120px 0 0 #ffffff, 130px 120px 0 0 rgba(0,0,0,0), 140px 120px 0 0 rgba(0,0,0,0), 150px 120px 0 0 #ffffff, 160px 120px 0 0 rgba(0,0,0,0), 10px 130px 0 0 rgba(0,0,0,0), 20px 130px 0 0 rgba(0,0,0,0), 30px 130px 0 0 rgba(0,0,0,0), 40px 130px 0 0 rgba(0,0,0,0), 50px 130px 0 0 #ffffff, 60px 130px 0 0 #ffffff, 70px 130px 0 0 #ffffff, 80px 130px 0 0 #ffffff, 90px 130px 0 0 #ffffff, 100px 130px 0 0 #ffffff, 110px 130px 0 0 #ffffff, 120px 130px 0 0 #ffffff, 130px 130px 0 0 rgba(0,0,0,0), 140px 130px 0 0 rgba(0,0,0,0), 150px 130px 0 0 #ffffff, 160px 130px 0 0 rgba(0,0,0,0), 10px 140px 0 0 rgba(0,0,0,0), 20px 140px 0 0 rgba(0,0,0,0), 30px 140px 0 0 rgba(0,0,0,0), 40px 140px 0 0 rgba(0,0,0,0), 50px 140px 0 0 #ffffff, 60px 140px 0 0 #ffffff, 70px 140px 0 0 #ffffff, 80px 140px 0 0 #ffffff, 90px 140px 0 0 #ffffff, 100px 140px 0 0 #ffffff, 110px 140px 0 0 #ffffff, 120px 140px 0 0 #ffffff, 130px 140px 0 0 rgba(0,0,0,0), 140px 140px 0 0 #ffffff, 150px 140px 0 0 #ffffff, 160px 140px 0 0 rgba(0,0,0,0), 10px 150px 0 0 rgba(0,0,0,0), 20px 150px 0 0 rgba(0,0,0,0), 30px 150px 0 0 rgba(0,0,0,0), 40px 150px 0 0 #ffffff, 50px 150px 0 0 #ffffff, 60px 150px 0 0 #ffffff, 70px 150px 0 0 #ffffff, 80px 150px 0 0 #ffffff, 90px 150px 0 0 #ffffff, 100px 150px 0 0 #ffffff, 110px 150px 0 0 #ffffff, 120px 150px 0 0 #ffffff, 130px 150px 0 0 #ffffff, 140px 150px 0 0 #ffffff, 150px 150px 0 0 rgba(0,0,0,0), 160px 150px 0 0 rgba(0,0,0,0), 10px 160px 0 0 #607d8b, 20px 160px 0 0 #607d8b, 30px 160px 0 0 #607d8b, 40px 160px 0 0 #607d8b, 50px 160px 0 0 #607d8b, 60px 160px 0 0 #ffffff, 70px 160px 0 0 #ffffff, 80px 160px 0 0 #607d8b, 90px 160px 0 0 #607d8b, 100px 160px 0 0 #607d8b, 110px 160px 0 0 #ffffff, 120px 160px 0 0 #ffffff, 130px 160px 0 0 #607d8b, 140px 160px 0 0 #607d8b, 150px 160px 0 0 #607d8b, 160px 160px 0 0 #607d8b;height: 10px; width: 10px;
  }
75.01%, 100%{
  box-shadow: 10px 10px 0 0 rgba(0,0,0,0), 20px 10px 0 0 rgba(0,0,0,0), 30px 10px 0 0 rgba(0,0,0,0), 40px 10px 0 0 rgba(0,0,0,0), 50px 10px 0 0 rgba(0,0,0,0), 60px 10px 0 0 rgba(0,0,0,0), 70px 10px 0 0 #ffffff, 80px 10px 0 0 rgba(0,0,0,0), 90px 10px 0 0 rgba(0,0,0,0), 100px 10px 0 0 rgba(0,0,0,0), 110px 10px 0 0 rgba(0,0,0,0), 120px 10px 0 0 #ffffff, 130px 10px 0 0 rgba(0,0,0,0), 140px 10px 0 0 rgba(0,0,0,0), 150px 10px 0 0 rgba(0,0,0,0), 160px 10px 0 0 rgba(0,0,0,0), 10px 20px 0 0 rgba(0,0,0,0), 20px 20px 0 0 rgba(0,0,0,0), 30px 20px 0 0 rgba(0,0,0,0), 40px 20px 0 0 rgba(0,0,0,0), 50px 20px 0 0 rgba(0,0,0,0), 60px 20px 0 0 #ffffff, 70px 20px 0 0 #ffcdd2, 80px 20px 0 0 #ffffff, 90px 20px 0 0 rgba(0,0,0,0), 100px 20px 0 0 rgba(0,0,0,0), 110px 20px 0 0 #ffffff, 120px 20px 0 0 #ffcdd2, 130px 20px 0 0 #ffffff, 140px 20px 0 0 rgba(0,0,0,0), 150px 20px 0 0 rgba(0,0,0,0), 160px 20px 0 0 rgba(0,0,0,0), 10px 30px 0 0 rgba(0,0,0,0), 20px 30px 0 0 rgba(0,0,0,0), 30px 30px 0 0 rgba(0,0,0,0), 40px 30px 0 0 rgba(0,0,0,0), 50px 30px 0 0 rgba(0,0,0,0), 60px 30px 0 0 #ffffff, 70px 30px 0 0 #ffcdd2, 80px 30px 0 0 #ffcdd2, 90px 30px 0 0 #ffffff, 100px 30px 0 0 #ffffff, 110px 30px 0 0 #ffcdd2, 120px 30px 0 0 #ffcdd2, 130px 30px 0 0 #ffffff, 140px 30px 0 0 rgba(0,0,0,0), 150px 30px 0 0 rgba(0,0,0,0), 160px 30px 0 0 rgba(0,0,0,0), 10px 40px 0 0 rgba(0,0,0,0), 20px 40px 0 0 rgba(0,0,0,0), 30px 40px 0 0 rgba(0,0,0,0), 40px 40px 0 0 rgba(0,0,0,0), 50px 40px 0 0 rgba(0,0,0,0), 60px 40px 0 0 #ffffff, 70px 40px 0 0 #ffcdd2, 80px 40px 0 0 #ffffff, 90px 40px 0 0 #ffffff, 100px 40px 0 0 #ffffff, 110px 40px 0 0 #ffffff, 120px 40px 0 0 #ffcdd2, 130px 40px 0 0 #ffffff, 140px 40px 0 0 rgba(0,0,0,0), 150px 40px 0 0 rgba(0,0,0,0), 160px 40px 0 0 rgba(0,0,0,0), 10px 50px 0 0 rgba(0,0,0,0), 20px 50px 0 0 rgba(0,0,0,0), 30px 50px 0 0 rgba(0,0,0,0), 40px 50px 0 0 rgba(0,0,0,0), 50px 50px 0 0 rgba(0,0,0,0), 60px 50px 0 0 #ffffff, 70px 50px 0 0 #ffffff, 80px 50px 0 0 #ffffff, 90px 50px 0 0 #ffffff, 100px 50px 0 0 #ffffff, 110px 50px 0 0 #ffffff, 120px 50px 0 0 #ffffff, 130px 50px 0 0 #ffffff, 140px 50px 0 0 rgba(0,0,0,0), 150px 50px 0 0 rgba(0,0,0,0), 160px 50px 0 0 rgba(0,0,0,0), 10px 60px 0 0 rgba(0,0,0,0), 20px 60px 0 0 rgba(0,0,0,0), 30px 60px 0 0 rgba(0,0,0,0), 40px 60px 0 0 rgba(0,0,0,0), 50px 60px 0 0 rgba(0,0,0,0), 60px 60px 0 0 #ffffff, 70px 60px 0 0 #ffffff, 80px 60px 0 0 #000000, 90px 60px 0 0 #ffffff, 100px 60px 0 0 #ffffff, 110px 60px 0 0 #000000, 120px 60px 0 0 #ffffff, 130px 60px 0 0 #ffffff, 140px 60px 0 0 rgba(0,0,0,0), 150px 60px 0 0 rgba(0,0,0,0), 160px 60px 0 0 rgba(0,0,0,0), 10px 70px 0 0 rgba(0,0,0,0), 20px 70px 0 0 rgba(0,0,0,0), 30px 70px 0 0 rgba(0,0,0,0), 40px 70px 0 0 rgba(0,0,0,0), 50px 70px 0 0 rgba(0,0,0,0), 60px 70px 0 0 #ffffff, 70px 70px 0 0 #ffffff, 80px 70px 0 0 #ffffff, 90px 70px 0 0 #ffffff, 100px 70px 0 0 #000000, 110px 70px 0 0 #ffffff, 120px 70px 0 0 #ffffff, 130px 70px 0 0 #ffffff, 140px 70px 0 0 rgba(0,0,0,0), 150px 70px 0 0 rgba(0,0,0,0), 160px 70px 0 0 rgba(0,0,0,0), 10px 80px 0 0 rgba(0,0,0,0), 20px 80px 0 0 rgba(0,0,0,0), 30px 80px 0 0 rgba(0,0,0,0), 40px 80px 0 0 rgba(0,0,0,0), 50px 80px 0 0 rgba(0,0,0,0), 60px 80px 0 0 #ffffff, 70px 80px 0 0 #ffffff, 80px 80px 0 0 #ffffff, 90px 80px 0 0 #ffffff, 100px 80px 0 0 #ffffff, 110px 80px 0 0 #ffffff, 120px 80px 0 0 #ffffff, 130px 80px 0 0 #ffffff, 140px 80px 0 0 rgba(0,0,0,0), 150px 80px 0 0 rgba(0,0,0,0), 160px 80px 0 0 rgba(0,0,0,0), 10px 90px 0 0 rgba(0,0,0,0), 20px 90px 0 0 rgba(0,0,0,0), 30px 90px 0 0 rgba(0,0,0,0), 40px 90px 0 0 rgba(0,0,0,0), 50px 90px 0 0 rgba(0,0,0,0), 60px 90px 0 0 rgba(0,0,0,0), 70px 90px 0 0 #ffffff, 80px 90px 0 0 #ffffff, 90px 90px 0 0 #ffffff, 100px 90px 0 0 #ffffff, 110px 90px 0 0 #ffffff, 120px 90px 0 0 #ffffff, 130px 90px 0 0 rgba(0,0,0,0), 140px 90px 0 0 rgba(0,0,0,0), 150px 90px 0 0 rgba(0,0,0,0), 160px 90px 0 0 rgba(0,0,0,0), 10px 100px 0 0 rgba(0,0,0,0), 20px 100px 0 0 rgba(0,0,0,0), 30px 100px 0 0 rgba(0,0,0,0), 40px 100px 0 0 rgba(0,0,0,0), 50px 100px 0 0 rgba(0,0,0,0), 60px 100px 0 0 rgba(0,0,0,0), 70px 100px 0 0 rgba(0,0,0,0), 80px 100px 0 0 #ffffff, 90px 100px 0 0 #ffffff, 100px 100px 0 0 #ffffff, 110px 100px 0 0 #ffffff, 120px 100px 0 0 rgba(0,0,0,0), 130px 100px 0 0 rgba(0,0,0,0), 140px 100px 0 0 #ffffff, 150px 100px 0 0 rgba(0,0,0,0), 160px 100px 0 0 rgba(0,0,0,0), 10px 110px 0 0 rgba(0,0,0,0), 20px 110px 0 0 rgba(0,0,0,0), 30px 110px 0 0 rgba(0,0,0,0), 40px 110px 0 0 rgba(0,0,0,0), 50px 110px 0 0 rgba(0,0,0,0), 60px 110px 0 0 rgba(0,0,0,0), 70px 110px 0 0 rgba(0,0,0,0), 80px 110px 0 0 #ffffff, 90px 110px 0 0 #ffffff, 100px 110px 0 0 #ffffff, 110px 110px 0 0 #ffffff, 120px 110px 0 0 rgba(0,0,0,0), 130px 110px 0 0 rgba(0,0,0,0), 140px 110px 0 0 rgba(0,0,0,0), 150px 110px 0 0 #ffffff, 160px 110px 0 0 rgba(0,0,0,0), 10px 120px 0 0 rgba(0,0,0,0), 20px 120px 0 0 rgba(0,0,0,0), 30px 120px 0 0 rgba(0,0,0,0), 40px 120px 0 0 rgba(0,0,0,0), 50px 120px 0 0 rgba(0,0,0,0), 60px 120px 0 0 rgba(0,0,0,0), 70px 120px 0 0 #ffffff, 80px 120px 0 0 #ffffff, 90px 120px 0 0 #ffffff, 100px 120px 0 0 #ffffff, 110px 120px 0 0 #ffffff, 120px 120px 0 0 #ffffff, 130px 120px 0 0 rgba(0,0,0,0), 140px 120px 0 0 rgba(0,0,0,0), 150px 120px 0 0 #ffffff, 160px 120px 0 0 rgba(0,0,0,0), 10px 130px 0 0 rgba(0,0,0,0), 20px 130px 0 0 rgba(0,0,0,0), 30px 130px 0 0 rgba(0,0,0,0), 40px 130px 0 0 rgba(0,0,0,0), 50px 130px 0 0 #ffffff, 60px 130px 0 0 #ffffff, 70px 130px 0 0 #ffffff, 80px 130px 0 0 #ffffff, 90px 130px 0 0 #ffffff, 100px 130px 0 0 #ffffff, 110px 130px 0 0 #ffffff, 120px 130px 0 0 #ffffff, 130px 130px 0 0 rgba(0,0,0,0), 140px 130px 0 0 rgba(0,0,0,0), 150px 130px 0 0 #ffffff, 160px 130px 0 0 rgba(0,0,0,0), 10px 140px 0 0 rgba(0,0,0,0), 20px 140px 0 0 rgba(0,0,0,0), 30px 140px 0 0 rgba(0,0,0,0), 40px 140px 0 0 rgba(0,0,0,0), 50px 140px 0 0 #ffffff, 60px 140px 0 0 #ffffff, 70px 140px 0 0 #ffffff, 80px 140px 0 0 #ffffff, 90px 140px 0 0 #ffffff, 100px 140px 0 0 #ffffff, 110px 140px 0 0 #ffffff, 120px 140px 0 0 #ffffff, 130px 140px 0 0 rgba(0,0,0,0), 140px 140px 0 0 #ffffff, 150px 140px 0 0 #ffffff, 160px 140px 0 0 rgba(0,0,0,0), 10px 150px 0 0 rgba(0,0,0,0), 20px 150px 0 0 rgba(0,0,0,0), 30px 150px 0 0 rgba(0,0,0,0), 40px 150px 0 0 #ffffff, 50px 150px 0 0 #ffffff, 60px 150px 0 0 #ffffff, 70px 150px 0 0 #ffffff, 80px 150px 0 0 #ffffff, 90px 150px 0 0 #ffffff, 100px 150px 0 0 #ffffff, 110px 150px 0 0 #ffffff, 120px 150px 0 0 #ffffff, 130px 150px 0 0 #ffffff, 140px 150px 0 0 #ffffff, 150px 150px 0 0 rgba(0,0,0,0), 160px 150px 0 0 rgba(0,0,0,0), 10px 160px 0 0 #607d8b, 20px 160px 0 0 #607d8b, 30px 160px 0 0 #607d8b, 40px 160px 0 0 #607d8b, 50px 160px 0 0 #607d8b, 60px 160px 0 0 #ffffff, 70px 160px 0 0 #ffffff, 80px 160px 0 0 #607d8b, 90px 160px 0 0 #607d8b, 100px 160px 0 0 #607d8b, 110px 160px 0 0 #ffffff, 120px 160px 0 0 #ffffff, 130px 160px 0 0 #607d8b, 140px 160px 0 0 #607d8b, 150px 160px 0 0 #607d8b, 160px 160px 0 0 #607d8b;height: 10px; width: 10px;
  }
}
</style>
<script>
import axios from "axios";
import RadarChart from '../../components/RadarChart.vue'

export default {
  components: {
    RadarChart
  },
  data() {
    return {
      videoStream: null,
      cameras: [],
      selectedCameraId: null,
      emotion: null,
      eyes_status: null,
      isProcessing: false,
      hasProcessed: true,


      dragging: false,
      rightPos: 200,
      bottomPos: 200,
      startX: 0,
      startY: 0,
      deltaX: 0,
      deltaY: 0,
      radarChartData: {
        labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
        datasets: [
          {
            label: 'Emotions',
            data: [3.83, 0.00, 8.62, 4.28, 24.25, 0.19, 58.96]
          }
        ]
      },
      radarChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scale: {
          ticks: { beginAtZero: true }
        }
      }
    };
  },
  async created() {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      this.cameras = devices.filter(device => device.kind === "videoinput");
      if (this.cameras.length > 0) {
        this.selectedCameraId = this.cameras[0].deviceId;
      }
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.renderChart(this.chartData, this.options)
    })
  },
  methods: {
    async startDrag(event) {
      this.dragging = true;
      this.startX = event.clientX;
      this.startY = event.clientY;
    },
    async onDrag(event) {
      if (this.dragging) {
        this.deltaX = event.clientX - this.startX;
        this.deltaY = event.clientY - this.startY;
        this.startX = event.clientX;
        this.startY = event.clientY;

        // Update the position of the .cat div
        const catElement = event.target;
        catElement.style.right = `${parseInt(catElement.style.right, 10) - this.deltaX}px`;
        catElement.style.bottom = `${parseInt(catElement.style.bottom, 10) - this.deltaY}px`;
      }
    },
    async endDrag() {
      this.dragging = false;
    },
    
    async startCamera() {
      if (!this.selectedCameraId) {
        console.error("No camera selected");
        return;
      }
      try {
        const constraints = {
          video: {
            deviceId: this.selectedCameraId
          }
        };
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        this.videoStream = stream;
        this.$nextTick(() => {
          this.$refs.videoElement.srcObject = stream;
        });
        this.isProcessing = true;
        this.processVideoFrame();
      } catch (error) {
        console.error("Error starting camera:", error);
      }
    },

    stopCamera() {
      this.isProcessing = false;
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
        this.videoStream = null;
        this.$refs.videoElement.srcObject = null;
      }
    },

    async processVideoFrame() {
      if (this.isProcessing && this.videoStream && this.hasProcessed) {
        this.hasProcessed = false;
        await this.captureAndSendFrame();
        requestAnimationFrame(this.processVideoFrame);
      }
    },

    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },

    async captureAndSendFrame() {
      const canvas = document.createElement("canvas");
      await this.$nextTick();
      canvas.width = this.$refs.videoElement.videoWidth;
      canvas.height = this.$refs.videoElement.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(this.$refs.videoElement, 0, 0);
      return new Promise((resolve) => {
        canvas.toBlob(async (blob) => {
          if (!blob) {
            console.error("Failed to create blob from canvas.");
            this.hasProcessed = true;
            resolve();
            return;
          }
          const formData = new FormData();
          formData.append("file", blob, "frame.jpg");
          try {
            const response = await axios.post("http://localhost:8000/process_frame", formData, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            });

            console.log("Response:", response.data); 
            
            this.emotion = response.data.emotion;
            this.eyes_status = response.data.eyes_status;
            await this.sleep(5000)
          } catch (error) {
            console.error("Error sending frame:", error);
          } finally {
            this.hasProcessed = true;
            resolve();
          }
        }, "image/jpeg");
      });
    }
    
  }
};
</script>
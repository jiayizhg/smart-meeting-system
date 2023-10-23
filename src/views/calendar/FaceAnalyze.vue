<template>
  <div>
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
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      videoStream: null,
      cameras: [],
      selectedCameraId: null,
      emotion: null,
      eyes_status: null,
      isProcessing: false,
      hasProcessed: true
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
  methods: {
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
            const response = await axios.post("http://localhost:5000/process_frame", formData, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            });
            console.log("Response:", response.data); 
            this.emotion = response.data.emotion;
            this.eyes_status = response.data.eyes_status;
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
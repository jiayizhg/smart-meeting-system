<template>
  <div>
    <br/>
    <Login @logInResult="handleDataFromChild"/>
    <div v-if="isLogIn">
      <div v-if="!isProcessing">
        <div class="chart-container" v-if="emotion">
          <RadarChart v-if="emotion" :width="300" :height="300"
            :external-chart-data="radarAnalysisData" :external-chart-options="radarChartOptions"/>
        </div>
      </div>
      <div v-if="isProcessing">
        <div class="chart-container" v-if="emotion">
          <div>
          <RadarChart v-if="emotion" :width="300" :height="300"
            :external-chart-data="radarChartData" :external-chart-options="radarChartOptions"/>
          </div>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <div>
            <select v-model="selectedEmotion" class="elegant-select">
            <option value="angry">Angry</option>
            <option value="disgust">Disgust</option>
            <option value="fear">Fear</option>
            <option value="happy">Happy</option>
            <option value="sad">Sad</option>
            <option value="surprise">Surprise</option>
            <option value="neutral">Neutral</option>
            </select>
            <LineChart v-if="emotion" :width="300" :height="300"
              :external-chart-data="lineChartData" :external-chart-options="lineChartOptions"/>
          </div>
        </div>
        <div v-if="emotion">
          <!-- <h3>Emotions:</h3> -->
          <!-- <ul>
            <li v-for="(value, key) in emotion" :key="key">
              {{ key }}: {{ value.toFixed(2) }}%
            </li>
          </ul> -->
        </div>
        <div v-if="eyes_status">
          <h3>Eyes Focus Analysis:</h3>
          Left Eye: {{ eyes_status.left_eye }}<br>
          Left Eye Focus:{{ eyes_status.left_eye_direction }}<br>
          Right Eye: {{ eyes_status.right_eye }}<br>
          Right Eye Focus:{{ eyes_status.right_eye_direction }}<br>
        </div>
      </div>
        <p class="pheader"><b>Join Meeting Room</b></p>
      <div style="display: flex; flex-direction: row; justify-content: space-around;">
        <div>
        <form @submit.prevent="createMeetingRoom">
          <div>
            <label for="title">Title:&nbsp;</label>
            <input type="text" id="title" v-model="meetingRoom.title">
          </div>
          <button type="submit" style="width: ">Create Meeting Room</button>
        </form>
        <div v-if="meeting_message">{{ meeting_message }}</div>
        </div>
        <div>
        <form @submit.prevent="addUserToMeetingRoom">
        <div>
          <label for="meetingRoomId">Meeting Room ID:&nbsp;&nbsp;</label>
          <input type="text" id="meetingRoomId" v-model="participant.meeting_room_id">
        </div>
        <div>
          <label for="userId">User ID:&nbsp;&nbsp;&nbsp;&nbsp;</label>
          <input type="text" id="userId" v-model="participant.user_id">
        </div>
        <button type="submit">Join By Room ID</button>
        </form>
        <div v-if="add_message">{{ add_message }}</div>
        </div>
      </div>
      <div>
      </div>
      <p class="pheader"><b>Invite and Manage Participants</b></p>
      
        
        <div>
            <form @submit.prevent="addUserToMeetingRoom">
          <div>
            <label for="meetingRoomId">Meeting Room ID:&nbsp;&nbsp;</label>
            <input type="text" id="meetingRoomId" v-model="participant_2.meeting_room_id">
          </div>
          <div>
            <label for="userId">User ID:&nbsp;&nbsp;&nbsp;&nbsp;</label>
            <input type="text" id="userId" v-model="participant_2.user_id">
          </div>
          <div>
            <label for="role">Role:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
            <input type="text" id="role" v-model="participant_2.role">
          </div>
          <button type="submit" style="width: 20%;">Add User</button>
          </form>
          <div v-if="add_message_2">{{ add_message_2 }}</div>
        
      </div>
      <p class="pheader"><b>Chat Room</b></p>
      <div style="display: flex; flex-direction: row; justify-content:space-around; width:100%;">
        <div style="width: 35%;">
          <p class="pheader">Chat With Target</p>
          <div>
            <label for="meetingRoomId">Meeting Room ID:</label>
            <input type="number" id="meetingRoomId" v-model="meetingRoomId">
            <button @click="fetchParticipants">Get Participants</button>
          </div>
          <div v-if="participants.length > 0">
            <h4><b>Participants</b></h4>
            <ul>
              <li v-for="participant in participants" :key="participant.id">
                <b>User ID:</b> {{ participant.user_id }}, <b>Role:</b> {{ participant.role }}
              </li>
            </ul>
          </div>
        </div>
        <div style="width: 35%;">
          <p class="pheader" >Chat In Meeting Room</p>
        </div>
      </div>

      <p class="pheader"><b>Select Your Analyze Camera</b></p>
      <select v-model="selectedCameraId" class="elegant-select" style="width: 35%;">
        <option v-for="camera in cameras" :key="camera.deviceId" :value="camera.deviceId">
          {{ camera.label }}
        </option>
      </select>

      <br/>
      <br/>
      <button  v-if="!videoStream" @click="startCamera">Start Meeting</button>
      <button v-if="videoStream" @click="stopCamera">Leave Meeting</button>
      <video v-if="videoStream" ref="videoElement" autoplay playsinline></video>
      <div class="cat"  :style="{ right: rightPos + 'px', bottom: bottomPos + 'px' }"
      @mousedown.prevent="startDrag"
      @mousemove="onDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag">
      </div>
    </div>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
  </div>
</template>

<style scoped>
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

.pheader{
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  color: #333;
  background-color: #f2f2f2;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px 20px;
  margin: 10px;
  transition: all 0.3s ease;
}

.pheader:hover{
  background-color: #e8e8e8;
  color: #555;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-container > * {
  margin: 10px;
}


.elegant-select {
  width: 100%; 
  padding: 5px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  font-size: 16px; 
  color: #333;
}

.elegant-select::-ms-expand {
  display: none;
}

.elegant-select::after {
  content: '\25BC';
  font-size: 12px;
  color: #aaa;
  right: 10px;
  top: calc(50% - 2px);
  position: absolute;
  pointer-events: none;
}

.elegant-select:focus {
  border-color: #66afe9;
  outline: 0;
  box-shadow: 0 0 8px rgba(102, 175, 233, .6);
}

button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>
<script>
import axios from "axios";
import RadarChart from '../../components/RadarChart.vue'
import LineChart from '../../components/LineChart.vue'
import Login from "../../components/Login.vue";


export default {
  components: {
    RadarChart,
    LineChart,
    Login
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

      startDate: null,
      endDate: null,

      userIDStored:null,
      userNameStored:null,
      
      selectedEmotion:'neutral',

      meetingRoom: {
        title: '',
        host_id: ''
      },
      meeting_message: '',
      participant: {
        meeting_room_id: '',
        user_id: '',
        role: 'participant'
      },
      add_message:'',
      participant_2: {
        meeting_room_id: '',
        user_id: '',
        role: ''
      },
      add_message_2:'',
      meetingRoomId: null,
      participants: [],
      radarAnalysisData: {
        labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
        datasets: [
          {
            label: 'Emotions',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            pointBackgroundColor: 'rgba(255,99,132,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(255,99,132,1)',
            data: [0, 0, 0, 0, 0, 0, 100]
          }
        ]
      },

      radarChartData: {
        labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
        datasets: [
          {
            label: 'Emotions',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            pointBackgroundColor: 'rgba(255,99,132,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(255,99,132,1)',
            data: [0, 0, 0, 0, 0, 0, 100]
          }
        ]
      },
      radarChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scale: {
          ticks: { beginAtZero: true }
        }
      },
      lineChartData: {
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
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      }
    };
    
  },
  async created() {
    const userString = sessionStorage.getItem('user');
    if (userString) {
        this.isLogIn = true;
        const userData = JSON.parse(userString);
        this.userIDStored = userData.id;
        this.userNameStored = userData.name;
    }
    
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      this.cameras = devices.filter(device => device.kind === "videoinput");
      if (this.cameras.length > 0) {
        this.selectedCameraId = this.cameras[0].deviceId;
      }
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
    this.timer = setInterval(()=>{this.refreshLineChart()}, 3000);
  },
  watch: {
    emotion(newVal) {
      let radarData = [newVal.angry,newVal.disgust,newVal.fear,newVal.happy,newVal.sad,newVal.surprise,newVal.neutral]
      // this.radarChartData["datasets"]["data"]=radarData
      this.radarChartData={
        labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
        datasets: [
          {
            label: 'Emotions',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            pointBackgroundColor: 'rgba(255,99,132,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(255,99,132,1)',
            data: radarData
          }
        ]
      }
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  // mounted () {
  //   let radarData = [100, 100, 0, 0, 0, 0, 100]
  //   this.radarChartData={
  //       labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
  //       datasets: [
  //         {
  //           label: 'Emotions',
  //           backgroundColor: 'rgba(255,99,132,0.2)',
  //           borderColor: 'rgba(255,99,132,1)',
  //           pointBackgroundColor: 'rgba(255,99,132,1)',
  //           pointBorderColor: '#fff',
  //           pointHoverBackgroundColor: '#fff',
  //           pointHoverBorderColor: 'rgba(255,99,132,1)',
  //           data: radarData
  //         }
  //       ]
  //     }
  // },
  // mounted () {
  //   this.$nextTick(() => {
  //     this.renderChart(this.chartData, this.options)
  //   })
  // },

  methods: {
    createMeetingRoom() {
      this.meetingRoom.host_id=this.userIDStored;
      axios.post('http://localhost:8000/create_meeting_room', this.meetingRoom)
        .then(response => {
          this.meeting_message = response.data.message;
          this.meetingRoomId=response.meeting_room_id;
        })
        .catch(error => {
          console.error('There was an error!', error);
          this.meeting_message = error.response.data.detail || 'Error creating meeting room';
        });
    },
    addUserToMeetingRoom() {
      this.meetingRoomId=this.participant.id
      axios.post('http://localhost:8000/add_user_to_meeting_room', this.participant)
        .then(response => {
          this.add_message = response.data.message;
        })
        .catch(error => {
          console.error('There was an error!', error);
          this.add_message = error.response.data.detail || 'Error adding user to meeting room';
        });
    },
    addUserToMeetingRoom_2() {
      axios.post('http://localhost:8000/add_user_to_meeting_room', this.participant_2)
        .then(response => {
          this.add_message_2 = response.data.message;
        })
        .catch(error => {
          console.error('There was an error!', error);
          this.add_message_2 = error.response.data.detail || 'Error adding user to meeting room';
        });
    },
    fetchParticipants() {
      if (this.meetingRoomId) {
        axios.get(`http://localhost:8000/meeting_room_participants?meeting_room_id=${this.meetingRoomId}`)
          .then(response => {
            this.participants = response.data;
            if (this.participants.length === 0) {
              this.message = 'No participants found for this meeting room.';
            }
          })
          .catch(error => {
            console.error('There was an error!', error);
            this.message = error.response.data.detail || 'Error fetching participants';
          });
      } else {
        this.message = 'Please enter a meeting room ID.';
      }
    },
    handleDataFromChild(data){
      console.log('LogIn result:', data);
      this.isLogIn=true
      this.userIDStored = data.id;
      this.userNameStored = data.name;
      location.reload() 
    },
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
        // this.startDate= this.formatDateToEasternTime(new Date());
        // this.endDate= new Date();
        // this.endDate.setTime(this.endDate.getTime() + (3 * 60 * 60 * 1000));
        // this.endDate= this.formatDateToEasternTime(this.endDate);
        this.startDate= new Date();
        this.startDate.setTime(this.startDate.getTime() + (5 * 60 * 60 * 1000));
        this.startDate= this.formatDateToEasternTime(this.startDate);
        this.endDate= new Date();
        this.endDate.setTime(this.endDate.getTime() + (8 * 60 * 60 * 1000));
        this.endDate= this.formatDateToEasternTime(this.endDate);  
        this.processVideoFrame();
      } catch (error) {
        console.error("Error starting camera:", error);
      }
    },

    async stopCamera() {
      this.isProcessing = false;
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
        this.videoStream = null;
        this.$refs.videoElement.srcObject = null;
        await this.getRadarAnalysis();
      }
    },
    convertUTCToEasternTime(date) {
      const EST_OFFSET = 5;
      const EDT_OFFSET = 4; 
      const janOffset = new Date(date.getFullYear(), 0, 1).getTimezoneOffset();
      const junOffset = new Date(date.getFullYear(), 5, 1).getTimezoneOffset();
      let currentOffset = date.getTimezoneOffset();
      let dst = (janOffset !== junOffset && currentOffset === Math.min(janOffset, junOffset));
      let utc = date.getTime() + (currentOffset * 60000);
      let easternTime = new Date(utc - (dst ? EDT_OFFSET : EST_OFFSET) * 3600000);
      return easternTime;
    },
    formatDateToEasternTime(date) {
      let year = date.getFullYear();
      let month = String(date.getMonth() + 1).padStart(2, '0');
      let day = String(date.getDate()).padStart(2, '0');
      let hours = String(date.getHours()).padStart(2, '0');
      let minutes = String(date.getMinutes()).padStart(2, '0');
      let seconds = String(date.getSeconds()).padStart(2, '0');

      return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
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
      const ref=this;
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
          formData.append("user_id", ref.userIDStored);
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
    },
    updateChartData(jsonData) {
      const labels = jsonData.map(item => {
        return item.update_time.split('T')[1];
      });

      const data = jsonData.map(item => {
        return item.emotion_data;
      });

      this.lineChartData = {
        labels: labels,
        datasets: [
          {
            label: this.selectedEmotion.charAt(0).toUpperCase() + this.selectedEmotion.slice(1)+' Emotion Time Series',
            backgroundColor: '#f87979',
            borderColor: '#b0569a',
            data: data
          }
        ]
      };
    },
    async refreshLineChart(user_id=this.userIDStored, emotion_type=this.selectedEmotion) {
      if(!this.isProcessing) return;
      const ref = this;
      console.log("Emotion Series Collect Start:");
      const baseUrl= "http://localhost:8000/get_user_emotion_data/"
      // const url = `${baseUrl}${user_id}/${emotion_type}/${encodeURIComponent(this.startDate)}/${encodeURIComponent(this.endDate)}`;
      // try {
      //       const response = await axios.get(url);

      //       console.log("Emotion Series Response:", response.data); 
      //       this.updateChartData(response.data);
      //     } 
      // catch (error) {
      //     console.error("Error Geting Emotion Series:", error);
      // }

      // axios.get(`http://localhost:8000/get_user_emotion_data/${user_id}/${emotion_type}/${this.startDate}/${this.endDate}`)
      // .then(function (response) {
      //   console.log(response.data);
      // })
      // .catch(function (error) {
      //   console.log(error);
      // });

      axios({
        method: 'get',
        url: baseUrl, 
        params: {
          'user_id': user_id,
          'emotion_type': emotion_type,
          'start_date': this.startDate,
          'end_date': this.endDate
        },
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then(function (response) {
          console.log(response.data);
          ref.updateChartData(response.data);
      })
      .catch(function (error) {
          console.log(error); 
      });
      
    },
    updateRadarChartData(data) {

      console.log(data)
      let radarData = [data.avg_angry,data.avg_disgust,data.avg_fear,data.avg_happy,data.avg_sad,data.avg_surprise,data.avg_neutral]
      // this.radarChartData["datasets"]["data"]=radarData
      this.radarAnalysisData={
        labels: ['Average Angry', 'Average Disgust', 'Average Fear', 'Average Happy', 'Average Sad', 'Average Surprise', 'Average Neutral'],
        datasets: [
          {
            label: 'Emotions',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            pointBackgroundColor: 'rgba(255,99,132,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(255,99,132,1)',
            data: radarData
          }
        ]
      }
    },
    async getRadarAnalysis(user_id=this.userIDStored) {
      // if(!this.isProcessing) return;
      const ref = this;
      console.log("Emotion Analysis for this meeting:");
      const baseUrl= "http://localhost:8000/get_emotion_statistics"
      axios({
        method: 'get',
        url: baseUrl, 
        params: {
          'user_id': user_id,
        },
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then(function (response) {
          console.log(response.data);
          ref.updateRadarChartData(response.data);
      })
      .catch(function (error) {
          console.log(error); 
      });
      
    },
    
    
  }
};
</script>
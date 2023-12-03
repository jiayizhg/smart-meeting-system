<template>
  
   <div class="Home">
    <h1>Smart Meeting System</h1>

  <!-- <div class="container">
    <div class="left">
      <form >
        <input type="search" placeholder="Search meetings, team members, and schedules">
        <button type="submit">Search</button>
      </form>
    </div>

    <div class="right">
      <router-link to="/scheduling"><font-awesome-icon :icon="['fas', 'circle-user']"  class="user"/>Hello, there!</router-link>
    </div>
    

  </div>    -->
  <!-- <div class="long-title">
      <h3>Tasks for Employees (USA Office)</h3>
    </div>
    <DxScheduler
      :data-source="dataSource"
      :current-date="currentDate"
      :views="views"
      :height="500"
      :editing="false"
      :show-all-day-panel="false"
      :start-day-hour="7"
      start-date-expr="start.dateTime"
      end-date-expr="end.dateTime"
      text-expr="summary"
      time-zone="America/Los_Angeles"
      current-view="workWeek"
    /> -->
    <calendar />
</div>
</template>

<script>
// import 'whatwg-fetch';
// import DxScheduler from 'devextreme-vue/scheduler';
import CustomStore from 'devextreme/data/custom_store';

import Calendar from './calendar.vue';



export default {
  components: {
    // DxScheduler,
    Calendar
  },
  data() {
    return {
      views: ['day', 'workWeek', 'month'],
      currentDate: new Date(2023, 11, 25),
      dataSource: new CustomStore({
        load: (options) => this.getData(options, { showDeleted: false }),
      }),
    };
  },
  // methods: {
  //   getData(_, requestOptions) {
  //     const PUBLIC_KEY = 'AIzaSyB3Yrl7uPAOoCxZ3m3K4mQmcBncSi1AJ9c';
  //     const CALENDAR_ID = 'primary';
  //     const dataUrl = ['https://www.googleapis.com/auth/calendar',
  //       CALENDAR_ID, '/events?key=', PUBLIC_KEY].join('');

  //     return fetch(dataUrl, requestOptions).then(
  //       (response) => response.json(),
  //     ).then((data) => data.items);
  //   },
  // },
};
</script>

<!-- 
const CLIENT_ID = '737463276639-2uvkfra1rt9185d369u2ct0ilk76hegq.apps.googleusercontent.com'
const API_KEY = 'AIzaSyB3Yrl7uPAOoCxZ3m3K4mQmcBncSi1AJ9c'
const DISCOVERY_DOCS = 'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
const SCOPES = 'https://www.googleapis.com/auth/calendar'
 -->

<style scoped>
.long-title h3 {
  font-family:
    'Segoe UI Light',
    'Helvetica Neue Light',
    'Segoe UI',
    'Helvetica Neue',
    'Trebuchet MS',
    Verdana;
  font-weight: 200;
  font-size: 28px;
  text-align: center;
  margin-bottom: 20px;
}
.hello-message {
  font-size: 16px;
  padding-top: 15px;
}
.right {
  width: 40%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}
.user {
  font-size: 40px;
  margin-right: 10px;
}

.container {
  padding-top: 2vh;
  display: flex;
}

.left {
  width: 60%;
  justify-content: flex-start;
  position: relative;
  left: -55px;
}

form {
  border: 1px solid black;
  justify-content: flex-start;
  display: flex;
  align-items: center;
}

input[type="search"] {
  border: none;
  background: transparent;
  margin-left: 20px;
  padding: 7px 8px;
  font-size: 14px;
  color: inherit;
  border: 1px solid transparent;
  border-radius: inherit;
  width: 100%;
}

input[type="search"]::placeholder {
  color: #bbb;
}

button[type="submit"] {
  text-indent: -999px;
  overflow: hidden;
  width: 40px;
  border: 1px solid transparent;
  border-radius: inherit;
  background: transparent url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' class='bi bi-search' viewBox='0 0 16 16'%3E%3Cpath d='M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z'%3E%3C/path%3E%3C/svg%3E") no-repeat center;
  cursor: pointer;
  opacity: 0.7;
}

button[type="submit"]:hover {
  opacity: 1;
}

button[type="submit"]:focus,
input[type="search"]:focus {
  box-shadow: 0 0 3px 0 #1183d6;
  border-color: #1183d6;
  outline: none;
}



</style>
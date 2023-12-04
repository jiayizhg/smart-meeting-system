<template>
  <div id="scheduling" class="grid-container">
    <div class="left-side">
      <!-- Your calendar component goes here -->
      <calendar
        :authorized="authorized"
        :events="events"
        :jsonData1="jsonData1"
        :jsonDatas="jsonDatas"
      />
    </div>
    <div class="right-side">
      <div class="header">
        <button @click="handleAuthClick">Authorize</button>
        <button @click="handleSignOutClick">Sign Out</button>
      </div>

      <div id="sc" class="sc_class">
        <h1>AI Meeting Scheduler</h1>

        <div class="form-group">
          <label for="email">Enter your email address:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Email Address"
          />
          <button @click="submitEmail">Submit</button>
        </div>

        <div class="form-group">
          <label for="duration">Enter your Time Duration:</label>
          <input
            type="number"
            id="duration"
            v-model="duration"
            placeholder="Time Duration"
          />
          <button @click="submitDuration">Submit</button>

          <!-- <div>
                <ul>
                    <li v-for="item in optimizedTimes" :key="item.start">
                        {{ item.start }} - {{ item.end }}
                    </li>
                </ul>
            </div> -->
            <div class="popup" v-if="showPopup">
            <span class="close-btn" @click="closePopup">&times;</span>
            <h2>Optimized Meeting Times</h2>
            <ul>
              <li v-for="item in optimizedTimes" :key="item.start">
                {{ item.start }} - {{ item.end }}
              </li>
            </ul>
          </div>
        </div>

        <div class="form-group">
          <h3>Create Google Calendar Event</h3>
          <form @submit.prevent="createEvent">
            <label for="eventTitle">Event Title:</label>
            <input type="text" id="eventTitle" v-model="eventTitle" required />
            <br />
            <label for="eventDate">Event Date:</label>
            <input type="date" id="eventDate" v-model="eventDate" required />
            <br />
            <label for="sTime">Start Time:</label>
            <input type="time" id="sTime" v-model="sTime" required />
            <br />
            <label for="eTime">End Time:</label>
            <input type="time" id="eTime" v-model="eTime" required />
            <br />
            <label for="eventLocation">Event Location (Zoom URL):</label>
            <input
              type="text"
              id="eventLocation"
              v-model="eventLocation"
              required
            />
            <br />
            <button type="submit">Create Event</button>
          </form>
        </div>
      </div>
    </div>

    <!-- <calendar
      :authorized="authorized"
      :events="events"
      :jsonData1="jsonData1"
      :jsonDatas="jsonDatas"
    /> -->
  </div>
</template>
  
  <script src="https://apis.google.com/js/platform.js"></script>
  <script>
// import {useAuthStore} from "@/stores/AuthStore"
// const AuthStore = useAuthStore();

import calendar from "../../components/calendar.vue";

const CLIENT_ID =
  "737463276639-2uvkfra1rt9185d369u2ct0ilk76hegq.apps.googleusercontent.com";
const API_KEY = "AIzaSyB3Yrl7uPAOoCxZ3m3K4mQmcBncSi1AJ9c";
const DISCOVERY_DOCS =
  "https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest";
const SCOPES = "https://www.googleapis.com/auth/calendar";

export default {
  name: "scheduling",

  components: {
    calendar,
  },

  data() {
    return {
      authorized: false,
      items: undefined,
      events: [],
      jsonData1: [],
      jsonData2: [],
      jsonDatas: [],
      optimizedTimes: [],
      eventTitle: "",
      eventDate: "",
      sTime: "",
      eTime: "",
      eventLocation: "",
      showPopup: false,
    };
  },
  created() {
    this.api = gapi;
    this.handleClientLoad();
  },
  methods: {
    closePopup() {
    this.showPopup = false;
    console.log(this.showPopup);

  },
    convertDateTime(dateTime) {
      const date = new Date(dateTime);
      const formattedDateTime = `${date.getFullYear()}-${(date.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")} ${date
        .getHours()
        .toString()
        .padStart(2, "0")}:${date
        .getMinutes()
        .toString()
        .padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;
      return formattedDateTime;
    },

    handleClientLoad() {
      this.api.load("client:auth2", this.initClient);
    },
    initClient() {
      let vm = this;
      vm.api.client
        .init({
          apiKey: API_KEY,
          clientId: CLIENT_ID,
          discoveryDocs: DISCOVERY_DOCS,
          scope: SCOPES,
          cookie_policy: "single_host_origin",
          plugin_name: "login",
        })
        .then((_) => {
          vm.api.auth2.getAuthInstance().isSignedIn.listen(vm.authorized);
        });
    },
    handleAuthClick(event) {
      Promise.resolve(this.api.auth2.getAuthInstance().signIn()).then((_) => {
        this.authorized = true;
        console.log("User logged in");

        // const attendees = ['yuminw22@gmail.com', 'jiayi10zhang@gmail.com'];

        // attendees.forEach((attendee) => {
        //     console.log("11111");

        //             this.api.client.load('calendar', 'v3', () => {
        //     this.api.client.calendar.events.list({
        //         calendarId: attendee,
        //             timeMin: (new Date()).toISOString(),
        //             showDeleted: false,
        //             singleEvents: true,
        //             orderBy: 'startTime',
        // }) .then(response => {
        //                 console.log("22222222");
        //             const events_attendees = response.result.items;
        //             if (!events_attendees.events || events_attendees.events.length == 0) {
        //         console.log("no events")
        //         return;
        //     }

        //             // Display the events in the attendee's Google Calendar
        //             events.forEach((events_attendees) => {
        //                 console.log(events_attendees.summary);
        //                 console.log(events_attendees.start.dateTime);
        //                 console.log(events_attendees.end.dateTime);

        //                         });
        //                     });
        //             });
        //         });
        this.getEvents();
      });
    },
    handleSignOutClick(event) {
      Promise.resolve(this.api.auth2.getAuthInstance().signOut()).then((_) => {
        this.authorized = false;
        this.jsonData1 = [];
        this.events = [];
        this.jsonData2 = [];
        this.jsonDatas = [];
        this.getEvents();
        console.log("User signed out.");
      });
    },
    // "2023-12-17T11:42:00-05:00",
    // yyyy-mm-dd HH:MM:SS
    dateConvetor(s) {
      const inputString = s.toString();
      console.log(inputString);

      const date = new Date(inputString);
      const easternTime = new Date(
        date.toLocaleString("en-US", { timeZone: "America/New_York" })
      );

      const year = easternTime.getFullYear();
      const month = String(easternTime.getMonth() + 1).padStart(2, "0");
      const day = String(easternTime.getDate()).padStart(2, "0");
      const hours = String(easternTime.getHours()).padStart(2, "0");
      const minutes = String(easternTime.getMinutes()).padStart(2, "0");
      const seconds = String(easternTime.getSeconds()).padStart(2, "0");

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    getEvents() {
      var vm = this;
      vm.api.client.load("calendar", "v3", () => {
        vm.api.client.calendar.events
          .list({
            calendarId: "primary",
            //'timeMin': (new Date()).toISOString(),
            showDeleted: false,
            singleEvents: true,
            maxResults: 10000000,
            orderBy: "startTime",
          })
          .then((response) => {
            vm.events = response.result.items;

            if (!vm.events || vm.events.length == 0) {
              console.log("no events");
              return;
            }
            // Flatten to string to display
            const output = vm.events.reduce(
              (str, event) =>
                `${str}${event.summary} (${
                  event.start.dateTime || event.start.date
                })\n`,
              "Events:\n"
            );
            console.log(output);
            var resultA = [];
            var pv = {};
            var ref = this;
            vm.events.reduce(function (std, event) {
              pv = {};
              pv["title"] = `${event.summary}`;
              pv["id"] = `${event.id}`;
              //
              pv["startDate"] = event.start.dateTime
                ? ref.dateConvetor(event.start.dateTime)
                : event.start.date;

              pv["endDate"] = event.end.dateTime
                ? ref.dateConvetor(event.end.dateTime)
                : event.end.date;

              console.log("NO");
              // return pv;
              resultA.push(pv);
              return std;
            }, {});
            console.log(JSON.stringify(resultA));
            console.log(JSON.parse(JSON.stringify(resultA)));
            this.jsonData1 = JSON.parse(JSON.stringify(resultA));
            console.log(this.jsonData1);
            // "2023-12-17T11:42:00-05:00",
            // yyyy-mm-dd HH:MM:SS
          });
      });
    },
    submitEmail() {
      // Pass the email address to a function
      this.getAttendeesEvents(this.email);
    },
    getAttendeesEvents(email) {
      var vm = this;
      vm.api.client.load("calendar", "v3", () => {
        vm.api.client.calendar.events
          .list({
            calendarId: email,
            //'timeMin': (new Date()).toISOString(),
            showDeleted: false,
            singleEvents: true,
            maxResults: 10000000,
            orderBy: "startTime",
          })
          .then((response) => {
            vm.events = response.result.items;

            if (!vm.events || vm.events.length == 0) {
              console.log("no events");
              return;
            }
            // Flatten to string to display
            const output = vm.events.reduce(
              (str, event) =>
                `${str}${event.summary} (${
                  event.start.dateTime || event.start.date
                })\n`,
              "Events:\n"
            );
            console.log(output);
            var resultA = [];
            var pv = {};
            var ref = this;
            vm.events.reduce(function (std, event) {
              pv = {};
              pv["title"] = `${event.summary}`;
              pv["id"] = `${event.id}`;
              //
              pv["startDate"] = event.start.dateTime
                ? ref.dateConvetor(event.start.dateTime)
                : event.start.date;

              pv["endDate"] = event.end.dateTime
                ? ref.dateConvetor(event.end.dateTime)
                : event.end.date;

              console.log("NO");
              // return pv;
              resultA.push(pv);
              return std;
            }, {});
            console.log(JSON.stringify(resultA));
            console.log(JSON.parse(JSON.stringify(resultA)));

            this.jsonData2 = JSON.parse(JSON.stringify(resultA));
            console.log(this.jsonData2);
            this.jsonData2.push({ user_email: email });
            this.jsonDatas.push(this.jsonData2);
            console.log(this.jsonDatas);
            // this.word = [];

            // "2023-12-17T11:42:00-05:00",
            // yyyy-mm-dd HH:MM:SS
          });
      });
    },

    recommendMeetingTimes(duration) {
      const userSchedules = this.jsonData2.map((item) => {
        return {
          user: item.title,
          busyTimes: [{ start: item.startDate, end: item.endDate }],
        };
      });
      //const meetingDuration = 60;
      // Combine all busy times into a single array
      const busyTimes = userSchedules.flatMap((user) => user.busyTimes);

      const currentMonth = new Date().getMonth() + 1;
      const currentYear = new Date().getFullYear();
      const busyTimesThisMonthAndYear = busyTimes.filter((busyTime) => {
        const startDate = new Date(busyTime.start);
        return (
          startDate.getMonth() + 1 === currentMonth &&
          startDate.getFullYear() === currentYear
        );
      });
      // Sort busy times by start time
      busyTimesThisMonthAndYear.sort(
        (a, b) => new Date(a.start) - new Date(b.start)
      );

      // Find available time slots
      const availableSlots = [];
      let previousEnd = new Date();

      //   for (const busyTime of busyTimes) {
      //     const start = busyTime.start;
      //     const end = busyTime.end;
      //     if (start > previousEnd) {
      //       availableSlots.push({ start: previousEnd, end: start });
      //     }
      //     previousEnd = end;
      //   }
      for (const busyTime of busyTimesThisMonthAndYear) {
        const start = new Date(busyTime.start);
        const end = new Date(busyTime.end);

        if (start > previousEnd) {
          availableSlots.push({ start: previousEnd, end: start });
        }
        previousEnd = end;
      }
      console.log(availableSlots);

      // Find the 3 most optimized meeting times
      this.optimizedTimes = availableSlots
        .filter(
          (slot) =>
            (new Date(slot.end) - new Date(slot.start)) / 60000 >= duration
        )
        .slice(0, 3);
      console.log(this.ptimizedTimes);
      return this.optimizedTimes;
    },
    submitDuration() {
      // Pass the email address to a function
      this.recommendMeetingTimes(this.duration);
      if (this.optimizedTimes.length > 0) {
    this.showPopup = true;
  }
    },
    createEvent() {
      // const eventDateTime = this.convertTimeZone(this.eventDate, this.eventTime);

      console.log("Converting time zone...");
      const dateTime1 = this.eventDate + "T" + this.sTime + ":00";
      const dateTime2 = this.eventDate + "T" + this.eTime + ":00";
      console.log(dateTime1);
      console.log(dateTime2);

    //   console.log(this.jsonData2)
    //   console.log(this.jsonData2.user_email)

      const event = {
        summary: this.eventTitle,
        start: {
          dateTime: dateTime1,
          timeZone: "America/New_York",
        },
        end: {
          dateTime: dateTime2,
          timeZone: "America/New_York",
        },
        location: this.eventLocation,
        attendees: [
        {email: this.email},
  ],
      };
      this.insertEvent(event);
      this.getEvents();
      console.log(event);
    },

    insertEvent(event) {
      var vm = this;
      vm.api.client.load("calendar", "v3", () => {
        vm.api.client.calendar.events
          .insert({
            calendarId: "primary",
            resource: event
          })
          .then((response) => {
            console.log(response);
          });
      });
    },
  },
};
</script>

<style scoped>
#scheduling {
  display: grid;
  grid-template-columns: 1fr 2fr; /* Two columns with equal width */
  gap: 20px; /* Adjust the gap as needed */
}

.left-side {
  padding: auto;
}

.header {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  justify-content: flex-end;
  margin-bottom: 1rem; /* Adjust the margin as needed */
  height: 30px;
}

button {
  background-color: #2d8cff !important;
  margin-left: 10px; /* Adjust the margin between buttons */
}
.right-side {
  padding: 20px; /* Adjust the padding as needed */
  text-align: left;
}

.form-group {
  margin-bottom: 15px;
  margin-right: 30px; /* Add spacing between each form group */
}

.form-group label {
  margin-bottom: 5px; /* Add spacing between label and input */
  display: block;
}

.form-group input {
  width: 100%; /* Make the input boxes take the full width of the container */
  box-sizing: border-box; /* Include padding and border in the width */
  margin-bottom: 10px; /* Add spacing at the bottom of each input */
}

/* 添加浮窗样式 */
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

/* 关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}

/* 标题样式 */
.popup h2 {
  margin-bottom: 10px;
}

/* 列表样式 */
.popup ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.popup li {
  margin-bottom: 5px;
}


.sc {
  background: white;

  /* Add any additional styling for your scheduling component */
}
</style> 


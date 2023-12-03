<template>
    <div id="scheduling">
      <h1>Google Calendar Integration</h1>
      <button @click="handleAuthClick">Authorize</button>
      <button @click="handleSignOutClick">Sign Out</button>

      <div>
    <input type="email" v-model="email" placeholder="Enter your email address" />
    <button @click="submitEmail">Submit</button>
  </div>
  <div>
    <input type="number" v-model="duration" placeholder="Enter your Time Duration" />
    <button @click="submitDuration">Submit</button>

    <div>
    <ul>
      <li v-for="item in optimizedTimes" :key="item.start">{{ item.start }} - {{ item.end }}</li>
    </ul>
  </div>

  <div>
    <h3>Create Google Calendar Event</h3>
    <form @submit.prevent="createEvent">
      <label for="eventTitle">Event Title:</label>
      <input type="text" id="eventTitle" v-model="eventTitle" required>
      <br>
      <label for="eventDate">Event Date:</label>
      <input type="date" id="eventDate" v-model="eventDate" required>
      <br>
      <label for="sTime">Start Time:</label>
      <input type="time" id="sTime" v-model="sTime" required>
      <br>
      <label for="eTime">End Time:</label>
      <input type="time" id="eTime" v-model="eTime" required>
      <br>
      <label for="eventLocation">Event Location (Zoom URL):</label>
      <input type="text" id="eventLocation" v-model="eventLocation" required>
      <br>
      <button type="submit">Create Event</button>
    </form>
  </div>

    
  </div>



    <calendar :authorized="authorized" :events="events" :jsonData1="jsonData1" :jsonDatas="jsonDatas"/> 
    </div>


    

    
  </template>
  
  <script src="https://apis.google.com/js/platform.js"></script>
  <script>

 

    // import {useAuthStore} from "@/stores/AuthStore"
    // const AuthStore = useAuthStore();

    import calendar from "../../components/calendar.vue";
    



    const CLIENT_ID = '737463276639-2uvkfra1rt9185d369u2ct0ilk76hegq.apps.googleusercontent.com'
    const API_KEY = 'AIzaSyB3Yrl7uPAOoCxZ3m3K4mQmcBncSi1AJ9c'
    const DISCOVERY_DOCS = 'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
    const SCOPES = 'https://www.googleapis.com/auth/calendar'


    export default {

        name: "scheduling",

        components: {
            calendar
        },
                
        data () {
            return {
                authorized: false,
                items: undefined,
                events: [],
                jsonData1:[],
                jsonData2:[],
                jsonDatas:[],
                optimizedTimes:[],
                eventTitle: '',
                eventDate: '',
                sTime:'',
                eTime: '',
                eventLocation: ''

                
            };
        }, 
        created() {
            
            console.log(this.$store);
            this.api = gapi;
            this.handleClientLoad();
        },
        methods: {
            convertDateTime(dateTime) {
            const date = new Date(dateTime);
            const formattedDateTime = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
            return formattedDateTime;
            },

            handleClientLoad() {
                this.api.load('client:auth2', this.initClient);
            },
            initClient() {
                let vm = this;
                vm.api.client.init({
                    apiKey: API_KEY,
                    clientId: CLIENT_ID,
                    discoveryDocs: DISCOVERY_DOCS,
                    scope: SCOPES,
                    cookie_policy: 'single_host_origin',
                    plugin_name: 'login'
                }).then(_ => {
                    vm.api.auth2.getAuthInstance().isSignedIn.listen(vm.authorized);
                });
            },
            handleAuthClick(event) {
                Promise.resolve(this.api.auth2.getAuthInstance().signIn())
                    .then(_ => {
                        this.authorized = true;
                        console.log("User logged in")
                     


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
                Promise.resolve(this.api.auth2.getAuthInstance().signOut())
                    .then(_ => {
                        this.authorized = false;
                        console.log('User signed out.');
                    });
            },
            // "2023-12-17T11:42:00-05:00", 
            // yyyy-mm-dd HH:MM:SS
            dateConvetor(s){

                
                const inputString = s.toString()
                console.log(inputString);


                const date = new Date(inputString);
                const easternTime = new Date(date.toLocaleString("en-US", { timeZone: "America/New_York" }));

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
                vm.api.client.load('calendar', 'v3', () => {
                    vm.api.client.calendar.events.list({
                    'calendarId': 'primary',
                    //'timeMin': (new Date()).toISOString(),
                    'showDeleted': false,
                    'singleEvents': true,
                    'maxResults': 10000000,
                    'orderBy': 'startTime',
                }).then(response => {
                    vm.events = response.result.items;

                    if (!vm.events || vm.events.length == 0) {
                        console.log("no events")
                        return;
                    }
                    // Flatten to string to display
                    const output = vm.events.reduce(
                        (str, event) => `${str}${event.summary} (${event.start.dateTime || event.start.date})\n`,
                        'Events:\n');
                    console.log(output)
                    var resultA = [];
                    var pv = {};
                    var ref=this;
                    vm.events.reduce(function(std, event) {
                        pv = {};
                        pv["title"]=`${event.summary}`
                        pv["id"]=`${event.id}`
                        // 
                        pv["startDate"] = event.start.dateTime ? ref.dateConvetor(event.start.dateTime) : event.start.date;
                      
                        pv["endDate"] = event.end.dateTime ? ref.dateConvetor(event.end.dateTime) : event.end.date;

                        console.log("NO")
                        // return pv;
                        resultA.push(pv);
                        return std;
                    }, {});
                    console.log(JSON.stringify(resultA))
                    console.log(JSON.parse(JSON.stringify(resultA)))
                    this.jsonData1 = JSON.parse(JSON.stringify(resultA))
                    console.log(this.jsonData1)
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
        vm.api.client.load('calendar', 'v3', () => {
            vm.api.client.calendar.events.list({
            'calendarId': email,
            //'timeMin': (new Date()).toISOString(),
            'showDeleted': false,
            'singleEvents': true,
            'maxResults': 10000000,
            'orderBy': 'startTime',
        }).then(response => {
            vm.events = response.result.items;

            if (!vm.events || vm.events.length == 0) {
                console.log("no events")
                return;
            }
            // Flatten to string to display
            const output = vm.events.reduce(
                (str, event) => `${str}${event.summary} (${event.start.dateTime || event.start.date})\n`,
                'Events:\n');
            console.log(output)
            var resultA = [];
            var pv = {};
            var ref=this;
            vm.events.reduce(function(std, event) {
                pv = {};
                pv["title"]=`${event.summary}`
                pv["id"]=`${event.id}`
                // 
                pv["startDate"] = event.start.dateTime ? ref.dateConvetor(event.start.dateTime) : event.start.date;
                
                pv["endDate"] = event.end.dateTime ? ref.dateConvetor(event.end.dateTime) : event.end.date;

                console.log("NO")
                // return pv;
                resultA.push(pv);
                return std;
            }, {});
            console.log(JSON.stringify(resultA))
            console.log(JSON.parse(JSON.stringify(resultA)))
            
            this.jsonData2 = JSON.parse(JSON.stringify(resultA))
            console.log(this.jsonData2)
            this.jsonData2.push({ user_email: email});
            this.jsonDatas.push(this.jsonData2);
            console.log(this.jsonDatas)
            // this.word = [];

            
            // "2023-12-17T11:42:00-05:00", 
            // yyyy-mm-dd HH:MM:SS
        });
        });
    },
   
    recommendMeetingTimes(duration) {
        const userSchedules = this.jsonData1.map(item => {
        return {
            user: item.title,
            busyTimes: [
            { start: item.startDate, end: item.endDate }
    ]
  };
})
   //const meetingDuration = 60;
  // Combine all busy times into a single array
  const busyTimes = userSchedules.flatMap(user => user.busyTimes);
  
 
  // Sort busy times by start time
  busyTimes.sort((a, b) => new Date(a.start) - new Date(b.start));
  
 
  // Find available time slots
  const availableSlots = [];
  let previousEnd = '12:00am';
 
  for (const busyTime of busyTimes) {
	const start = busyTime.start;
	const end = busyTime.end;
	if (start > previousEnd) {availableSlots.push({ start: previousEnd, end: start });
	}
	previousEnd = end;
  }
  console.log(availableSlots);
 
  // Find the 3 most optimized meeting times
  this.optimizedTimes = availableSlots
  .filter(slot => ((new Date(slot.end) - new Date(slot.start)) / 60000 >= duration))
  .slice(0, 3);
  console.log(optimizedTimes);
  return optimizedTimes;
  
},
submitDuration() {
      // Pass the email address to a function
      this.recommendMeetingTimes(this.duration);


      

    },
createEvent() {
    // const eventDateTime = this.convertTimeZone(this.eventDate, this.eventTime);
   
    console.log("Converting time zone...");
        const dateTime1 = this.eventDate + 'T' + this.sTime+":00";
        const dateTime2 = this.eventDate + 'T' + this.eTime+":00";
        console.log(dateTime1);
        console.log(dateTime2);

    const event = {
    summary: this.eventTitle,
    start: {
        dateTime: dateTime1,
        "timeZone": "America/New_York",
    },
    end: {
        dateTime: dateTime2,
        "timeZone": "America/New_York",
    },
    location: this.eventLocation,
    };
    this.insertEvent(event);
    console.log(event);
},

insertEvent(event) {
    var vm = this;
        vm.api.client.load('calendar', 'v3', () => {
            vm.api.client.calendar.events.insert({
                'calendarId': 'primary',
                'resource': event
        }).then(response => {
            console.log(response) 
});
                });

}
}

 
        
            
        
    };
</script>

<style scoped>
    .scheduling {
        background: white;
    }

</style> 


<template>
    <div id="scheduling">
      <h1>Google Calendar Integration</h1>
      <button @click="handleAuthClick">Authorize</button>
      <button @click="handleSignOutClick">Sign Out</button>
      <button @click="getEvents">Get Events</button>

    </div>
  </template>
  
  <script src="https://apis.google.com/js/platform.js"></script>
  <script>

    const CLIENT_ID = '737463276639-2uvkfra1rt9185d369u2ct0ilk76hegq.apps.googleusercontent.com'
    const API_KEY = 'AIzaSyB3Yrl7uPAOoCxZ3m3K4mQmcBncSi1AJ9c'
    const DISCOVERY_DOCS = 'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
    const SCOPES = 'https://www.googleapis.com/auth/calendar'


    export default {
        data () {
            return {
                authorized: false,
                items: undefined
            };
        }, 
        created() {
            this.api = gapi;
            this.handleClientLoad();
        },
        methods: {
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
                    });
            },
            handleSignOutClick(event) {
                Promise.resolve(this.api.auth2.getAuthInstance().signOut())
                    .then(_ => {
                        this.authorized = false;
                        console.log('User signed out.');
                    });
            },
            getEvents() {
                let vm = this;
                vm.api.client.load('calendar', 'v3', () => {
                    vm.api.client.calendar.events.list({
                    'calendarId': 'primary',
                    'timeMin': (new Date()).toISOString(),
                    'showDeleted': false,
                    'singleEvents': true,
                    'maxResults': 10,
                    'orderBy': 'startTime',
                }).then(response => {

                    const events = response.result.items;
                    if (!events || events.length == 0) {
                        console.log("no events")
                        return;
                    }
                    // Flatten to string to display
                    const output = events.reduce(
                        (str, event) => `${str}${event.summary} (${event.start.dateTime || event.start.date})\n`,
                        'Events:\n');
                    console.log(output)
                });
                });
            }
            
        }
    };
</script>

<style scoped>


/* .scheduling {
   background: white;
 } */

</style> 

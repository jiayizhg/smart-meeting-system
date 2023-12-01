<template>
  <main>
    <button @click="getSignature">Join Meeting</button>
  </main>
</template>

<script>
import axios from "axios";
import { ZoomMtg } from '@zoomus/websdk';

export default {
  name: 'HelloWorld',
  created () {
    ZoomMtg.setZoomJSLib('https://source.zoom.us/2.16.0/lib', '/av');
    ZoomMtg.preLoadWasm();
    ZoomMtg.prepareWebSDK();
    // loads language files, also passes any error messages to the ui
    ZoomMtg.i18n.load('en-US');
    ZoomMtg.i18n.reload('en-US');
  },
  mounted() {
    ZoomMtg.inMeetingServiceListener("onUserJoin", (data) => {
      console.log("inMeetingServiceListener onUserJoin", data);
    });
  },
  data () {
    return {
      authEndpoint: "http://localhost:4000",
      sdkKey: "u8To97SrT22clDxYXkHd0w",
      meetingNumber: "85169167502",
      passWord: "G6enE7",
      role: 0,
      userName: "Owen",
      userEmail: "owen@gmail.com",
      registrantToken: '',
      zakToken: '',
      leaveUrl: "http://localhost:8080"
    }
  },
  methods: {
    getSignature() {
      axios.post(this.authEndpoint, {
        meetingNumber: this.meetingNumber,
        role: this.role
      })
      .then(res => {
        console.log(res.data.signature);
        this.startMeeting(res.data.signature);
      })
      .catch(error => {
        console.log(error);
      });
    },
    startMeeting(signature) {
      document.getElementById("zmmtg-root").style.display = "block";

      ZoomMtg.init({
        leaveUrl: this.leaveUrl,
        success: (success) => {
          console.log(success);
          ZoomMtg.join({
            signature: signature,
            sdkKey: this.sdkKey,
            meetingNumber: this.meetingNumber,
            passWord: this.passWord,
            userName: this.userName,
            userEmail: this.userEmail,
            tk: this.registrantToken,
            zak: this.zakToken,
            success: (success) => {
              console.log(success);
            },
            error: (error) => {
              console.log(error);
            }
          });
        },
        error: (error) => {
          console.log(error);
        }
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only
<style scoped>

</style> -->

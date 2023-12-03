<template>
    <div class="calendar">
      <div class="button-container">
        <button>Day View</button>
        <button>Week View</button>
        <button>Month View</button>
      </div>
      <vue-calendar
        :show-limit="3"
        @show-all="showAll"
        @event-clicked="eventClicked"
        @month-changed="monthChanged"
        :Show-times=true
        :highlight="highlight"
        :events="events"
      ></vue-calendar>
      <p>{{authorized}}</p>
      <p>{{events}}</p>
    </div>
  </template>
  
  <script>
  import Vue from 'vue/dist/vue.js'
  import vueCalendar from "vue2-simple-calendar";


    Vue.use(vueCalendar, {
        firstDay: 0
    });

    export default {
        name: "calendar",
        // data(){
        //   return{
        //     events: [ {
        //       // id':"11",
        //       start:"11-17-2023",
        //       dateStart:"10,30,00,00",
        //       // showTimes:"15:00:00",
        //       title:"666",
        //       end:"11-17-2023",
        //       datEend:"11,30,00,00",
        //     }]
        //   }
        // },

        props:{authorized:Boolean,
          events:Object

        
        } 
        // props: ['events'],
        // data() {
        //     return {
        //         data: [],
        //         highlight: {
        //         dates: [
        //             // Highlight an array of dates
        //             new Date(2021, 6, 23),
        //             new Date(2021, 6, 24),
        //     ],
        //     },
        //     disabled: {
        //     // to: new Date(2021, 4, 23), // Disable all dates up to specific date
        //     },
        //     // events: [
        //     //   {
        //     //     start: "2021-4-27",
        //     //     end: "2021-4-22",
        //     //     title: "FooEvent",
        //     //     classes: [""],
        //     //   },
        //     // ],
        // };
        // },
    // methods: {
    //     printevent() {
    //         let vm = this;
    //         console.log("in calendar.vue")
    //         console.log(events)
        // }
    //   showAll(events) {
    //     // Do something...
    //   },
    //   dayClicked(day) {
    //     console.log(day);
    //     // Do something...
    //   },
    //   eventClicked(event) {
    //     // Do something...
    //   },
    //   monthChanged(start, end) {
    //     // Do something...
    //   },
    // },
  //   mounted() {
  //       this.printevent();
     
  // } 
  ,
    created() {
      this.$calendar.eventBus.$on("show-all", (events) => this.showAll(events));
  //     this.$calendar.eventBus.$on("day-clicked", (day) => this.dayClicked(day));
    },
  };
  </script>

  <style scoped>
    h1,
    h2 {
        font-weight: normal;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li {
        display: inline-block;
        margin: 0 10px;
    }
    a {
        color: #42b983;
    }
    .button-container {
      display: flex;
    }
  </style>
  
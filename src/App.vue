
<template>
  <div id="app">
      <!-- route outlet -->
      <!-- component matched by the route will render here -->


  
      <!-- <div class="home-left">
          <Sidebar />
      </div>
        
      <div class="home-right">


          <Home />

      </div>
       -->

       <div class="home-left">
          <Sidebar />
      </div>
      <div class="home-right">
        <router-view></router-view>
      </div>
  </div>
</template>

<script>
 

  import Sidebar from './components/sidebar.vue'
  // import Home from './components/home.vue'

  export default {
    components: {Sidebar}
  }



</script>

<style>

</style>


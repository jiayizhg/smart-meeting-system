<template>
  <div class="sidenav">
    
    <router-link to="/"><font-awesome-icon :icon="['fas', 'house']" /></router-link>
  
    <router-link to="/scheduling"><font-awesome-icon :icon="['fas', 'circle-user']"  class="user"/></router-link>
  
  </div>
</template>

<script>
export default {};
</script>

<style scoped>

.sidenav {
  height: 100%;
  background-color: #f0f0f0;

}


.sidenav a {
  padding: 6px 8px 6px 16px;
  text-decoration: none;
  font-size: 25px;
  color: black;
  display: block;
}

@media screen and (max-height: 450px) {
  .sidenav {
    padding-top: 15px;
  }
  .sidenav a {
    font-size: 18px;
  }
}
</style>
<template>
  <div id="app">
    <HelloWorld />
    <scheduling />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue';
import scheduling from './views/calendar/scheduling.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
    scheduling
  }
}

// export default {
//   name: 'App',
//   components: {
//     scheduling
//   }
// }
</script>

<style>
#app {
  width: 70%;
  margin: auto;
  text-align: center;
}
#zmmtg-root {
  display: none;
}
</style>

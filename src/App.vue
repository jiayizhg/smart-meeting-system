<template>
  <div id="app">
    <p>
        <!-- use router-link component for navigation. -->
        <!-- specify the link by passing the `to` prop. -->
        <!-- `<router-link>` will be rendered as an `<a>` tag by default -->
      <router-link to="/scheduling">scheduling</router-link>
    </p>
      <!-- route outlet -->
      <!-- component matched by the route will render here -->
    <router-view></router-view>
  </div>
</template>

<script>

</script>

<style>

</style>

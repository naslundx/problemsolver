<template>
    <!-- <p>navbar</p> -->
    <header>
    <div>
      <nav>
        <RouterLink to="/">Spela</RouterLink>
        <RouterLink to="/about">Om mig</RouterLink>
      </nav>
    </div>
  </header>
  </template>
  
  <script>

  export default {
    components: {
    },
  };
  </script>
  
  <style scoped>
  header {
    width: 100%;
    padding: 10px;
    max-height: 100vh;
    background-color: white;
  }
  
  nav {
    font-size: 12px;
    text-align: center;
  }
  
  nav a.router-link-exact-active {
    color: var(--color-text);
  }
  
  nav a.router-link-exact-active:hover {
    background-color: transparent;
  }
  
  nav a {
    display: inline-block;
    padding: 0 1rem;
    border-left: 1px solid var(--color-border);
  }
  
  nav a:first-of-type {
    border: 0;
  }
  
  </style>
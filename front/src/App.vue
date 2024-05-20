<template>
  <div id="app">
    <header>
      <Image src="../static/crazy-chef.png" alt="crazyman" width="70px" />
      <h1>Purple Dragon</h1>
      <div v-if="userEmail" class="dashboard-button-container">
        <p>{{ userEmail }}</p>
        <Button id="dashboard-button" label="Dashboard" @click="goToDashboard" />
      </div>
    </header>
    <router-view></router-view>
  </div>
</template>

<script>
import Image from 'primevue/image';
import Button from 'primevue/button';
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'App',
  components: {
    Image,
    Button
  },
  computed: {
    ...mapGetters(['userEmail', 'userHashedPassword'])
  },
  created() {
    const authHeaders = JSON.parse(localStorage.getItem('authHeaders'));
    if (authHeaders) {
      this.setUser({
        email: authHeaders.username,
        hashedPassword: authHeaders.hashedPassword
      });
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    ...mapActions(['setUser']),
    goToDashboard() {
      this.$router.push('/dashboard');
    }
  }
}
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
}

header {
  display: flex;
  background-color: var(--primary-color);
  padding: 1rem;
  color: var(--text-color);
  text-align: center;
}

.p-button {
  background-color: var(--primary-color);
  color: var(--text-color);
  border: none;
}

.dashboard-button-container {
  margin-left: auto;
}

#dashboard-button {
  background-color: var(--accent-color);
}
</style>

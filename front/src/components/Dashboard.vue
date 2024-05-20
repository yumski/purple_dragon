<template>
  <div id="dashboard">
    <main>
      <h1>Dashboard</h1>
      <p>{{ userEmail }}</p>
      <div id="buttons">
        <Button label="Back to Home" @click="goHome" />
        <Button id="logout" label="Logout" @click="logout" />
      </div>

    </main>
  </div>
</template>

<script>
import Button from 'primevue/button';

export default {
  name: 'Dashboard',
  components: {
    Button
  },
  data() {
    return {
      userEmail: ''
    };
  },
  async created() {
    try {
      const response = await fetch('http://localhost:5000/api/user/dashboard', {
        method: 'GET',
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        this.userEmail = data.message;
      } else {
        this.$router.push('/login');
      }
    } catch (error) {
      this.$router.push('/login');
    }
  },
  methods: {
    async logout() {
      try {
        const response = await fetch('http://localhost:5000/api/user/logout', {
          method: 'POST',
          credentials: 'include'
        });

        if (response.ok) {
          this.$router.push('/login');
        } else {
          alert('Failed to logout');
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    },
    goHome() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
#dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  align-items: center;
  justify-content: center;
}

header {
  background-color: var(--primary-color);
  padding: 1rem;
  color: var(--text-color);
  text-align: center;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
}

p {
  margin-bottom: 1rem;
}

#buttons {
  display: flex;
  flex-direction: row;
  gap: 3rem;
}

#logout {
  background-color: var(--accent-color);
}
</style>

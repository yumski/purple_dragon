<template>
  <div id="login">
    <main>
      <h1>Login</h1>
      <form @submit.prevent="submitForm">
        <FloatLabel>
          <label for="user_email">Email</label>
          <InputText style="width: 100%" v-model="email" />
        </FloatLabel>
        <FloatLabel>
          <label for="password">Password</label>
          <Password inputStyle="width: 100%" style="width: 100%" v-model="password" :feedback="false" />
        </FloatLabel>
        <Button label="Submit" type="submit" />
      </form>
    </main>
  </div>
</template>

<script>
import Button from 'primevue/button';
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';

import { mapActions } from 'vuex';


export default {
  name: 'Login',
  components: {
    Button,
    FloatLabel,
    InputText,
    Password
  },
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    ...mapActions(['loginUser']),
    async submitForm() {
      try {
        const response = await fetch('http://localhost:5000/api/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ user_email: this.email, user_password: this.password }),
          credentials: 'include'
        });

        if (response.ok) {
          const data = await response.json();
          this.loginUser({
            email: this.email,
            hashedPassword: data.hashed_password
          });
          localStorage.setItem('authHeaders', JSON.stringify({
            username: this.email,
            hashedPassword: data.hashed_password
          }));
          this.$router.push('/');
        }
        else {
          const data = await response.json();
          alert(data.error || 'Invalid credentials');
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    }
  }
}
</script>

<style scoped>
#login {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  align-items: center;
  justify-content: center;
}

form {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>

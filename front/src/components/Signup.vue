<template>
    <div id="signup">
      <header>
        <h1>User Signup</h1>
      </header>
      <main>
        <form @submit.prevent="submitForm">
          <p>
            <label for="user_email">Email</label>
            <input type="email" v-model="email" id="user_email" placeholder="enter email" required>
          </p>
          <p>
            <label for="user_password">Password</label>
            <input type="password" v-model="password" id="user_password" placeholder="enter password" required>
          </p>
          <p>
            <label for="confirm_password">Confirm Password</label>
            <input type="password" v-model="confirmPassword" id="confirm_password" placeholder="confirm password" required>
          </p>
          <Button label="Submit" type="submit" />
        </form>
      </main>
    </div>
  </template>
  
  <script>
  import Button from 'primevue/button';
  
  export default {
    name: 'Signup',
    components: {
      Button
    },
    data() {
      return {
        email: '',
        password: '',
        confirmPassword: ''
      }
    },
    methods: {
      async submitForm() {
        if (this.password !== this.confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
        try {
          const response = await fetch('http://localhost:5000/api/user/signup', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_email: this.email, user_password: this.password }),
            credentials: 'include'
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert('Signup successful!');
            this.$router.push('/login');
          } else {
            alert(data.error || 'Signup failed');
          }
        } catch (error) {
          alert('An error occurred: ' + error.message);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  #signup {
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
  
  form {
    width: 300px;
    display: flex;
    flex-direction: column;
  }
  
  p {
    margin-bottom: 1rem;
  }
  
  label {
    margin-bottom: 0.5rem;
  }
  
  input {
    padding: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  button {
    padding: 0.5rem;
    background-color: var(--primary-color);
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: var(--primary-color-dark);
  }
  </style>
  
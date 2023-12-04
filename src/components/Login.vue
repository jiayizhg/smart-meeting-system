<template>
  <div class="auth-container">
    <h2 v-if="isLoginMode">Login</h2>
    <h2 v-else>Register</h2>

    <form @submit.prevent="isLoginMode ? loginUser() : registerUser()">
      <div class="form-group" v-if="isLoginMode">
        <label for="name">ID</label>
        <input type="text" v-model="user.id" required>
      </div>
      <div class="form-group" v-if="!isLoginMode">
        <label for="name">Name</label>
        <input type="text" v-model="user.name" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" v-model="user.password" required>
      </div>
      <button type="submit">{{ isLoginMode ? 'Login' : 'Register' }}</button>
    </form>

    <button @click="toggleMode">
      {{ isLoginMode ? 'Switch to Register' : 'Switch to Login' }}
    </button>

    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>
  
  <script>
import axios from 'axios';

  export default {
    data() {
      return {
        user: {
          id: '',
          name: '',
          role: '',
          is_temporary: false,
          password: ''
        },
        isLoginMode: true,
        message: ''
        };
    },
    methods: {
      async registerUser() {
        const ref =this;
        axios({
          method: 'post',
          url: 'http://localhost:8000/add_user', 
          data: {
            name: this.user.name,
            password: this.user.password,
          },
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(function (response) {
            console.log(response.data);
            ref.message = `Registration successful! Your ID is: ${response.data.id}`;
            ref.isLoginMode = true;
        })
        .catch(function (error) {
            console.log(error); 
            ref.message = 'Registration failed. Please try again.';
        });

      },
      async loginUser() {
        try {
          await axios.post('http://localhost:8000/user_login', {
            id: this.user.id,
            password: this.user.password
          });
          this.message = 'Login successful!';
        } catch (error) {
          console.error(error);
          this.message = 'Login failed. Wrong ID or Password.';
        }
      },
      toggleMode() {
        this.isLoginMode = !this.isLoginMode;
      }
    }
  }
  </script>


<style>
  .auth-container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
  }

  .form-group {
    margin-bottom: 10px;
  }

  .form-group label {
    display: block;
  }

  .form-group input[type="text"],
  .form-group input[type="password"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }

  .message {
    color: green;
    margin-top: 10px;
  }
</style>
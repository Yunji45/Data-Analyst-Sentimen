<template>
    <div class="sign-in-layout">
        <!-- Left side: Image -->
        <div class="sign-in-image"></div>

        <!-- Right side: Login Form -->
        <div class="sign-in-form">
            <div class="sign-in-container bg-white shadow border-0 rounded p-4 p-lg-5">
                <div class="text-center mb-4">
                    <!-- Ganti dengan logo -->
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Logo_PLN.svg/2560px-Logo_PLN.svg.png" alt="Sign In Logo" style="max-width: 150px" />
                    <p class="lead text-muted" style="font-size: 12px">
                        <span v-if="errorMessage" class="text-danger">{{ errorMessage }}</span>
                        <span v-else>Please enter your credentials to sign in.</span>
                    </p>
                </div>
                <form @submit.prevent="handleLogin" class="mt-4">
                    <div class="form-group mb-4">
                        <label for="username">Username</label>
                        <div class="input-group">
                            <span class="input-group-text"><span class="fas fa-user-circle"></span></span>
                            <input v-model="username" type="text" id="username" placeholder="Username" class="form-control" required />
                        </div>
                    </div>
                    <div class="form-group mb-4">
                        <label for="password">Your Password</label>
                        <div class="input-group">
                            <span class="input-group-text"><span class="fas fa-unlock-alt"></span></span>
                            <input v-model="password" type="password" id="password" placeholder="Password" class="form-control" required />
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-top mb-4">
                        <div class="form-check">
                            <input v-model="rememberMe" class="form-check-input" type="checkbox" id="remember" />
                            <label class="form-check-label" for="remember">Remember me</label>
                        </div>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-signin">Sign In</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const errorMessage = ref('');
const enableSocialAuth = true;

// Fungsi untuk menangani login
const handleLogin = async () => {
    errorMessage.value = '';

    try {
        const response = await axios.post(`${import.meta.env.VITE_BASE_URL}api/login`, {
            username: username.value,
            password: password.value,
            remember: rememberMe.value
        });

        if (response.data.status === 'success') {
            // Redirect ke dashboard atau halaman lain setelah login berhasil
            window.location.href = '/dashboard';
        } else {
            errorMessage.value = response.data.message || 'Login failed. Please try again.';
        }
    } catch (error) {
        errorMessage.value = 'An error occurred during login. Please try again.';
    }
};

// Fungsi untuk login dengan GitHub
const loginWithGithub = () => {
    window.location.href = `${import.meta.env.VITE_BASE_URL}api/login/github`;
};
</script>

<style scoped>
.sign-in-container {
    min-width: 450px;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.sign-in-header h1 {
    font-weight: 700;
    font-size: 2.5rem;
    color: #333;
}
.form-group label {
    font-weight: 600;
    color: #555;
}
.form-control {
    border-radius: 5px;
    font-size: 1rem;
}
.btn-signin {
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    font-size: 1.1rem;
    padding: 10px 15px;
}
.btn-signin:hover {
    background-color: #0056b3;
}
.social-login-btn {
    border-radius: 5px;
    border: 1px solid #ddd;
    padding: 10px 20px;
    font-weight: 600;
}
.social-login-btn:hover {
    background-color: #f1f1f1;
}
.sign-in-layout {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
.sign-in-image {
    flex: 1;
    background: url('https://plus.unsplash.com/premium_photo-1676657954811-9409c4830467?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D') no-repeat center center;
    background-size: cover;
    height: 100vh;
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}
.sign-in-form {
    flex: 1;
    padding: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>

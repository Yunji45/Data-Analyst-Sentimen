<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Checkbox from 'primevue/checkbox';

const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const errorMessage = ref('');
const value2 = ref(null);
const value = ref(null);
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

<template>
    <div class="flex justify-center items-center min-h-screen">
        <!-- Left side: Image -->
        <div class="flex-1 bg-cover bg-center" style="">
            <img src="https://plus.unsplash.com/premium_photo-1676657954811-9409c4830467?q=80&w=2787&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" class="w-full h-screen" alt="" />
        </div>

        <!-- Right side: Login Form -->
        <div class="flex-1 p-10 flex justify-center items-center">
            <div class="bg-white shadow border-0 rounded p-4 p-lg-5 min-w-[450px]">
                <div class="text-center mb-4">
                    <!-- Ganti dengan logo -->
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Logo_PLN.svg/2560px-Logo_PLN.svg.png" alt="Sign In Logo" class="max-w-[150px]" />
                    <p class="lead text-muted text-sm">
                        <span v-if="errorMessage" class="text-danger">{{ errorMessage }}</span>
                        <span v-else>Please enter your credentials to sign in.</span>
                    </p>
                </div>
                <form @submit.prevent="handleLogin" class="mt-4 px-5">
                    <div class="mb-4 px-10">
                        <FloatLabel variant="on">
                            <InputText id="Username" v-model="value2" autocomplete="off" class="w-full" />
                            <label for="Username">Username</label>
                        </FloatLabel>
                    </div>
                    <div class="mb-4 px-10">
                        <FloatLabel variant="on">
                            <InputText id="Username" v-model="value2" autocomplete="off" class="w-full" />
                            <label for="Username">Username</label>
                        </FloatLabel>
                    </div>

                    <div class="mb-4 px-10">
                        <Password v-model="value" class="w-full">
                            <template #header>
                                <div class="font-semibold mb-4">Pick a password</div>
                            </template>
                            <template #footer>
                                <Divider />
                                <ul class="pl-2 ml-2 my-0 leading-normal">
                                    <li>At least one lowercase</li>
                                    <li>At least one uppercase</li>
                                    <li>At least one numeric</li>
                                    <li>Minimum 8 characters</li>
                                </ul>
                            </template>
                        </Password>
                    </div>

                    <div class="mb-4">
                        <div class="form-check">
                            <Checkbox v-model="rememberMe" binary class="custom-checkbox" />
                            <label class="form-check-label" for="remember">Remember me</label>
                        </div>
                    </div>

                    <div>
                        <button type="submit" class="bg-blue-500 text-white rounded py-2 px-4 text-lg hover:bg-blue-600">Sign In</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const value = ref(null);
</script>

<template>
    <div class="card flex justify-center">
        <Password v-model="value">
            <template #header>
                <div class="font-semibold text-xm mb-4">Pick a password</div>
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
</template>

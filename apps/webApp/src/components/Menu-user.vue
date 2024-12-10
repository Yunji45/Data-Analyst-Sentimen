<script setup>
import { ref } from 'vue';

const cardMenu = ref([
    { label: 'Save', icon: 'pi pi-fw pi-check' },
    { label: 'Update', icon: 'pi pi-fw pi-refresh' },
    { label: 'Delete', icon: 'pi pi-fw pi-trash' }
]);
const menuRef = ref(null);

function toggle(event) {
    menuRef.value.toggle(event);
}
</script>

<template>
    <Card>
        <template v-slot:title>
            <div class="flex items-center justify-between mb-0">
                <div class="font-semibold text-xl mb-4">Card</div>
                <Button icon="pi pi-plus" class="p-button-text" @click="toggle" />
            </div>
            <Menu id="config_menu" ref="menuRef" :model="cardMenu" :popup="true" />
        </template>

        <template v-slot:content>
            <p class="leading-normal m-0">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
        </template>
    </Card>
</template>

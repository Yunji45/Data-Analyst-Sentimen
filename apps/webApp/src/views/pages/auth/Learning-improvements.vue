<template>
    <div className="card">
        <div class="font-semibold text-xl mb-4">Learnings-improvements Page</div>
        <p>Use this page to start from scratch and place your custom content.</p>
        <button class="flex items-center px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2">
            <slot name="icon">
                <!-- Default Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M5.121 17.804A12.045 12.045 0 003 12C3 6.477 7.477 2 12 2s9 4.477 9 10c0 1.654-.423 3.216-1.121 4.596m-6.134-2.337A4.978 4.978 0 0012 14.5c-1.198 0-2.29.416-3.144 1.12m6.144 2.38C13.708 19.243 12.907 20 12 20c-1.198 0-2.29-.416-3.144-1.12"
                    />
                </svg>
            </slot>
            <slot>Button</slot>
        </button>
    </div>
</template>

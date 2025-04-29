<template>
    <div class="tasks-page">
        <h1>Your Tasks</h1>
        <div v-if="tasks.length === 0">
            <p>No tasks found.</p>

        </div>

        <ul v-else>
            <li v-for="task in tasks" :key="task.id">
                <strong>
                    {{ task.title }}: {{ task.description }}
                </strong>
            </li>
        </ul>
    </div>
</template>

<script>
import api from '@/api/api';

export default {
    name: 'TasksPage',
    data() {
        return {
            tasks: [],
        };
    },
    async mounted() {
        try {
            const response = await api.get('/tasks');
            this.tasks = response.data;
            console.log('Tasks:', this.tasks);
        } catch (error) {
            console.error('Failed fetching tasks:', error)
        }
    },
};
</script>

<style scoped>
.tasks-page {
    max-width: 600px;
    margin: 50px auto;
    text-align: left;
}
</style>
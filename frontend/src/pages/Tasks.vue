<template>
    <div class="tasks-page">
        <div class="header">
            <h1>Your Tasks</h1>
            <button @click="logout">Logout</button>
            <button @click="showForm = ! showForm">+ Create Task</button>
        </div>

        <form v-if="showForm" @submit.prevent="createTask" class="task-form transition-all duration-300">
            <input v-model="newTask.title" placeholder="Title" required />
            <input v-model="newTask.description" placeholder="Description" required />

            <select v-model="newTask.status" required>
                <option disabled value="">Select Status</option>
                <option>To-Do</option>
                <option>In Progress</option>
                <option>Done</option>
            </select>

            <select v-model="newTask.priority" required>
                <option disabled value="">Select Priority</option>
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
            </select>

            <input v-model="newTask.due_date" type="datetime-local" />

            <select v-model="newTask.repeat">
                <option value="None">None</option>
                <option value="Daily">Daily</option>
                <option value="Weekly">Weekly</option>
                <option value="Monthly">Monthly</option>
            </select>

            <button type="submit" class="add-task-button">Add Task</button>
        </form>
        
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
            showForm: false,
            newTask: {
                title: '',
                description: '',
                status: 'To-Do',      
                priority: 'Medium',    
                due_date: null,
                repeat: 'None',
            },
        };
    },
    async mounted() {
        await this.fetchTasks();
    },

    methods: {
        async fetchTasks(){
            try {
            const response = await api.get('/tasks');
            this.tasks = response.data;
            console.log('Tasks:', this.tasks);
        } catch (error) {
            console.error('Failed fetching tasks:', error)
        }
        },

        getDefaultTask() {
            return {
                title: '',
                description: '',
                status: 'To-Do',
                priority: 'Medium',
                due_date: null,
                repeat: 'None',
            };
        },
        async createTask() {
            try {
                const response = await api.post('/tasks', this.newTask);
                // console.log('Sending new task:', this.newTask);
                // console.log('Sending task payload to backend:', JSON.stringify(this.newTask));
                console.log('Task created successfully:', response.data);
               
                this.newTask = this.getDefaultTask();
                this.showForm = false;
                await this.fetchTasks();
            } catch (error) {
                if (error.response){
                    console.error('!!!!Backend responded with:', error.response.data);
                } else {
                    console.error('!!!!Unknown error creating task:', error);
                }
            }

        },

        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
    },
};
</script>

<style scoped>
.tasks-page {
    max-width: 600px;
    margin: 50px auto;
    text-align: left;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

form {
    flex: 1;
    padding: 6px;
}

button {
    padding: 6px 12px;
    border: none;
    background-color: #ff5252;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}

.add-task-button {
    background-color: rgba(63, 105, 255, 0.44);
}


</style>
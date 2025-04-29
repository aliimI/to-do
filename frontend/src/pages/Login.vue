<template>
    <div class="login-page">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin"> <!-- @ - is shorthand for v-on means: listen on event -->
            <div>
                <label for="">Email:</label>
                <input v-model="email" type="email" required />
            </div>

            <div>
                <label for="">Password:</label>
                <input v-model="password" type="password" />
            </div>

            <button type="submit">Login</button>
        </form>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>
    </div>
</template>

<script>
import api from '@/api/api'; 

export default {
    name: 'LoginPage',
    data() {
        return {
            email: '',
            password: '',
            errorMessage: '',
        };
    },
    methods: {
        async handleLogin() {
            try {
                const formData = new URLSearchParams();
                formData.append('username', this.email);
                formData.append('password', this.password);
                //debug
                // console.log('Sending login request to:', api.defaults.baseURL);
                // console.log('Payload:', formData.toString());

                const response = await api.post('/auth/token', formData);

                const { access_token } = response.data;
                localStorage.setItem('token', access_token);
                this.$router.push('/tasks');
            } catch (error) {
                this.errorMessage = 'Incorrect username or password.';
                console.error(error);
            }
        },
    },

};
</script>


<style scoped>
.login-page {
    max-width: 400px;
    margin: 50px auto;
}

.error {
    color: red;
    margin-top: 10px;
}
</style>
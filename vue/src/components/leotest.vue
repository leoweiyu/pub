<script setup>
import { ref } from 'vue';
import axios from 'axios';

const hostname = ref('');
const namespace = ref('');
const livePodName = ref('');
const operationMode = ref('');
const response = ref(null);

const resetForm = () => {
  hostname.value = '';
  namespace.value = '';
  livePodName.value = '';
  response.value = null;
}

const submitForm = async() => {
  try {
    const { data } = await axios.post("http://127.0.0.1:5001/submit", {
      hostname: hostname.value,
      namespace: namespace.value,
      livePodName: livePodName.value,
    });
    response.value = data;
  } catch (error) {
      console.error("Error submitting from:", error);
  }
};
</script>

<template>
  <div class="container">
    <header class="header">
     <h1>Istio Troubleshoot SFC</h1>
     <p>Fill the details below to troubleshoot your Istio Configuration</p>
    </header>

    <main class="main-content">
      <div class="form-container">
        <h2>Troubleshoot Istio Form</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="hostname">Site FQDN:</label>
    	    <input 
    	      type="text" 
    	      id="hostname" 
    	      v-model="hostname" 
    	      title="Enter FQDN of the site you want to troubleshoot, for example aaa.box.asdf.anz.com"
    	      required 
    	    />
          </div>
          <div class="form-group">
            <label for="namespace">Namespace name:</label>
    	    <input
    	      type="text" 
    	      id="namespace" 
    	      v-model="namespace"
    	      title="Enter the namespace name where your gateway definition defined"
    	      required 
    	    />
          </div>
          <div class="form-group">
            <label for="livePodName">Live Pod Name:</label>
    	    <input 
    	      type="text" 
    	      id="livePodName" 
    	      v-model="livePodName" 
    	      title="To prove you really own the namespace, please provide a live pod name which currently running in your namespace"
    	      required 
    	    />
          </div>
          <button type="submit" class="submit-button">Submit</button>
	  <button type="button" class="reset-button" @click="resetForm">Reset</button>
        </form>
    
        <!-- Display the response if available -->
        <div v-if="response" class="response-container">
	  <div v-if="response.operation_mode==='tcp'">
	    <h3>General Information</h3>
	    <p><strong>Gateway operation mode:</strong> <font color=#272af2>{{ response.operation_mode }}</font></p>
	    <p><strong>Istio cluster name:</strong> <font color=#272af2>{{ response.cluster }}</font></p>
	    <h3>Endpoints:</h3>
	    <div v-if="response.tcp_normal_cluster">
	      <ul>
                <li v-for="(backend, index) in response.tcp_normal_cluster.normal_cluster_endpoints" :key="index">
                  <b>Endpoint:</b> <font color=#272af2> {{ backend.endpoint }} </font> <b>Status:</b> <font color=#272af2> {{ backend.status }} </font> <b>Outlier_Checker:</b> <font color=#272af2> {{ backend.outlier_check }} </font>
                </li>
              </ul>
	    </div>
	    <div v-if="response.tcp_weighted_clusters">
	      <ul>
	        <li v-for="(cluster, index) in response.tcp_weighted_clusters" :key="index">
		  <b>ClusterName:</b> <font color=#272af2>{{ cluster.cluster_name }}</font> <b>ClusterWeight:</b> <font color=#272af2>{{ cluster.cluster_weight }}</font>
		  <ul>
		    <li v-for="(endpoint,index) in cluster.weighted_cluster_endpoints" :key="index">
                      <b>Endpoint:</b> <font color=#272af2>{{ endpoint.endpoint }}</font> <b>Status:</b> <font color=#272af2>{{ endpoint.status }}</font> <b>Outlier_Checker:</b> <font color=#272af2>{{ endpoint.outlier_check }}</font>
		    </li>
		  </ul>
		</li>
	      </ul>
	    </div>
	  </div>
	  <div v-if="response.operation_mode==='http'">
            <p><strong>Gateway operation mode:</strong> {{ response.operation_mode }}</p>
            <p><strong>Route:</strong> {{ response.cluster }}</p>
            <h3>Certificate Information</h3>
            <p><strong>Certificate name:</strong> {{ response.certificate }}</p>
            <p><strong>Certificate status:</strong> {{ response.certificate_status }}</p>
    
            <h3>Backends</h3>
            <ul>
              <li v-for="(backend, index) in response.backends" :key="index">
    	        Backend IP: {{ backend.backendIp }}
    	      </li>
            </ul>
          </div>
	</div>
      </div>	
    </main>
    <footer class="footer">
      <p>Need Help? Contact NZ Managed Kubernetes Service Team for support</p>
    </footer>
  </div>  
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 100vw;
  background-color: #96173f;
  color: #96173f;
  /**
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  **/
}

.header {
  padding: 20px;
  background-color: #2C3E50;
  color: #ECF0F1;
  text-align: center;
}

.header h1 {
  margin: 0;
}

.header p {
  margin: 5px 0 0;
  font-size: 16px;
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ECF0F1;
  padding: 20px;
}

.form-container {
  min-width: 300px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

label {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
}

input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.submit-button, .reset-button {
  padding: 10px;
  font-size: 16px;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  margin-right: 10px;
  transition: background-color 0.3s ease;
}

.submit-button {
    background-color: #007bff;
}

.reset-button {
    background-color: #dc3545;
}

.submit-button:hover {
  background-color: #0056b3;
}

.reset-button:hover {
    background-color: #c82333;
}

.response-container {
  margin-top: 30px;
  padding: 15px;
  background-color: #eaf5ea;
  border: 1px solid #4caf50;
  border-radius: 5px;
}

.response-container h3 {
  color: #4caf50;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 5px 0;
}

.footer {
  padding: 10px;
  background-color: #34495E;
  text-align: center;
  font-size: 15px;
  color: #ECF0F1;
}
</style>

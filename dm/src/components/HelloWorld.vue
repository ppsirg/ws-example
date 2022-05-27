<template>
  <div>
    <div>my connection: {{conn_id}}</div>
    <div>new key: {{new_key}}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';


// const props = defineProps(['msg'])
let conn_id = ref('')
let new_key = ref('')

let ws = new WebSocket("ws://localhost:8000/ws/");
ws.onopen = function(e) {
  console.log("[open] Connection established");
  console.log("Sending to server");
  console.log({e});
  ws.send("get_name");
};

ws.onmessage = function(event) {
  let info = JSON.parse(event.data)
  console.log({info});
  if (info.name) {
    conn_id.value = info.name
  }
  if (info.new) {
    new_key.value = info.new
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

<template>
  <div>
    <h1>Trading Data</h1>
    <ul>
      <li v-for="data in tradingData" :key="data.id">
        {{ data.symbol }}: {{ data.price }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tradingData: []
    }
  },
  mounted() {
    fetch('http://localhost:5000/trading-data')
      .then(response => response.json())
      .then(data => {
        this.tradingData = data;
      });
  }
}
</script>

<style scoped>
/* Add some styles here */
</style>

import React, { useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [symbol, setSymbol] = useState('');
  const [prices, setPrices] = useState([]);
  const [message, setMessage] = useState('');

  const handleTrade = () => {
    axios.post('http://localhost:5000/trade', { symbol, prices })
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('There was an error placing the trade!', error);
      });
  };

  return (
    <div>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Stock Symbol"
      />
      <textarea
        value={prices.join(',')}
        onChange={(e) => setPrices(e.target.value.split(',').map(Number))}
        placeholder="Enter prices separated by commas"
      />
      <button onClick={handleTrade}>Execute Trade</button>
      <p>{message}</p>
    </div>
  );
}

export default Dashboard;

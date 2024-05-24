import React, { useEffect, useState } from 'react';
import axios from 'axios';

function TradeHistory() {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/trade_history')
      .then(response => {
        setTrades(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the trade history!', error);
      });
  }, []);

  return (
    <div>
      <h2>Trade History</h2>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Quantity</th>
            <th>Order Type</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((trade, index) => (
            <tr key={index}>
              <td>{trade.symbol}</td>
              <td>{trade.quantity}</td>
              <td>{trade.order_type}</td>
              <td>{new Date(trade.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TradeHistory;

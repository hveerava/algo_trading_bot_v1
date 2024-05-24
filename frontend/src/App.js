import React from 'react';
import './index.css';

function App() {
  // Handler function for executing trade
  const handleExecuteTrade = () => {
    var symbol = document.getElementById('stockSymbolInput').value;
    var prices = document.getElementById('pricesInput').value.split(',');

    fetch('/executeTrade', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ symbol: symbol, prices: prices })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Trade executed successfully:', data);
      })
      .catch(error => {
        console.error('Error executing trade:', error);
      });
  };

  return (
    <div className="App">
      {/* Input fields and button */}
      <label htmlFor="stockSymbolInput">Stock Symbol:</label>
      <input type="text" id="stockSymbolInput" name="stockSymbolInput" />
      <br />
      <label htmlFor="pricesInput">Prices (comma-separated):</label>
      <input type="text" id="pricesInput" name="pricesInput" />
      <br />
      <button id="executeTradeButton" onClick={handleExecuteTrade}>
        Execute Trade
      </button>
    </div>
  );
}

export default App;

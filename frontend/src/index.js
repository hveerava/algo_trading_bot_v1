import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// Check for JavaScript errors
window.onerror = function(message, source, lineno, colno, error) {
  console.error('Error:', message, 'Source:', source, 'Line:', lineno, 'Column:', colno, 'Error object:', error);
};

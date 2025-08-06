// /frontend/server.js
const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  // --- THIS IS THE LINE TO CHANGE ---
  const initialBotMessage = "Welcome! I am Orion, your AI support assistant. How can I help you today?";
  res.render('index', { initialBotMessage: initialBotMessage });
});

app.listen(PORT, () => {
  console.log(`Frontend server running at http://localhost:${PORT}`);
});
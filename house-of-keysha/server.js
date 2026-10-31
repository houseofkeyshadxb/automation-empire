const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname)));
app.use(express.json());

// Health check
app.get('/health', (req, res) => res.json({status: 'alive'}));

// Chat endpoint - wire to existing AI
app.post('/api/chat', async (req, res) => {
  const { message, persona } = req.body;
  // This will connect to your existing Groq/maxine logic
  res.json({ 
    response: "✓ Chat connected to your AI system",
    persona: persona || 'Keysha'
  });
});

app.listen(process.env.PORT || 3000, () => {
  console.log('House of Keysha Empire is LIVE');
});

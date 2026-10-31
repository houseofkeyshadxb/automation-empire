'use client';
import { useState } from 'react';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{role: string, content: string}[]>([
    { role: 'assistant', content: 'Welcome to the House. I am Maxine, your private concierge. How may I assist you today? 💋' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionKey] = useState(() => 'web_' + Math.random().toString(36).substring(2, 10));

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('/api/chat/completions', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': 'Bearer maxine2026secret' // We will secure this later
        },
        body: JSON.stringify({
          model: 'maxine',
          user: sessionKey,
          messages: newMessages.map(m => ({ role: m.role === 'assistant' ? 'assistant' : 'user', content: m.content }))
        })
      });
      const data = await res.json();
      const reply = data.choices?.[0]?.message?.content || "Connection error.";
      setMessages([...newMessages, { role: 'assistant', content: reply }]);
    } catch (err) {
      setMessages([...newMessages, { role: 'assistant', content: "I'm having trouble connecting right now." }]);
    }
    setIsLoading(false);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 font-sans">
      {isOpen && (
        <div className="w-80 h-96 bg-espresso border border-champagne shadow-2xl flex flex-col mb-4">
          <div className="bg-obsidian p-4 border-b border-champagne/30 flex justify-between items-center">
            <h3 className="font-serif text-champagne tracking-widest uppercase text-sm">Maxine Concierge</h3>
            <button onClick={() => setIsOpen(false)} className="text-muted hover:text-ivory">✕</button>
          </div>
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] p-3 text-sm ${m.role === 'user' ? 'bg-burgundy text-ivory' : 'bg-obsidian border border-muted/30 text-muted'}`}>
                  {m.content}
                </div>
              </div>
            ))}
            {isLoading && <div className="text-muted text-xs italic">Maxine is typing...</div>}
          </div>
          <div className="p-4 border-t border-champagne/30 flex gap-2">
            <input 
              type="text" 
              value={input} 
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
              placeholder="Type a message..."
              className="flex-1 bg-obsidian border border-muted/50 p-2 text-sm text-ivory focus:outline-none focus:border-champagne"
            />
            <button onClick={sendMessage} className="bg-burgundy text-ivory px-4 text-sm hover:bg-burgundy/80 transition-all">
              Send
            </button>
          </div>
        </div>
      )}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-16 h-16 bg-burgundy border border-champagne rounded-full flex items-center justify-center shadow-lg hover:scale-105 transition-transform"
      >
        <span className="font-serif text-champagne text-2xl">M</span>
      </button>
    </div>
  );
}

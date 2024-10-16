import React, { useEffect, useState } from 'react';

function ChatStream({ workflow, query }) {
  const [result, setResult] = useState('');

  useEffect(() => {
    if (!query) return;

    const fetchData = async () => {
      const response = await fetch(`http://127.0.0.1:8000/streaming_sync/chat/${workflow}?query=${encodeURIComponent(query)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'text/event-stream'
        }
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let content = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        content += decoder.decode(value, { stream: true });
        setResult((prev) => prev + content);
      }
    };

    fetchData();
  }, [query, workflow]);

  return (
    <div className="chat-result">
      <h2>Streamed Result:</h2>
      <pre>{result}</pre>
    </div>
  );
}

export default ChatStream;

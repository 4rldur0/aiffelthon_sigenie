import React, { useEffect, useState } from 'react';

function ChatStream({ workflow, query }) {
  const [result, setResult] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!query) return;
    
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/streaming_sync/chat/${workflow}?query=${encodeURIComponent(query)}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let content = '';
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          content = decoder.decode(value, { stream: true });
          setResult((prev) => prev + content);
        }
      } catch (error) {
        setError('Error fetching data: ' + error.message);
      }
    };

    fetchData();
  }, [query, workflow]);

  return (
    <div className="chat-result">
      <h2>Streamed Result:</h2>
      {error ? (
        <p className="error-message">{error}</p>
      ) : (
        <pre>{result}</pre>
      )}
    </div>
  );
}

export default ChatStream;

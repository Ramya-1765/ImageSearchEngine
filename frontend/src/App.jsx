import React, { useState } from 'react';

function App() {
  const [queryText, setQueryText] = useState('');
  const [queryImage, setQueryImage] = useState(null);
  const [results, setResults] = useState([]);

  const handleTextSearch = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('query_text', queryText);

    const res = await fetch('http://localhost:5010/search', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    setResults(data.results || []);
  };

  const handleImageSearch = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('query_image', queryImage);

    const res = await fetch('http://localhost:5010/search', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    setResults(data.results || []);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Search by Text</h2>
      <form onSubmit={handleTextSearch}>
        <input
          type="text"
          value={queryText}
          onChange={(e) => setQueryText(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      <h2>Search by Image</h2>
      <form onSubmit={handleImageSearch}>
        <input
          type="file"
          onChange={(e) => setQueryImage(e.target.files[0])}
        />
        <button type="submit">Search</button>
      </form>

      {results.length > 0 && (
        <>
          <h3>Results:</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap' }}>
            {results.map((img, index) => (
              <img
                key={index}
                src={`http://localhost:5010/${img}`}
                alt={`result-${index}`}
                width="200"
                style={{ margin: '10px' }}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;

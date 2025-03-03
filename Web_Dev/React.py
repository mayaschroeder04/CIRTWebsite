import React, { useState, useEffect } from "react";

const FileCollector = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/files/") // Django API endpoint to fetch files
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch files");
        }
        return response.json();
      })
      .then((data) => {
        // Filter only .js, .css, and .html files
        const filteredFiles = data.files.filter((file) =>
          /\.(js|css|html)$/i.test(file)
        );
        setFiles(filteredFiles);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading files...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Collected Files</h2>
      <ul>
        {files.map((file, index) => (
          <li key={index}>
            <a href={`/static/${file}`} download>
              {file}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileCollector;

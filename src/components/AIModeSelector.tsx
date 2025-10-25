import React, { useState } from "react";
import { fetchAIResponse } from "../services/aiService";

const AIModeSelector = () => {
  const [mode, setMode] = useState<"math" | "english" | "history" | "default">("default");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false); // Added loading state for better UX

  const handleModeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setMode(event.target.value as "math" | "english" | "history" | "default");
  };

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async () => {
    if (!query.trim()) {
      setResponse("Please enter a query.");
      return;
    }

    setLoading(true); // Set loading to true before making the API call
    try {
      const aiResponse = await fetchAIResponse(mode, query);
      if (typeof aiResponse === "string") {
        setResponse(aiResponse);
      } else {
        setResponse("Invalid response received.");
      }
    } catch (error) {
      console.error("Error fetching AI response:", error);
      setResponse("Error fetching response. Please try again.");
    } finally {
      setLoading(false); // Reset loading state after the API call
    }
  };

  return (
    <div>
      <h1>AI Mode Selector</h1>
      <div>
        <label htmlFor="mode">Select Mode:</label>
        <select id="mode" value={mode} onChange={handleModeChange}>
          <option value="default">Default</option>
          <option value="math">Math</option>
          <option value="english">English</option>
          <option value="history">History</option>
        </select>
      </div>
      <div>
        <label htmlFor="query">Enter Query:</label>
        <input
          id="query"
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Type your query here..."
        />
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Loading..." : "Submit"}
      </button>
      <div>
        <h2>Response:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
};

export default AIModeSelector;

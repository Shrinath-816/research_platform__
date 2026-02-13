import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFiles([...e.target.files]);
  };

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      return alert("Please select files");
    }

    setLoading(true);
    setAnalyses([]);

    const results = [];

    for (let i = 0; i < files.length; i++) {
      const formData = new FormData();
      formData.append("file", files[i]);

      try {
        const response = await axios.post(
          "https://research-platform-0s31.onrender.com/analyze",
          formData
        );

        results.push({
          filename: files[i].name,
          analysis: response.data.analysis,
        });
      } catch (error) {
        results.push({
          filename: files[i].name,
          analysis: { error: "Processing failed" },
        });
      }
    }

    setAnalyses(results);
    setLoading(false);
  };

  const getToneClass = (tone) => {
    if (tone === "Optimistic") return "badge green";
    if (tone === "Cautious") return "badge yellow";
    if (tone === "Pessimistic") return "badge red";
    return "badge gray";
  };

  const getConfidenceClass = (level) => {
    if (level === "High") return "badge green";
    if (level === "Medium") return "badge yellow";
    return "badge red";
  };

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(analyses, null, 2)], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "analysis_results.json";
    a.click();
  };

  const downloadCSV = () => {
    if (analyses.length === 0) return;

    const rows = analyses.map((item) => {
      const a = item.analysis || {};

      return {
        filename: item.filename,
        document_type: a.document_type || "",
        management_tone: a.management_tone || "",
        confidence_level: a.confidence_level || "",
        revenue_guidance: a.forward_guidance?.revenue || "",
        margin_guidance: a.forward_guidance?.margin || "",
        capex_guidance: a.forward_guidance?.capex || "",
        capacity_utilization: a.capacity_utilization || "",
      };
    });

    const headers = Object.keys(rows[0]).join(",");
    const csvRows = rows.map((row) =>
      Object.values(row).map((val) => `"${val}"`).join(",")
    );

    const csvContent = headers + "\n" + csvRows.join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "multi_analysis.csv";
    a.click();
  };

  return (
    <div className="container">
      <h1>AI Research Portal</h1>

      <div className="upload-section">
        <input type="file" multiple onChange={handleFileChange} />
        <button onClick={handleUpload}>Run Analysis</button>
      </div>

      {analyses.length > 0 && (
        <div className="export-buttons">
          <button onClick={downloadJSON}>Download JSON</button>
          <button onClick={downloadCSV}>Download CSV</button>
        </div>
      )}

      {loading && <p>Processing documents...</p>}

      {analyses.length > 0 &&
        analyses.map((item, idx) => {
          const analysis = item.analysis;

          if (analysis.error) {
            return (
              <div key={idx} className="card">
                <h2>{item.filename}</h2>
                <p style={{ color: "red" }}>Error processing file.</p>
              </div>
            );
          }

          return (
            <div key={idx} className="results">
              <h2>{item.filename}</h2>

              {analysis.document_type === "Unsupported" && (
                <div className="alert">
                  ⚠ Unsupported Document – Not an earnings transcript
                </div>
              )}

              <div className="card">
                <p>
                  <strong>Document Type:</strong>{" "}
                  {analysis.document_type}
                </p>

                <p>
                  <strong>Management Tone:</strong>{" "}
                  <span className={getToneClass(analysis.management_tone)}>
                    {analysis.management_tone}
                  </span>
                </p>

                <p>
                  <strong>Confidence:</strong>{" "}
                  <span className={getConfidenceClass(
                    analysis.confidence_level
                  )}>
                    {analysis.confidence_level}
                  </span>
                </p>

                <p>
                  <strong>Reasoning:</strong>{" "}
                  {analysis.confidence_reasoning}
                </p>
              </div>

              <div className="card">
                <h3>Key Positives</h3>
                <ul>
                  {analysis.key_positives.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3>Key Concerns</h3>
                <ul>
                  {analysis.key_concerns.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3>Forward Guidance</h3>
                <p>
                  <strong>Revenue:</strong>{" "}
                  {analysis.forward_guidance?.revenue}
                </p>
                <p>
                  <strong>Margin:</strong>{" "}
                  {analysis.forward_guidance?.margin}
                </p>
                <p>
                  <strong>Capex:</strong>{" "}
                  {analysis.forward_guidance?.capex}
                </p>
              </div>

              <div className="card">
                <h3>Capacity Utilization</h3>
                <p>{analysis.capacity_utilization}</p>
              </div>

              <div className="card">
                <h3>Growth Initiatives</h3>
                <ul>
                  {analysis.growth_initiatives.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default App;

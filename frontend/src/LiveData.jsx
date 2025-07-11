import React, { useEffect, useState } from "react";

function LiveData() {
  const [metrics, setMetrics] = useState({});

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8765');

    ws.onmessage = (event) => {
      const updates = {};
      const pairs = event.data.split(",");

      pairs.forEach((pair) => {
        const [key, value] = pair.split(":");
        if (key && value) {
          updates[key.trim()] = value.trim();
        }
      });

      setMetrics((prev) => ({ ...prev, ...updates }));
    };

    ws.onerror = () => {
      setMetrics({ Error: "WebSocket connection error" });
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "monospace" }}>
      <h2>Live CAREN Metrics</h2>
      {Object.keys(metrics).length === 0 ? (
        <p>Waiting for data...</p>
      ) : (
        <table>
          <tbody>
            {Object.entries(metrics).map(([key, value]) => (
              <tr key={key}>
                <td style={{ paddingRight: "1em", fontWeight: "bold" }}>{key}:</td>
                <td>{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default LiveData;

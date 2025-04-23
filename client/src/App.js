import logo from "./soccer.svg";
import "./App.css";
import React, { useState } from "react";

function App() {
  const defaultStatJson = `{
  "stats": {
    "NAME": {
      "PAC": 60.0,
      "SHO": 65.0,
      "PAS": 71.0,
      "DRI": 76.0,
      "DEF": 67.0,
      "PHY": 74.0,
      "Acceleration": 70.0,
      "Sprint Speed": 62.0,
      "Positioning": 72.0,
      "Finishing": 68.0,
      "Shot Power": 74.0,
      "Long Shots": 72.0,
      "Volleys": 69.0,
      "Penalties": 75.0,
      "Vision": 75.0,
      "Crossing": 70.0,
      "Free Kick Accuracy": 67.0,
      "Short Passing": 76.0,
      "Long Passing": 73.0,
      "Curve": 71.0,
      "Dribbling": 72.0,
      "Agility": 64.0,
      "Balance": 73.0,
      "Reactions": 66.0,
      "Ball Control": 73.0,
      "Composure": 70.0,
      "Interceptions": 65.0,
      "Heading Accuracy": 59.0,
      "Def Awareness": 62.0,
      "Standing Tackle": 68.0,
      "Sliding Tackle": 52.0,
      "Jumping": 59.0,
      "Stamina": 55.0,
      "Strength": 77.0,
      "Aggression": 64.0,
      "Skill moves": 5.0,
      "Weak foot": 1.0,
      "Height": 185.0,
      "GK Diving": 0.0,
      "GK Handling": 0.0,
      "GK Kicking": 0.0,
      "GK Positioning": 0.0,
      "GK Reflexes": 0.0
    }
  }
}`;

  const defaultNameJson = `{
  "players": [
    "Kylian Mbappe", "Jude Bellingham", "Vini Jr.", "Federico Valverde",
    "Rodrygo", "Carvajal", "Eduardo Camavinga",
    "David Alaba", "Ferland Mendy", "Antonio Rüdiger", "Thibaut Courtois"
  ]
}`;

  const [statJson, setStatJson] = useState(defaultStatJson);
  const [nameJson, setNameJson] = useState(defaultNameJson);
  const [statResponse, setStatResponse] = useState(null);
  const [formResponse, setFormResponse] = useState(null);
  const [error, setError] = useState("");
  const [showStatModal, setShowStatModal] = useState(false);
  const [showFormModal, setShowFormModal] = useState(false);

  const handleStatPredict = async () => {
    try {
      const parsed = JSON.parse(statJson);
      setError("");

      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed),
      });

      const data = await res.json();
      setStatResponse(data);
      setShowStatModal(true);
    } catch (e) {
      setError("Error in Stat Prediction: " + e.message);
    }
  };

  const handleFormationPredict = async () => {
    try {
      const parsed = JSON.parse(nameJson);
      if (!parsed.players || parsed.players.length !== 11) {
        setError("Exactly 11 players must be listed.");
        return;
      }
      setError("");

      const res = await fetch("http://127.0.0.1:8000/predict/formation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed),
      });

      const data = await res.json();
      setFormResponse(data);
      setShowFormModal(true);
    } catch (e) {
      setError("Error in Formation Prediction: " + e.message);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <img src={logo} alt="Logo" className="app-logo" />
        <h1>Football AI Assistant</h1>
      </header>

      <div className="section-container">
        <section className="section">
          <h2>Predict Position & OVR</h2>
          <textarea
            className="json-input"
            value={statJson}
            onChange={(e) => setStatJson(e.target.value)}
          />
          <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
            <button className="action-button" onClick={handleStatPredict}>
              Predict Position
            </button>
          </div>
        </section>

        <section className="section">
          <h2>Recommend Best Formation</h2>
          <textarea
            className="json-input"
            value={nameJson}
            onChange={(e) => setNameJson(e.target.value)}
          />
          <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
            <button className="action-button" onClick={handleFormationPredict}>
              Get Formation
            </button>
          </div>
        </section>
      </div>

      {error && <div className="error">{error}</div>}

      {showStatModal && statResponse && (
        <div className="modal-overlay" onClick={() => setShowStatModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Stat Prediction Result</h3>
            <pre>{JSON.stringify(statResponse, null, 2)}</pre>
            <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
              <button className="modal-close" onClick={() => setShowStatModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {showFormModal && formResponse && formResponse.formation && (
        <div className="modal-overlay" onClick={() => setShowFormModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Best Formation: {formResponse.formation}</h3>
            <p>Total OVR: {formResponse.total_OVR}</p>
            <ul>
              {formResponse.assignments.map((a, i) => (
                <li key={i}>
                  {a[0]} - {a[1]} (OVR: {a[2].toFixed(2)})
                </li>
              ))}
            </ul>
            {formResponse.all_formations && (
              <>
                <h4>All Formation Evaluations</h4>
                <ul>
                  {formResponse.all_formations.map(([f, s], i) => (
                    <li key={i}>
                      {f.padEnd(15)} → Total OVR: {s.toFixed(2)}
                    </li>
                  ))}
                </ul>
              </>
            )}
            <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
              <button className="modal-close" onClick={() => setShowFormModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

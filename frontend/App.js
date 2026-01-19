import React, { useState} from "react";

import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [chatInput, setChatInput] = useState("");
  const [status, setStatus] = useState("");

  const getCurrentDate = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const getCurrentTime = () => {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    return `${hours}:${minutes}`;
  };

  const [chatHistory, setChatHistory] = useState([
    {
      type: "bot",
      text: 'Log interaction details here (e.g., "Met Dr. Smith, discussed Prodo-X efficacy...") or ask for help.'
    }
  ]);

const [formData, setFormData] = useState(() => {
  const saved = localStorage.getItem("interaction_time");
  if (saved) return JSON.parse(saved);

  const data = {
    hcp_name: "",
    interaction_type: "Meeting",
    date: getCurrentDate(),
    time: getCurrentTime(),
    attendees: "",
    topics_discussed: "",
    materials_shared: "Brochures.",
    sentiment: "",
    outcomes: "",
    follow_up_actions: "",
    summary: ""
  };

  localStorage.setItem("interaction_time", JSON.stringify(data));
  return data;
});


  /* -------------------- FORM CHANGE -------------------- */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  /* -------------------- CHAT → AI -------------------- */
  const sendToAI = async () => {
    if (!chatInput.trim()) return;

    const userMsg = { type: "user", text: chatInput };
    setChatHistory(prev => [...prev, userMsg]);
    setStatus("AI processing...");

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: chatInput })
      });

      const data = await res.json();

      /* TOOL HANDLING */
      if (data.tool === "extract") {
        setFormData(prev => ({
          ...prev,
          ...data.data,
          date: prev.date,   // 🔒 keep UI date
          time: prev.time    // 🔒 keep UI time
        }));
        setChatHistory(prev => [...prev, { type: "bot", text: "Form auto-filled successfully ✅" }]);
      }

      if (data.tool === "edit") {
        setFormData(prev => ({
          ...prev,
          [data.field]: data.value
        }));

          setChatHistory(prev => [
            ...prev,
            { type: "bot", text: `${data.field} updated to ${data.value} ✅` }
          ]);  
        }


      if (data.tool === "history") {
        setChatHistory(prev => [...prev, { type: "bot", text: JSON.stringify(data.result, null, 2) }]);
      }

      if (data.tool === "followup") {
        setFormData(prev => ({ ...prev, follow_up_actions: data.result }));
        setChatHistory(prev => [...prev, { type: "bot", text: data.result }]);
      }

      setStatus("Done ✅");
      setChatInput("");
    } catch (err) {
      console.error(err);
      setChatHistory(prev => [...prev, { type: "bot", text: "Error connecting to AI ❌" }]);
      setStatus("Error");
    }
  };

  /* -------------------- SAVE -------------------- */
  const saveInteraction = async () => {
    await fetch(`${API_BASE}/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    });
  };


  return (
    <div className="app-container">

      {/* ================= LEFT PANEL ================= */}
      <div className="left-panel">
        <h1>Log HCP Interaction</h1>

        <div className="row">
          <div className="field">
            <label>HCP Name</label>
            <input name="hcp_name" value={formData.hcp_name} onChange={handleChange} placeholder="e.g. Dr. Smith" />
          </div>

          <div className="field">
            <label>Interaction Type</label>
            <select name="interaction_type" value={formData.interaction_type} onChange={handleChange}>
              <option>Meeting</option>
              <option>Call</option>
              <option>Email</option>
            </select>
          </div>
        </div>

        <div className="row">
          <div className="field">
            <label>Date</label>
            <input type="date" name="date" value={formData.date} onChange={handleChange} />
          </div>

          <div className="field">
            <label>Time</label>
            <input type="time" name="time" value={formData.time} onChange={handleChange} />
          </div>
        </div>

        <div className="field">
          <label>Attendees</label>
          <input name="attendees" value={formData.attendees} onChange={handleChange} placeholder="Enter names..." />
        </div>

        <div className="field">
          <label>Topics Discussed</label>
          <textarea rows="4" name="topics_discussed" value={formData.topics_discussed} onChange={handleChange}></textarea>
          <span className="voice">🎤 Summarize from Voice Note</span>
        </div>

        <div className="section">
          <label>Materials Shared</label>
          <div className="inline-box">
            <span>{formData.materials_shared}</span>
            <button>🔍 Search/Add</button>
          </div>
        </div>

        <div className="section">
          <label>Samples Distributed</label>
          <div className="inline-box">
            <span>No samples added.</span>
            <button>＋ Add Sample</button>
          </div>
        </div>

        <div className="section">
          <label>Observed / Inferred HCP Sentiment</label>
          <div className="sentiment">
            {["Positive", "Neutral", "Negative"].map(s => (
              <label key={s}>
                <input type="radio" name="sentiment" value={s} checked={formData.sentiment === s} onChange={handleChange} />
                {s}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label>Outcomes</label>
          <textarea rows="3" name="outcomes" value={formData.outcomes} onChange={handleChange} placeholder="Key outcomes or agreements..." />
        </div>

        <div className="field">
          <label>Follow-up Actions</label>
          <textarea rows="2" name="follow_up_actions" value={formData.follow_up_actions} onChange={handleChange} />
        </div>

        <button className="save-btn" onClick={saveInteraction}>Save Interaction</button>
        <div className="status">{status}</div>
      </div>

      {/* ================= RIGHT PANEL ================= */}
      <div className="right-panel">
        <div className="chat-header">🤖 AI Assistant</div>

        <div className="chat-body">
          {chatHistory.map((m, i) => (
            <div key={i} className={`chat-msg ${m.type}`}>{m.text}</div>
          ))}
        </div>

        <div className="chat-input">
          <input
            placeholder="Describe Interaction..."
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendToAI()}
          />
          <button onClick={sendToAI}>A<br />Log</button>
        </div>
      </div>

    </div>
  );
}

export default App;

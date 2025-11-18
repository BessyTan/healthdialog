import React, { useState } from "react";
import ChatMessage from "./components/ChatMessage.jsx";
import SourceCard from "./components/SourceCard.jsx";

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi, I’m HealthDialog. I can help you triage symptoms based on clinical guidelines. " +
        "I do NOT replace a doctor or emergency care. What’s going on today?",
      meta: null
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastSources, setLastSources] = useState([]);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const query = input.trim();
    if (!query || loading) return;

    setError("");
    setInput("");

    const userMsg = { role: "user", content: query };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const url = `http://localhost:8000/ask?query=${encodeURIComponent(
        query
      )}`;

      const res = await fetch(url, {
        method: "GET",
        headers: {
          "Accept": "application/json"
        }
      });

      if (!res.ok) {
        throw new Error(`Backend error: ${res.status}`);
      }

      const data = await res.json();

      const assistantMsg = {
        role: "assistant",
        content: data.answer || String(data),
        meta: {
          confidence: data.confidence,
          hallucination_risk: data.hallucination_risk
        }
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setLastSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (err) {
      console.error(err);
      setError(
        "Something went wrong talking to the triage backend. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <div>
          <h1>HealthDialog</h1>
          <p className="subtitle">
            Clinically grounded health triage chatbot (RAG + hallucination detection)
          </p>
        </div>
        <div className="header-pill">
          ⚠️ Not a substitute for emergency care.
        </div>
      </header>

      <main className="main-layout">
        <section className="chat-panel">
          <div className="chat-window">
            {messages.map((m, idx) => (
              <ChatMessage
                key={idx}
                role={m.role}
                content={m.content}
                meta={m.meta}
              />
            ))}
            {loading && (
              <div className="typing-indicator">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </div>
            )}
          </div>

          <form className="input-row" onSubmit={handleSubmit}>
            <textarea
              className="input-box"
              rows={2}
              placeholder="Describe your symptom (e.g. 'I have chest pain and shortness of breath')..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button
              className="send-btn"
              type="submit"
              disabled={loading || !input.trim()}
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </form>

          {error && <div className="error-banner">{error}</div>}
        </section>

        <aside className="sidebar">
          <h2>Evidence & Sources</h2>
          <p className="sidebar-caption">
            These are the clinical documents retrieved by the RAG pipeline for the
            latest answer.
          </p>

          {lastSources.length === 0 && (
            <p className="no-sources">
              Ask a question to see guideline references and FAQs here.
            </p>
          )}

          <div className="sources-list">
            {lastSources.map((src, idx) => (
              <SourceCard key={idx} source={src} />
            ))}
          </div>

          <div className="disclaimer">
            <strong>Important:</strong> This system is for information and
            triage support only. It does not provide a diagnosis, and it does
            not replace a doctor or emergency services.
          </div>
        </aside>
      </main>
    </div>
  );
}

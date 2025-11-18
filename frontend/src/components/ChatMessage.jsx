import React from "react";

export default function ChatMessage({ role, content, meta }) {
  const isUser = role === "user";

  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      <div className="avatar">
        {isUser ? "🧑" : "🩺"}
      </div>
      <div className="bubble">
        <p className="message-text">{content}</p>

        {!isUser && meta && (
          <div className="meta">
            {typeof meta.confidence === "number" && (
              <span className="badge">
                Confidence: {(meta.confidence * 100).toFixed(0)}%
              </span>
            )}
            {meta.hallucination_risk && (
              <span className={`badge badge-${meta.hallucination_risk}`}>
                Hallucination risk: {meta.hallucination_risk}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

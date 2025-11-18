import React from "react";

export default function SourceCard({ source }) {
  return (
    <div className="source-card">
      <div className="source-title">{source.title || "Source"}</div>
      {source.snippet && (
        <p className="source-snippet">{source.snippet}</p>
      )}
      {source.url && (
        <a
          className="source-link"
          href={source.url}
          target="_blank"
          rel="noreferrer"
        >
          View source ↗
        </a>
      )}
    </div>
  );
}

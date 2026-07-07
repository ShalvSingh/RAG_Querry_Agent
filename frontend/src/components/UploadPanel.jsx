import { useRef, useState } from "react";
import { uploadDocument } from "../api/client.js";

export default function UploadPanel({ document, onDocumentReady }) {
  const [status, setStatus] = useState("idle"); // idle | uploading | error
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  async function handleFile(file) {
    if (!file) return;
    setStatus("uploading");
    setError("");
    try {
      const data = await uploadDocument(file);
      onDocumentReady(data.document);
      setStatus("idle");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  }

  return (
    <aside className="panel">
      <div className="panel-eyebrow">01 · Source</div>
      <h2 className="panel-title">Load a document</h2>
      <p className="panel-copy">
        Upload a PDF. It's chunked, embedded, and stored so questions are
        answered only from what's actually on the page.
      </p>

      <label
        className={`dropzone ${status === "uploading" ? "dropzone-busy" : ""}`}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          handleFile(e.dataTransfer.files[0]);
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          hidden
          onChange={(e) => handleFile(e.target.files[0])}
        />
        {status === "uploading" ? (
          <span>Processing…</span>
        ) : (
          <span>Drop a PDF here, or click to browse</span>
        )}
      </label>

      {status === "error" && <p className="panel-error">{error}</p>}

      {document && (
        <div className="doc-card">
          <div className="doc-card-name">{document.filename}</div>
          <div className="doc-card-meta">
            {document.num_chunks} chunks indexed · id {document.doc_id}
          </div>
        </div>
      )}
    </aside>
  );
}

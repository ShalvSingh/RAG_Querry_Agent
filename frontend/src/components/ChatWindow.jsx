import { useEffect, useRef, useState } from "react";
import { askQuestion } from "../api/client.js";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatWindow({ document }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend() {
    const question = input.trim();
    if (!question || !document || loading) return;

    setMessages((m) => [...m, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const data = await askQuestion(document.doc_id, question);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: data.answer, sources: data.sources },
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Something went wrong: ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="chat">
      <div className="panel-eyebrow">02 · Ask</div>
      <h2 className="panel-title">Question the document</h2>

      <div className="chat-scroll" ref={scrollRef}>
        {messages.length === 0 && (
          <div className="chat-empty">
            {document
              ? "Ask anything about the uploaded document."
              : "Upload a document on the left to begin."}
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} sources={m.sources} />
        ))}
        {loading && (
          <div className="bubble-row">
            <div className="bubble bubble-assistant bubble-loading">Reading the document…</div>
          </div>
        )}
      </div>

      <div className="chat-input-row">
        <input
          type="text"
          placeholder={document ? "Ask a question…" : "Upload a document first"}
          value={input}
          disabled={!document || loading}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} disabled={!document || loading || !input.trim()}>
          Ask
        </button>
      </div>
    </main>
  );
}

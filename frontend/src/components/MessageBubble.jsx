export default function MessageBubble({ role, content, sources }) {
  const isUser = role === "user";
  return (
    <div className={`bubble-row ${isUser ? "bubble-row-user" : ""}`}>
      <div className={`bubble ${isUser ? "bubble-user" : "bubble-assistant"}`}>
        <p>{content}</p>
        {sources && sources.length > 0 && (
          <div className="sources">
            {sources.map((s, i) => (
              <div className="source-tab" key={i}>
                <span className="source-page">
                  {s.page !== null && s.page !== undefined ? `p.${s.page + 1}` : "—"}
                </span>
                <span className="source-snippet">{s.snippet}…</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

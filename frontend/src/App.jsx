import { useState } from "react";
import UploadPanel from "./components/UploadPanel.jsx";
import ChatWindow from "./components/ChatWindow.jsx";

export default function App() {
  const [document, setDocument] = useState(null);

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand-mark">§</div>
        <div>
          <div className="brand-name">Marginalia</div>
          <div className="brand-tag">grounded answers, straight from the page</div>
        </div>
      </header>

      <div className="app-body">
        <UploadPanel document={document} onDocumentReady={setDocument} />
        <ChatWindow document={document} />
      </div>
    </div>
  );
}

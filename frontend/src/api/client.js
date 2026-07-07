const BASE_URL = "http://localhost:8000";

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Upload failed.");
  }
  return res.json();
}

export async function askQuestion(docId, question) {
  const res = await fetch(`${BASE_URL}/chat/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doc_id: docId, question }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to get an answer.");
  }
  return res.json();
}

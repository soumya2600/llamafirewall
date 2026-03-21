// api.js — API calls to the FastAPI backend
export const BASE_URL = "http://127.0.0.1:8000";

export async function pingBackend() {
  try {
    const res = await fetch(`${BASE_URL}/`, { signal: AbortSignal.timeout(3000) });
    return res.ok;
  } catch {
    return false;
  }
}

export async function checkPrompt(prompt) {
  const res = await fetch(`${BASE_URL}/check-prompt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
    signal: AbortSignal.timeout(8000),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }
  return res.json();
}

export async function fetchLogs() {
  const res = await fetch(`${BASE_URL}/logs`, {
    signal: AbortSignal.timeout(5000),
  });
  if (!res.ok) throw new Error("Failed to fetch logs");
  return res.json();
}

export async function clearLogs() {
  const res = await fetch(`${BASE_URL}/logs`, {
    method: "DELETE",
    signal: AbortSignal.timeout(5000),
  });
  if (!res.ok) throw new Error("Failed to clear logs");
  return res.json();
}

export async function fetchStatus() {
  try {
    const res = await fetch(`${BASE_URL}/status`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

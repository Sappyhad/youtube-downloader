const form = document.getElementById("form");
const statusEl = document.getElementById("status");
const bar = document.getElementById("bar");
const button = document.getElementById("go");
const LABELS = { queued: "Pobieranie informacji o filmie…", downloading: "Pobieranie", processing: "Łączenie / konwersja…" };

function setStatus(text, kind = "") {
  statusEl.textContent = text;
  statusEl.className = kind;
}

function setProgress(percent) {
  bar.style.display = percent == null ? "none" : "block";
  bar.firstElementChild.style.width = `${percent ?? 0}%`;
}

async function poll(jobId) {
  const res = await fetch(`/api/status/${jobId}`);
  const job = await res.json();
  if (job.status === "done") {
    setProgress(100);
    const details = job.resolution ? ` (${job.resolution})` : "";
    setStatus(`Gotowe: ${job.title}${details}`, "done");
    window.location.href = `/api/file/${jobId}`;
    button.disabled = false;
    return;
  }
  if (job.status === "error") {
    setProgress(null);
    setStatus(`Błąd: ${job.error}`, "error");
    button.disabled = false;
    return;
  }
  setProgress(job.percent ?? 0);
  const pct = job.status === "downloading" && job.percent != null ? ` ${job.percent}%` : "";
  setStatus(LABELS[job.status] + pct);
  setTimeout(() => poll(jobId), 700);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  setProgress(0);
  setStatus("Start…");
  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: document.getElementById("url").value,
        format: form.elements.format.value,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || res.statusText);
    poll(data.job_id);
  } catch (err) {
    setProgress(null);
    setStatus(`Błąd: ${err.message}`, "error");
    button.disabled = false;
  }
});

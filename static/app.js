const form = document.getElementById("upload-form");
const input = document.getElementById("video-input");
const fileLabel = document.getElementById("file-label");
const button = document.getElementById("analyze-button");
const message = document.getElementById("message");
const canvas = document.getElementById("timeline-chart");
const ctx = canvas.getContext("2d");

input.addEventListener("change", () => {
  fileLabel.textContent = input.files.length ? input.files[0].name : "Choose a video file";
});

function setMessage(text, kind = "") {
  message.textContent = text;
  message.className = `message ${kind}`;
}
function setRisk(element, level) {
  element.textContent = level || "—";
  element.className = "";
  element.classList.add(level ? `risk-${level.toLowerCase()}` : "risk-neutral");
}
function formatDuration(seconds) {
  if (seconds == null) return "—";
  const total = Math.round(seconds);
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}
function updateMetrics(data) {
  document.getElementById("average-count").textContent = data.average_people_count ?? "—";
  document.getElementById("peak-count").textContent = data.peak_people_count ?? "—";
  document.getElementById("duration").textContent = formatDuration(data.duration_seconds);
  setRisk(document.getElementById("risk-level"), data.risk_level);
  document.getElementById("analysis-notice").textContent = data.notice || "";
  drawChart(data.timeline || []);
}
function drawChart(points) {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const w = rect.width, h = rect.height;
  ctx.clearRect(0, 0, w, h);
  if (!points.length) {
    ctx.fillStyle = "#8794a8"; ctx.font = "12px DM Sans"; ctx.textAlign = "center";
    ctx.fillText("No timeline data yet", w / 2, h / 2); return;
  }
  const pad = {l: 38, r: 15, t: 16, b: 29};
  const cw = w-pad.l-pad.r, ch = h-pad.t-pad.b;
  const max = Math.max(5, ...points.map(p => p.people_count));
  ctx.font = "10px DM Sans"; ctx.textAlign = "right"; ctx.fillStyle = "#8b98aa";
  for (let i=0;i<=4;i++) {
    const value = Math.round(max*i/4), y = pad.t+ch-(ch*i/4);
    ctx.strokeStyle = "#edf1f6"; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(w-pad.r,y); ctx.stroke();
    ctx.fillText(value, pad.l-9, y+3);
  }
  const xAt = i => pad.l + (points.length === 1 ? cw/2 : i*cw/(points.length-1));
  const yAt = v => pad.t+ch-(v/max)*ch;
  ctx.beginPath();
  points.forEach((p,i)=>{const x=xAt(i),y=yAt(p.people_count);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});
  ctx.strokeStyle="#315be8";ctx.lineWidth=2.5;ctx.lineJoin="round";ctx.stroke();
  const lastX=xAt(points.length-1), lastY=yAt(points[points.length-1].people_count);
  ctx.lineTo(lastX,pad.t+ch);ctx.lineTo(xAt(0),pad.t+ch);ctx.closePath();
  ctx.fillStyle="rgba(49,91,232,.08)";ctx.fill();
  ctx.fillStyle="#8794a8";ctx.textAlign="center";
  const first=points[0].time_seconds, last=points[points.length-1].time_seconds;
  ctx.fillText(`${first}s`,pad.l,h-8);ctx.fillText(`${last}s`,w-pad.r,h-8);
}
function renderHistory(rows) {
  const body = document.getElementById("history-body");
  if (!rows.length) { body.innerHTML='<tr><td colspan="5" class="empty">No analyses yet.</td></tr>'; return; }
  body.replaceChildren();
  rows.forEach(row => {
    const tr=document.createElement("tr");
    const values=[row.filename,row.created_at.replace("T"," ").replace("+00:00",""),row.average_people_count,row.peak_people_count];
    values.forEach(value=>{const td=document.createElement("td");td.textContent=value;tr.appendChild(td);});
    const td=document.createElement("td"),tag=document.createElement("span");
    tag.className=`risk-tag tag-${row.risk_level.toLowerCase()}`;tag.textContent=row.risk_level;
    td.appendChild(tag);tr.appendChild(td);body.appendChild(tr);
  });
}
async function loadHistory() {
  try { const response=await fetch("/api/history"); if(!response.ok)throw new Error(); renderHistory(await response.json()); }
  catch { setMessage("Could not load monitoring history.","error"); }
}
form.addEventListener("submit", async event => {
  event.preventDefault();
  if (!input.files.length) { setMessage("Choose a video before analysing.","error"); return; }
  const data=new FormData();data.append("video",input.files[0]);
  button.disabled=true;button.textContent="Analysing…";setMessage("Processing video. Longer videos may take more time.");
  try {
    const response=await fetch("/api/analyze",{method:"POST",body:data});
    const result=await response.json();
    if(!response.ok)throw new Error(result.error||"Analysis failed.");
    updateMetrics(result);await loadHistory();setMessage("Analysis completed and saved to history.","success");
  } catch(error) { setMessage(error.message||"Unable to analyse this video.","error"); }
  finally {button.disabled=false;button.innerHTML='Analyse video <span>→</span>';}
});
document.getElementById("refresh-history").addEventListener("click",loadHistory);
window.addEventListener("resize",()=>drawChart([]));
loadHistory();drawChart([]);

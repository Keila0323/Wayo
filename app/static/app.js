// ── City options per country ─────────────────────────
const CITIES = {
  "Dominican Republic": ["Santo Domingo", "Punta Cana", "Santiago", "Puerto Plata", "Samaná", "La Romana"],
  "Puerto Rico":        ["San Juan", "Ponce", "Rincón", "Vieques", "Culebra"],
  "Colombia":           ["Cartagena", "Medellín", "Bogotá", "Santa Marta", "Cali"],
  "Mexico":             ["Mexico City", "Cancún", "Tulum", "Oaxaca", "Puerto Vallarta", "Playa del Carmen"]
};

// ── Populate cities when country changes ─────────────
document.getElementById("destination").addEventListener("change", function () {
  const citySelect = document.getElementById("city");
  const cities = CITIES[this.value] || [];
  citySelect.innerHTML = cities.length
    ? cities.map(c => `<option value="${c}">${c}</option>`).join("")
    : `<option value="">Select country first</option>`;
});

// ── Set min date to today ─────────────────────────────
const today = new Date().toISOString().split("T")[0];
document.getElementById("check_in").min = today;
document.getElementById("check_out").min = today;

document.getElementById("check_in").addEventListener("change", function () {
  document.getElementById("check_out").min = this.value;
});

// ── Vibe chip toggle ──────────────────────────────────
document.querySelectorAll(".vibe-chip").forEach(chip => {
  chip.addEventListener("click", () => chip.classList.toggle("active"));
});

// ── Form submission ───────────────────────────────────
document.getElementById("plannerForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const vibes = [...document.querySelectorAll(".vibe-chip.active")]
    .map(c => c.dataset.vibe);

  const payload = {
    destination:   document.getElementById("destination").value,
    city:          document.getElementById("city").value,
    check_in:      document.getElementById("check_in").value,
    check_out:     document.getElementById("check_out").value,
    group_type:    document.getElementById("group_type").value,
    budget:        document.getElementById("budget").value,
    accommodation: document.getElementById("accommodation").value,
    vibes
  };

  // Validate
  if (!payload.destination || !payload.city || !payload.check_in || !payload.check_out || !payload.group_type || !payload.budget) {
    alert("Please fill in all required fields.");
    return;
  }

  if (payload.check_in >= payload.check_out) {
    alert("Check-out date must be after check-in date.");
    return;
  }

  // Show loading
  const btn = document.getElementById("planBtn");
  btn.disabled = true;
  btn.textContent = "Building your trip...";
  document.getElementById("loading").classList.add("active");
  document.getElementById("results").classList.remove("active");
  document.getElementById("results").innerHTML = "";

  // Scroll to loading
  document.getElementById("loading").scrollIntoView({ behavior: "smooth", block: "center" });

  try {
    const resp = await fetch("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await resp.json();
    renderResults(data.itinerary, data.weather, payload);

  } catch (err) {
    alert("Something went wrong. Please try again.");
    console.error(err);
  } finally {
    document.getElementById("loading").classList.remove("active");
    btn.disabled = false;
    btn.textContent = "Build My Itinerary ✦";
  }
});

// ── Render results ────────────────────────────────────
function renderResults(itinerary, weather, payload) {
  const el = document.getElementById("results");

  const weatherMap = {};
  (weather || []).forEach(w => { weatherMap[w.date] = w; });

  // Transport banner
  const transport = itinerary.transport || {};
  const transportHTML = transport.options ? `
    <div class="transport-banner">
      <h3>🚗 Getting Around ${payload.city}</h3>
      <div class="transport-options">
        ${transport.options.map(o => `<span class="transport-tag">${o}</span>`).join("")}
      </div>
      <p class="transport-tip">💡 ${transport.tip}</p>
    </div>
  ` : "";

  // Day cards
  const daysHTML = (itinerary.days || []).map((day, i) => {
    const w = weather && weather[i] ? weather[i] : null;
    const weatherNote = w ? `${w.icon} ${w.conditions} · ${w.temp}°F` : (day.weather_note || "");

    return `
      <div class="day-card">
        <div class="day-header">
          <h3>${day.day}${day.date ? ` — ${day.date}` : ""}</h3>
          ${weatherNote ? `<span class="weather-badge">${weatherNote}</span>` : ""}
        </div>
        <div class="day-body">
          ${renderSlot("morning",   "🌅 Morning",   day.morning)}
          ${renderSlot("afternoon", "☀️ Afternoon", day.afternoon)}
          ${renderSlot("evening",   "🌙 Evening",   day.evening)}
        </div>
      </div>
    `;
  }).join("");

  // Tips
  const tipsHTML = itinerary.tips && itinerary.tips.length ? `
    <div class="tips-card">
      <h3>✦ Local Tips for ${payload.city}</h3>
      <ul class="tips-list">
        ${itinerary.tips.map(t => `<li>${t}</li>`).join("")}
      </ul>
    </div>
  ` : "";

  el.innerHTML = `
    <div class="results-header">
      <h2>Your ${payload.city} Itinerary</h2>
      <p>${payload.group_type} · ${payload.budget} · ${payload.check_in} → ${payload.check_out}</p>
    </div>
    ${transportHTML}
    ${daysHTML}
    ${tipsHTML}
  `;

  el.classList.add("active");
  el.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderSlot(className, label, slot) {
  if (!slot) return "";
  return `
    <div class="time-slot ${className}">
      <div class="time-label">
        <span class="time-dot"></span>
        ${label}
      </div>
      <div class="slot-content">
        <div class="slot-title">${slot.title || ""}</div>
        <div class="slot-desc">${slot.description || ""}</div>
        ${slot.transport ? `<span class="slot-transport">🚗 ${slot.transport}</span>` : ""}
      </div>
    </div>
  `;
}

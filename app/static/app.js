// ── City options per country ─────────────────────────
const CITIES = {
  "Dominican Republic": ["Santo Domingo", "Punta Cana", "Santiago", "Puerto Plata", "Samaná", "La Romana"],
  "Puerto Rico":        ["San Juan", "Ponce", "Rincón", "Vieques", "Culebra"],
  "Colombia":           ["Cartagena", "Medellín", "Bogotá", "Santa Marta", "Cali"],
  "Mexico":             ["Mexico City", "Cancún", "Tulum", "Oaxaca", "Puerto Vallarta", "Playa del Carmen"]
};

const CATEGORY_CONFIG = {
  gastronomy: {
    label: "Gastronomy",
    icon: "🍽️",
    subcategories: [
      { key: "food",        label: "Food",        icon: "🌮" },
      { key: "drinks",      label: "Drinks",      icon: "🥤" },
      { key: "bars",        label: "Bars",        icon: "🍹" },
      { key: "restaurants", label: "Restaurants", icon: "🍴" },
    ]
  },
  activities: {
    label: "Activities & Destinations",
    icon: "🌴",
    subcategories: [
      { key: "activities",  label: "Activities",  icon: "🧗" },
      { key: "beaches",     label: "Beaches",     icon: "🏖️" },
      { key: "landmarks",   label: "Landmarks",   icon: "🏛️" },
      { key: "experiences", label: "Experiences", icon: "✨" },
    ]
  }
};

let currentData = null;
let activeCategory = "gastronomy";
let activeSubcategory = "food";

// ── Populate cities ───────────────────────────────────
document.getElementById("destination").addEventListener("change", function () {
  const citySelect = document.getElementById("city");
  const cities = CITIES[this.value] || [];
  citySelect.innerHTML = cities.length
    ? cities.map(c => `<option value="${c}">${c}</option>`).join("")
    : `<option value="">Select country first</option>`;
});

// ── Set min date ──────────────────────────────────────
const today = new Date().toISOString().split("T")[0];
document.getElementById("check_in").min = today;
document.getElementById("check_out").min = today;
document.getElementById("check_in").addEventListener("change", function () {
  document.getElementById("check_out").min = this.value;
});

// ── Vibe chips ────────────────────────────────────────
document.querySelectorAll(".vibe-chip").forEach(chip => {
  chip.addEventListener("click", () => chip.classList.toggle("active"));
});

// ── Form submit ───────────────────────────────────────
document.getElementById("plannerForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const vibes = [...document.querySelectorAll(".vibe-chip.active")].map(c => c.dataset.vibe);
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

  if (!payload.destination || !payload.city || !payload.check_in || !payload.check_out || !payload.group_type || !payload.budget) {
    alert("Please fill in all required fields.");
    return;
  }
  if (payload.check_in >= payload.check_out) {
    alert("Check-out date must be after check-in date.");
    return;
  }

  const btn = document.getElementById("planBtn");
  btn.disabled = true;
  btn.textContent = "Finding your spots...";
  document.getElementById("loading").classList.add("active");
  document.getElementById("results").classList.remove("active");
  document.getElementById("results").innerHTML = "";
  document.getElementById("loading").scrollIntoView({ behavior: "smooth", block: "center" });

  try {
    const resp = await fetch("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    currentData = data.itinerary;
    activeCategory = "gastronomy";
    activeSubcategory = "food";
    renderResults(currentData, payload);
  } catch (err) {
    alert("Something went wrong. Please try again.");
  } finally {
    document.getElementById("loading").classList.remove("active");
    btn.disabled = false;
    btn.textContent = "Explore This Destination ✦";
  }
});

// ── Render results ────────────────────────────────────
function renderResults(data, payload) {
  const el = document.getElementById("results");

  // Weather strip
  const weatherHTML = (data.weather || []).length ? `
    <div class="weather-strip">
      ${(data.weather || []).map(w => `
        <div class="weather-day">
          <span class="w-icon">${w.icon}</span>
          <span class="w-date">${w.day.split(",")[0]}</span>
          <span class="w-temp">${w.temp}°F</span>
        </div>
      `).join("")}
    </div>
  ` : "";

  // Transport banner
  const t = data.transport || {};
  const transportHTML = t.options ? `
    <div class="transport-banner">
      <h3>🚗 Getting Around ${data.city || payload.city}</h3>
      <div class="transport-options">
        ${t.options.map(o => `<span class="transport-tag">${o}</span>`).join("")}
      </div>
      <p class="transport-tip">💡 ${t.tip}</p>
    </div>
  ` : "";

  el.innerHTML = `
    <div class="results-header">
      <h2>${data.city || payload.city}</h2>
      <p>${payload.group_type} · ${payload.budget} · ${payload.check_in} → ${payload.check_out}</p>
    </div>

    ${weatherHTML}

    <div class="category-tabs">
      ${Object.entries(CATEGORY_CONFIG).map(([key, cat]) => `
        <button class="cat-tab ${key === activeCategory ? 'active' : ''}" data-category="${key}">
          ${cat.icon} ${cat.label}
        </button>
      `).join("")}
    </div>

    <div class="subcategory-tabs" id="subcategoryTabs"></div>
    <div class="recs-grid" id="recsGrid"></div>

    ${transportHTML}

    ${data.tips && data.tips.length ? `
      <div class="tips-card">
        <h3>✦ Local Tips for ${data.city || payload.city}</h3>
        <ul class="tips-list">
          ${data.tips.map(t => `<li>${t}</li>`).join("")}
        </ul>
      </div>
    ` : ""}
  `;

  el.classList.add("active");

  // Bind category tab clicks
  el.querySelectorAll(".cat-tab").forEach(btn => {
    btn.addEventListener("click", function () {
      activeCategory = this.dataset.category;
      activeSubcategory = CATEGORY_CONFIG[activeCategory].subcategories[0].key;
      el.querySelectorAll(".cat-tab").forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      renderSubcategories();
      renderCards();
    });
  });

  renderSubcategories();
  renderCards();
  el.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderSubcategories() {
  const container = document.getElementById("subcategoryTabs");
  const subs = CATEGORY_CONFIG[activeCategory].subcategories;
  container.innerHTML = subs.map(s => `
    <button class="sub-tab ${s.key === activeSubcategory ? 'active' : ''}" data-sub="${s.key}">
      ${s.icon} ${s.label}
    </button>
  `).join("");

  container.querySelectorAll(".sub-tab").forEach(btn => {
    btn.addEventListener("click", function () {
      activeSubcategory = this.dataset.sub;
      container.querySelectorAll(".sub-tab").forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      renderCards();
    });
  });
}

function renderCards() {
  const container = document.getElementById("recsGrid");
  const items = (currentData[activeCategory] || {})[activeSubcategory] || [];

  if (!items.length) {
    container.innerHTML = `<div class="carousel-wrapper"><div class="no-recs">No recommendations found for this category.</div></div>`;
    return;
  }

  const cardsHTML = items.map(item => `
    <div class="rec-card">
      <div class="rec-header">
        <div>
          <div class="rec-name">${item.name}</div>
          <div class="rec-sub">${item.subcategory || ""}</div>
        </div>
        <span class="rec-cost">${item.cost || ""}</span>
      </div>
      <p class="rec-desc">${item.description || ""}</p>
      <div class="rec-footer">
        <span class="rec-vibe">✦ ${item.vibe || ""}</span>
        ${item.transport ? `<span class="rec-transport">🚗 ${item.transport}</span>` : ""}
      </div>
    </div>
  `).join("");

  container.innerHTML = `
    <div class="carousel-wrapper">
      <button class="carousel-arrow carousel-arrow--left" aria-label="Scroll left">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>
      <div class="carousel-track" id="carouselTrack">
        ${cardsHTML}
      </div>
      <button class="carousel-arrow carousel-arrow--right" aria-label="Scroll right">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </button>
    </div>
  `;

  // Arrow scroll logic
  const track = container.querySelector("#carouselTrack");
  const leftBtn = container.querySelector(".carousel-arrow--left");
  const rightBtn = container.querySelector(".carousel-arrow--right");

  const SCROLL_AMOUNT = 320;

  function updateArrows() {
    const atStart = track.scrollLeft <= 4;
    const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    leftBtn.classList.toggle("hidden", atStart);
    rightBtn.classList.toggle("hidden", atEnd);
  }

  leftBtn.addEventListener("click", () => {
    track.scrollBy({ left: -SCROLL_AMOUNT, behavior: "smooth" });
  });

  rightBtn.addEventListener("click", () => {
    track.scrollBy({ left: SCROLL_AMOUNT, behavior: "smooth" });
  });

  track.addEventListener("scroll", updateArrows, { passive: true });
  updateArrows();

  // Touch/swipe support
  let touchStartX = 0;
  track.addEventListener("touchstart", e => {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });
  track.addEventListener("touchend", e => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) {
      track.scrollBy({ left: diff > 0 ? SCROLL_AMOUNT : -SCROLL_AMOUNT, behavior: "smooth" });
    }
  }, { passive: true });
}

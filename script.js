// Initialize AOS and Swiper, handle dark mode, smooth scroll, filters, countdown, ripple, chat, etc.

document.addEventListener("DOMContentLoaded", function () {
  const html = document.documentElement;

  // Page loader
  setTimeout(() => {
    document.body.classList.remove("page-loading");
    const loader = document.getElementById("page-loader");
    if (loader) {
      loader.classList.add("hidden");
      setTimeout(() => loader.remove(), 400);
    }
  }, 600);

  // Dark mode toggle (persist to localStorage)
  const THEME_KEY = "cefg-theme";
  const current = localStorage.getItem(THEME_KEY);
  if (current === "dark") {
    html.classList.remove("light");
  } else if (current === "light") {
    html.classList.add("light");
  }

  const darkToggle = document.getElementById("darkModeToggle");
  if (darkToggle) {
    darkToggle.addEventListener("click", () => {
      const isLight = html.classList.toggle("light");
      localStorage.setItem(THEME_KEY, isLight ? "light" : "dark");
    });
  }

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const targetId = link.getAttribute("href").substring(1);
      const el = document.getElementById(targetId);
      if (el) {
        e.preventDefault();
        const y = el.getBoundingClientRect().top + window.pageYOffset - 80;
        window.scrollTo({ top: y, behavior: "smooth" });
      }
    });
  });

  // AOS scroll animations
  if (window.AOS) {
    AOS.init({
      duration: 700,
      easing: "ease-out-quart",
      once: false,
      offset: 80
    });
  }

  // Swiper Sliders
  if (window.Swiper) {
    const heroContainer = document.querySelector(".hero-swiper");
    if (heroContainer) {
      new Swiper(heroContainer, {
        loop: true,
        autoplay: {
          delay: 3500,
          disableOnInteraction: false
        },
        effect: "slide",
        pagination: {
          el: ".hero-swiper .swiper-pagination",
          clickable: true
        },
        speed: 800
      });
    }

    const galleryContainer = document.querySelector(".gallery-swiper");
    if (galleryContainer) {
      new Swiper(galleryContainer, {
        loop: true,
        slidesPerView: 1,
        spaceBetween: 16,
        navigation: {
          nextEl: ".gallery-swiper .swiper-button-next",
          prevEl: ".gallery-swiper .swiper-button-prev"
        },
        pagination: {
          el: ".gallery-swiper .swiper-pagination",
          clickable: true
        },
        breakpoints: {
          768: { slidesPerView: 1.2 }
        }
      });
    }
  }

  // Event filters
  const filterButtons = document.querySelectorAll(".filter-btn");
  const eventCards = document.querySelectorAll(".events-grid .event-card");
  if (filterButtons.length && eventCards.length) {
    filterButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const filter = btn.dataset.filter;
        filterButtons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        eventCards.forEach((card) => {
          const type = card.dataset.type;
          if (filter === "all" || type === filter) {
            card.style.display = "";
            card.style.opacity = "1";
          } else {
            card.style.opacity = "0";
            setTimeout(() => {
              card.style.display = "none";
            }, 200);
          }
        });
      });
    });
  }

  // Team event toggle
  const teamCheckbox = document.getElementById("isTeamEvent");
  const teamFields = document.getElementById("teamFields");
  if (teamCheckbox && teamFields) {
    teamCheckbox.addEventListener("change", () => {
      teamFields.classList.toggle("hidden", !teamCheckbox.checked);
    });
  }

  // Countdown timer
  const countdownCard = document.querySelector(".countdown-card");
  if (countdownCard) {
    const dateStr = countdownCard.getAttribute("data-event-date");
    const targetDate = dateStr ? new Date(dateStr) : null;
    if (targetDate && !isNaN(targetDate)) {
      const spanDays = countdownCard.querySelector(".days");
      const spanHours = countdownCard.querySelector(".hours");
      const spanMinutes = countdownCard.querySelector(".minutes");
      const spanSeconds = countdownCard.querySelector(".seconds");
      const update = () => {
        const now = new Date();
        const diff = targetDate - now;
        if (diff <= 0) {
          spanDays.textContent = "00";
          spanHours.textContent = "00";
          spanMinutes.textContent = "00";
          spanSeconds.textContent = "00";
          return;
        }
        const s = Math.floor(diff / 1000);
        const d = Math.floor(s / 86400);
        const h = Math.floor((s % 86400) / 3600);
        const m = Math.floor((s % 3600) / 60);
        const sec = s % 60;
        spanDays.textContent = String(d).padStart(2, "0");
        spanHours.textContent = String(h).padStart(2, "0");
        spanMinutes.textContent = String(m).padStart(2, "0");
        spanSeconds.textContent = String(sec).padStart(2, "0");
      };
      update();
      setInterval(update, 1000);
    }
  }

  // Ripple effect (JS-powered)
  document.body.addEventListener("click", function (e) {
    const target = e.target.closest(".ripple");
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const circle = document.createElement("span");
    circle.classList.add("ripple-anim");
    circle.style.width = circle.style.height = size + "px";
    circle.style.left = e.clientX - rect.left - size / 2 + "px";
    circle.style.top = e.clientY - rect.top - size / 2 + "px";
    target.appendChild(circle);
    setTimeout(() => circle.remove(), 600);
  });

  // Chatbot
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatMessages = document.getElementById("chatMessages");

  if (chatForm && chatInput && chatMessages) {
    const addMessage = (text, from) => {
      const msg = document.createElement("div");
      msg.className = "msg " + from;
      msg.innerHTML = "<p>" + text + "</p>";
      chatMessages.appendChild(msg);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (!text) return;
      addMessage(text, "user");
      chatInput.value = "";
      try {
        const res = await fetch("/api/chatbot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        addMessage(data.reply || "I couldn't understand that, please try again.", "bot");
      } catch (err) {
        addMessage("Network error. Please try again.", "bot");
      }
    });
  }
});


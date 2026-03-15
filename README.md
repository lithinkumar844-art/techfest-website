# College Event Fest Guide

Modern multi-page Flask + MongoDB website for managing college tech fest events, with animations, sliders, dark mode, and dashboards for students and admins.

## Features

- Home page with hero image slider, countdown timer, featured events, and schedule section
- Events listing with animated cards, filters, and scroll animations
- Event details page with description, rules, and venue map (Google Maps Embed API)
- Registration form with team support and digital event pass with QR code
- Student dashboard to view registered events and achievement badges
- Admin dashboard to create/delete events and see participant list
- Leaderboard page with animated ranking cards
- Gallery page with image carousel and hover effects
- Help section with simple chatbot UI backed by a small FAQ API
- Dark mode toggle with smooth transition and persistence
- Page loader, ripple effects, hover and scroll reveal animations using CSS + AOS + Swiper

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, AOS, Swiper, QRious
- **Backend**: Python, Flask
- **Database**: MongoDB (via `pymongo`)
- **Maps**: Google Maps Embed API

## Project Structure

```text
college-fest-guide/
├── app.py
├── requirements.txt
├── README.md
├── database/
│   └── models.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── events.html
│   ├── event_detail.html
│   ├── register.html
│   ├── digital_pass.html
│   ├── dashboard.html
│   ├── admin.html
│   ├── leaderboard.html
│   ├── gallery.html
│   └── help.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
        └── (place your hero & gallery images here)
```

## Setup

1. **Install dependencies**

   ```bash
   cd college-fest-guide
   python -m venv venv
   venv\Scripts\activate  # on Windows
   pip install -r requirements.txt
   ```

2. **Configure MongoDB**

   - Start MongoDB locally (default URI `mongodb://localhost:27017/`).
   - Optionally set a custom URI and DB name in environment variables:

   ```bash
   set MONGO_URI=mongodb://localhost:27017/
   set MONGO_DB_NAME=college_fest_guide
   ```

3. **Configure Google Maps API key**

   - Create a Google Maps Embed API key.
   - Set it as an environment variable:

   ```bash
   set GOOGLE_MAPS_API_KEY=YOUR_REAL_KEY_HERE
   ```

4. **Run the app**

   ```bash
   set FLASK_APP=app.py
   python app.py
   ```

   The site will start on `http://127.0.0.1:5000/`.

## Login

- **Student**: open `/login` and enter your email (demo login).
- **Admin**: open `/login` and enter the admin password.
  - Local default: `admin123`
  - For deployment, set environment variable **`ADMIN_PASSWORD`**.

## Seed sample data (recommended)

This adds sample events + leaderboard participants so the UI looks full.

```bash
python scripts/seed_data.py
```

## Notes

- Place hero and gallery images in `static/images/` matching the names used in `style.css` (e.g., `hero-techfest.jpg`, `gallery1.jpg`, etc.), or change the CSS to use your own assets.
- This is a starter implementation; you can connect real authentication, richer scoring logic for the leaderboard, and a more advanced chatbot as needed.


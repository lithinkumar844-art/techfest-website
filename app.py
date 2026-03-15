import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from bson.objectid import ObjectId
from database.models import get_db, init_db


def login_required(role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not session.get("user"):
                return redirect(url_for("login", next=request.path))
            if role and session.get("role") != role:
                return redirect(url_for("login", next=request.path))
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def create_app():
    app = Flask(__name__)

    # Config from environment for deployment
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    app.config["MONGO_DB_NAME"] = os.getenv("MONGO_DB_NAME", "college_fest_guide")
    app.config["GOOGLE_MAPS_API_KEY"] = os.getenv(
        "GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY_HERE"
    )
    app.config["ADMIN_PASSWORD"] = os.getenv("ADMIN_PASSWORD", "admin123")

    # Initialize MongoDB client / database
    init_db(app)

    @app.context_processor
    def inject_now():
        return {
            "now": datetime.utcnow(),
            "session_user": session.get("user"),
            "session_role": session.get("role"),
        }

    @app.route("/login", methods=["GET", "POST"])
    def login():
        next_url = request.args.get("next") or url_for("home")
        error = None

        if request.method == "POST":
            role = request.form.get("role")
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""

            if role == "student":
                if not email:
                    error = "Please enter your email."
                else:
                    session["user"] = email
                    session["role"] = "student"
                    return redirect(next_url)
            elif role == "admin":
                if password != app.config["ADMIN_PASSWORD"]:
                    error = "Invalid admin password."
                else:
                    session["user"] = "admin"
                    session["role"] = "admin"
                    return redirect(url_for("admin_dashboard"))
            else:
                error = "Please select a role."

        return render_template("login.html", next_url=next_url, error=error)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    @app.route("/")
    def home():
        db = get_db()
        featured_events = list(db.events.find().sort("date", 1).limit(4))
        upcoming_event = db.events.find_one(sort=[("date", 1)])
        return render_template(
            "index.html",
            featured_events=featured_events,
            upcoming_event=upcoming_event,
        )

    @app.route("/events")
    def events():
        db = get_db()
        all_events = list(db.events.find().sort("date", 1))
        return render_template("events.html", events=all_events)

    @app.route("/events/<event_id>")
    def event_detail(event_id):
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return redirect(url_for("events"))
        return render_template("event_detail.html", event=event)

    @app.route("/register/<event_id>", methods=["GET", "POST"])
    def register(event_id):
        db = get_db()
        event = db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            return redirect(url_for("events"))

        if request.method == "POST":
            data = request.form.to_dict()
            data["event_id"] = ObjectId(event_id)
            data["event_name"] = event.get("name")
            data["event_date"] = event.get("date")
            data["created_at"] = datetime.utcnow()
            result = db.registrations.insert_one(data)
            registration_id = str(result.inserted_id)
            return render_template(
                "digital_pass.html",
                event=event,
                registration_id=registration_id,
            )

        return render_template("register.html", event=event)

    @app.route("/student/dashboard")
    @login_required(role="student")
    def student_dashboard():
        email = session.get("user")
        db = get_db()
        registrations = []
        if email:
            registrations = list(db.registrations.find({"email": email}))
        return render_template(
            "dashboard.html", registrations=registrations, email=email
        )

    @app.route("/admin")
    @login_required(role="admin")
    def admin_dashboard():
        db = get_db()
        events = list(db.events.find().sort("date", 1))
        participants = list(db.registrations.find().sort("created_at", -1))
        return render_template(
            "admin.html", events=events, participants=participants
        )

    @app.route("/admin/events/create", methods=["POST"])
    @login_required(role="admin")
    def admin_create_event():
        db = get_db()
        data = request.form.to_dict()
        data["created_at"] = datetime.utcnow()
        db.events.insert_one(data)
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/events/<event_id>/delete", methods=["POST"])
    @login_required(role="admin")
    def admin_delete_event(event_id):
        db = get_db()
        db.events.delete_one({"_id": ObjectId(event_id)})
        db.registrations.delete_many({"event_id": ObjectId(event_id)})
        return redirect(url_for("admin_dashboard"))

    @app.route("/leaderboard")
    def leaderboard():
        db = get_db()
        # Simple aggregation by score field, if present
        pipeline = [
            {"$match": {"score": {"$exists": True}}},
            {"$sort": {"score": -1}},
            {"$limit": 20},
        ]
        leaders = list(db.participants.aggregate(pipeline))
        return render_template("leaderboard.html", leaders=leaders)

    @app.route("/gallery")
    def gallery():
        return render_template("gallery.html")

    @app.route("/help")
    def help_page():
        return render_template("help.html")

    @app.route("/api/chatbot", methods=["POST"])
    def chatbot():
        """
        Simple rule-based chatbot for event FAQs.
        """
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").lower()
        response = "I'm not sure about that. Please contact your event coordinator."

        if "schedule" in message or "time" in message:
            response = "You can find the full schedule on the Schedule section of the home page or Events page."
        elif "register" in message:
            response = "To register, open the Events page, choose an event, and click the Register button."
        elif "venue" in message or "location" in message or "where" in message:
            response = "All venues are shown on the Event Details page with an embedded Google Map."
        elif "contact" in message or "help" in message:
            response = "For additional help, please reach out to your college tech fest coordinator."
        elif "login" in message or "password" in message:
            response = "Students can log in using email. Admin login uses the ADMIN_PASSWORD set on the server."
        elif "leaderboard" in message or "rank" in message:
            response = "Leaderboard shows top participants based on score. Results appear once scores are published."

        return jsonify({"reply": response})

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)


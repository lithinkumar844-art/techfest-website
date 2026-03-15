import os
from datetime import datetime, timedelta
from pymongo import MongoClient


def main():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGO_DB_NAME", "college_fest_guide")

    client = MongoClient(mongo_uri)
    db = client[db_name]

    # Clear existing sample collections (optional)
    db.events.delete_many({})
    db.registrations.delete_many({})
    db.participants.delete_many({})

    today = datetime.utcnow().date()
    sample_events = [
        {
            "name": "Campus Hackathon 24H",
            "type": "Hackathon",
            "date": str(today + timedelta(days=7)),
            "venue": "Innovation Lab",
            "venue_query": "Innovation Lab, College Campus",
            "short_description": "Build a prototype in 24 hours with your team.",
            "description": "A 24-hour hackathon focused on solving real campus problems with tech.",
            "rules": "Teams of 2-4\nBring your laptop\nInternet will be provided\nFinal demo is mandatory",
            "created_at": datetime.utcnow(),
        },
        {
            "name": "CodeSprint Arena",
            "type": "Coding Contest",
            "date": str(today + timedelta(days=10)),
            "venue": "Computer Lab A",
            "venue_query": "Computer Lab A, College Campus",
            "short_description": "Fast-paced coding rounds with increasing difficulty.",
            "description": "Solve algorithmic challenges under time pressure and climb the leaderboard.",
            "rules": "Individual event\nNo plagiarism\nMultiple languages allowed\nTop scorers win",
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Robotics Challenge: Line Follower",
            "type": "Robotics Challenge",
            "date": str(today + timedelta(days=14)),
            "venue": "Mechanical Block",
            "venue_query": "Mechanical Block, College Campus",
            "short_description": "Design a bot that follows the track fastest.",
            "description": "Compete with custom bots built for speed and control on a predefined track.",
            "rules": "Teams of 2-3\nBot size limits apply\nNo external control\nTime penalties for off-track",
            "created_at": datetime.utcnow(),
        },
        {
            "name": "Tech Quiz Showdown",
            "type": "Tech Quiz",
            "date": str(today + timedelta(days=5)),
            "venue": "Seminar Hall 2",
            "venue_query": "Seminar Hall 2, College Campus",
            "short_description": "MCQ + buzzer round on tech and current trends.",
            "description": "Test your knowledge in tech, AI, cybersecurity, and latest innovations.",
            "rules": "Teams of 2\nNo mobile phones\nDecision of judges is final",
            "created_at": datetime.utcnow(),
        },
    ]

    db.events.insert_many(sample_events)

    sample_participants = [
        {"name": "Aarav Kumar", "college": "Tech College A", "score": 980},
        {"name": "Meera Iyer", "college": "Tech College B", "score": 930},
        {"name": "Rohan Das", "college": "Tech College C", "score": 890},
        {"name": "Ananya Singh", "college": "Tech College A", "score": 860},
        {"name": "Sana Ali", "college": "Tech College D", "score": 820},
    ]

    for p in sample_participants:
        p["created_at"] = datetime.utcnow()

    db.participants.insert_many(sample_participants)

    print(f"Seed complete. Inserted {len(sample_events)} events and {len(sample_participants)} participants into '{db_name}'.")


if __name__ == "__main__":
    main()


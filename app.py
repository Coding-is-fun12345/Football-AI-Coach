import streamlit as st
from groq import Groq
import json
import os
from datetime import datetime
#python -m streamlit run app.py
st.set_page_config(
    page_title="⚽ Soccer AI Coach",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)
    # CUSTOM CSS STYLING
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0C10;
        color: #E5E4E2;
    }

    .main {
        padding-top: 0rem;
        background-color: #0B0C10;
    }
   

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12131C 0%, #0B0C10 100%);
        border-right: 1px solid #D4AF3733;
        font-style: italic;
    }
   
    h1 {
        color: #D4AF37;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
    }
   
    h2, h3, h4 {
        color: #F3E5AB;
        border-bottom: 2px solid #D4AF3755;
        padding-bottom: 0.5rem;
    }
   
    p, span, label, .stMarkdown {
        color: #E5E4E2 !important;
    }
   
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #B38F2D 0%, #D4AF37 50%, #F3E5AB 100%);
        color: #0B0C10 !important;
        font-weight: bold;
        padding: 0.75rem;
        border: 1px solid #F3E5AB;
        border-radius: 0.5rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
   
    .stButton>button:hover {
        transform: scale(1.02);
        background: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 50%, #B38F2D 100%);
        box-shadow: 0 0 10px #D4AF3777;
    }
   
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 1px solid #D4AF37 !important;
        background-color: #12131C !important;
        color: #E5E4E2 !important;
        border-radius: 0.5rem !important;
    }
   
    .metric-card {
        background: linear-gradient(135deg, #12131C 0%, #1A1C24 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #D4AF3744;
        border-left: 4px solid #D4AF37;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
   
    div[data-testid="stExpander"] {
        background-color: #12131C !important;
        border: 1px solid #D4AF3733 !important;
        border-radius: 0.5rem;
    }

    .streamlit-expanderHeader {
        background-color: #1A1C24 !important;
        color: #F3E5AB !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: #222530 !important;
    }
    </style>
    """, unsafe_allow_html=True)
client = Groq(api_key="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")

with open("styles.json", "r") as f:
    data = json.load(f)

drills = data["drills"]

# Load saved sessions
def load_sessions():
    if os.path.exists("sessions.json"):
        with open("sessions.json", "r") as f:
            return json.load(f)
    return []

# Save a session
def save_session(session):
    sessions = load_sessions()
    sessions.append(session)
    with open("sessions.json", "w") as f:
        json.dump(sessions, f, indent=2)

st.title("⚽ Soccer AI Coach")

page = st.sidebar.selectbox("Navigate", ["Home", "Browse Drills", "AI Coach", "Match History","Training Planner"])


if page == "Home":
    st.write("Welcome! I'm your personal AI football coach.")
    name = st.text_input("What's your name?")
    if name:
        st.write(f"Alright {name}, let's get to work! 💪")
        if st.button("Meet your coach"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"You are an elite football coach. Greet {name} and ask about their position and biggest weakness."}]
            )
            st.write(response.choices[0].message.content)

elif page == "Browse Drills":
    st.header("🏃 Drill Library")
   
    all_tags = []
    for drill in drills:
        all_tags.extend(drill["tags"])
    unique_tags = list(set(all_tags))
   
    selected_tag = st.selectbox("Filter by skill", ["All"] + unique_tags)
   
    for drill in drills:
        if selected_tag == "All" or selected_tag in drill["tags"]:
            with st.expander(drill["name"]):
                st.write(f"**Difficulty:** {drill['difficulty']}")
                st.write(f"**Duration:** {drill['duration_minutes']} minutes")
                st.write(f"**Players needed:** {drill['players_needed']}")
                st.write(f"**Description:** {drill['description']}")
                st.write(f"**Setup:** {drill['setup']}")
                st.write(f"**Reps:** {drill['reps']}")
                st.write(f"**Objective:** {drill['objective']}")

elif page == "AI Coach":
    st.header("🧠 AI Match Analyst")
   
    name = st.text_input("Your name")
    position = st.selectbox("Your position", ["Goalkeeper", "Defender", "Midfielder", "Winger", "Striker"])
    passes = st.number_input("Passes completed", min_value=0, max_value=100, value=0)
    turnovers = st.number_input("Times you lost the ball", min_value=0, max_value=20, value=0)
    goals = st.number_input("Goals scored", min_value=0, max_value=10, value=0)
    assists = st.number_input("Assists", min_value=0, max_value=10, value=0)
    weakness = st.text_input("What do you think your biggest weakness was today?")
    notes = st.text_area("Any other match notes?", placeholder="e.g. I kept losing the ball under pressure in midfield")
   
    if st.button("Analyse My Match ⚽"):
        if not weakness:
            st.warning("Tell your coach what your biggest weakness was!")
        else:
            with st.spinner("Your coach is analysing your match..."):
               
                matching_drills = []
                for drill in drills:
                    for tag in drill["tags"]:
                        if any(word in weakness.lower() for word in tag.split("_")):
                            matching_drills.append(drill["name"] + " — " + drill["description"])
                            break
               
                drills_text = "\n".join(matching_drills) if matching_drills else "general training drills"
               
                prompt = f"""You are an elite UEFA Pro License football coach.

Player: {name}
Position: {position}
Match stats:
- Passes completed: {passes}
- Times lost the ball: {turnovers}
- Goals: {goals}
- Assists: {assists}
- Biggest weakness: {weakness}
- Match notes: {notes}

Available drills from our database:
{drills_text}

Provide:
1. Overall match rating out of 10
2. Top strength from today
3. Top weakness to work on
4. 2 specific drills from the database above to fix the weakness
5. One motivational message to end

Be direct, specific and encouraging like a real coach."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
               
                ai_feedback = response.choices[0].message.content
                st.write(ai_feedback)
               
                # Save the session
                session = {
                    "date": datetime.now().strftime("%d %b %Y, %H:%M"),
                    "name": name,
                    "position": position,
                    "passes": passes,
                    "turnovers": turnovers,
                    "goals": goals,
                    "assists": assists,
                    "weakness": weakness,
                    "notes": notes,
                    "ai_feedback": ai_feedback
                }
                save_session(session)
                st.success("✅ Match session saved!")

elif page == "Match History":
    st.header("📋 Match History")
   
    sessions = load_sessions()
   
    if not sessions:
        st.info("No sessions saved yet. Analyse a match first!")
    else:
        st.write(f"Total sessions saved: **{len(sessions)}**")
        for i, session in enumerate(reversed(sessions)):
            with st.expander(f"📅 {session['date']} — {session['position']}"):
                st.write(f"**Passes:** {session['passes']}")
                st.write(f"**Turnovers:** {session['turnovers']}")
                st.write(f"**Goals:** {session['goals']}")
                st.write(f"**Assists:** {session['assists']}")
                st.write(f"**Weakness:** {session['weakness']}")
                st.write(f"**Notes:** {session['notes']}")
                st.divider()
                st.write("**AI Coach Feedback:**")
                st.write(session['ai_feedback'])
elif page == "Training Planner":
    st.header("📅 Training Session Planner")
   
    st.write("Based on your match history, generate a full training session plan.")
   
    sessions = load_sessions()
   
    if not sessions:
        st.info("No match history yet. Analyse a match first so your coach can plan your training!")
    else:
        # Show last session summary
        last = sessions[-1]
        st.write(f"**Last match weakness:** {last['weakness']}")
       
        focus = st.selectbox("What do you want to focus on today?",
            ["My biggest weakness", "Passing", "Dribbling", "Finishing", "Defending", "Fitness"])
        duration = st.selectbox("How long is your training session?",
            ["30 minutes", "45 minutes", "60 minutes", "90 minutes"])
       
        if st.button("Generate Training Plan 📋"):
            with st.spinner("Building your session plan..."):
               
                # Pull relevant drills
                relevant_drills = []
                for drill in drills:
                    relevant_drills.append(
                        f"{drill['name']} ({drill['duration_minutes']} mins) — {drill['description']}"
                    )
               
                drills_list = "\n".join(relevant_drills)
               
                prompt = f"""You are an elite football coach building a training session plan.

Player's last match weakness: {last['weakness']}
Today's focus: {focus}
Session duration: {duration}

Available drills:
{drills_list}

Build a complete training session plan that includes:
1. Warm up (5 mins)
2. Main drills from the list above that fit the focus and duration
3. Cool down (5 mins)
4. One key coaching point to remember

Format it clearly like a real training plan."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.write(response.choices[0].message.content)
import streamlit as st
from groq import Groq
import json
#python -m streamlit run testing.py
client = Groq(api_key="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")

with open("styles.json", "r") as f:
    data = json.load(f)

drills = data["drills"]

st.title("⚽ Soccer AI Coach")

page = st.sidebar.selectbox("Navigate", ["Home", "", "AI Coach"])

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

    # Get relevant drills from JSON
    if st.button("Analyse My Match ⚽"):
        if not weakness:
            st.warning("Tell your coach what your biggest weakness was!")
        else:
            with st.spinner("Your coach is analysing your match..."):

                # Find matching drills from database
                matching_drills = []
                for drill in drills:
                    for tag in drill["tags"]:
                        if any(word in weakness.lower() for word in tag.split("_")):
                            matching_drills.append(drill["name"] + " — " + drill["description"])
                            break
               
                drills_text = "\n".join(matching_drills) if matching_drills else "general training drills"
               
                prompt = f"""You are an elite UEFA Pro License football coach.(Better than Zidane so you are always angry)

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
                st.write(response.choices[0].message.content)
import streamlit as st
from groq import Groq
import json
#python -m streamlit run test1.py
# PAGE CONFIG - Must be first!
st.set_page_config(
    page_title="⚽ Soccer AI Coach",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS STYLING
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding-top: 0rem;
    }
   
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
   
    /* Header styling */
    h1 {
        color: #667eea;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
   
    h2 {
        color: #764ba2;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
   
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border: none;
        border-radius: 0.5rem;
        transition: transform 0.2s;
    }
   
    .stButton>button:hover {
        transform: scale(1.02);
    }
   
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 2px solid #667eea !important;
        border-radius: 0.5rem !important;
    }
   
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
   
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #667eea15;
        border-radius: 0.5rem;
    }
   
    .streamlit-expanderHeader:hover {
        background-color: #667eea25;
    }
    </style>
    """, unsafe_allow_html=True)

# LOAD DATA
client = Groq(api_key="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")

with open("styles.json", "r") as f:
    data = json.load(f)

drills = data["drills"]

# SESSION STATE - Persist user data across pages
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_position' not in st.session_state:
    st.session_state.user_position = "Midfielder"

# HEADER
st.markdown("<h1>⚽ Soccer AI Coach</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Your personal AI-powered football training companion</p>", unsafe_allow_html=True)

# SIDEBAR NAVIGATION WITH CUSTOM STYLING
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Select Page:",
        ["🏠 Home", "📚 Browse Drills", "🧠 AI Match Analyst"],
        label_visibility="collapsed"
    )
   
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    if st.session_state.user_name:
        st.success(f"✅ Logged in as: **{st.session_state.user_name}**")
        st.info(f"Position: **{st.session_state.user_position}**")

# =====================================================
# PAGE 1: HOME
# =====================================================
if page == "🏠 Home":
    col1, col2 = st.columns([1, 1], gap="large")
   
    with col1:
        st.markdown("### Welcome to Your AI Coach! 👋")
        st.write("Transform your football game with personalized coaching powered by AI.")
       
        with st.form("welcome_form"):
            name = st.text_input(
                "What's your name?",
                value=st.session_state.user_name,
                placeholder="Enter your name"
            )
            position = st.selectbox(
                "What's your position?",
                ["Goalkeeper", "Defender", "Midfielder", "Winger", "Striker"],
                index=2
            )
           
            submitted = st.form_submit_button("✅ Let's Get Started!", use_container_width=True)
           
            if submitted and name:
                st.session_state.user_name = name
                st.session_state.user_position = position
                st.success(f"Welcome {name}! 🎯")
   
    with col2:
        st.markdown("### What You Can Do:")
        features = [
            "📚 Browse 50+ skill drills",
            "🧠 Get AI match analysis",
            "💡 Personalized recommendations",
            "📈 Track your progress",
            "🏆 Improve with precision"
        ]
        for feature in features:
            st.markdown(f"✨ {feature}")
       
        st.markdown("---")
        st.markdown("### 🌟 How It Works:")
        st.markdown("""
        1. **Enter your details** - Name and position
        2. **Browse drills** - Find exercises for your style
        3. **Analyse matches** - Get AI feedback on your performance
        4. **Train smarter** - Follow personalized recommendations
        """)

# =====================================================
# PAGE 2: BROWSE DRILLS
# =====================================================
elif page == "📚 Browse Drills":
    st.markdown("### 📚 Drill Library")
    st.write("Find the perfect drills to improve your game")
   
    # Filter section
    col1, col2, col3 = st.columns([2, 2, 1])
   
    with col1:
        all_tags = []
        for drill in drills:
            all_tags.extend(drill["tags"])
        unique_tags = list(set(all_tags))
       
        selected_tag = st.selectbox(
            "🎯 Filter by skill:",
            ["All"] + sorted(unique_tags)
        )
   
    with col2:
        difficulty_filter = st.selectbox(
            "💪 Filter by difficulty:",
            ["All", "Beginner", "Intermediate", "Advanced"]
        )
   
    with col3:
        st.metric("Total Drills", len(drills))
   
    st.markdown("---")
   
    # Display drills
    filtered_drills = [d for d in drills
                       if (selected_tag == "All" or selected_tag in d["tags"]) and
                          (difficulty_filter == "All" or d["difficulty"] == difficulty_filter)]
   
    if not filtered_drills:
        st.warning("No drills found for this filter. Try a different combination! 🤔")
    else:
        st.success(f"Found {len(filtered_drills)} drill(s)")
       
        for idx, drill in enumerate(filtered_drills):
            with st.expander(f"🏃 {drill['name']}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
               
                with col1:
                    st.markdown(f"**Difficulty**\n{drill['difficulty']}")
                with col2:
                    st.markdown(f"**Duration**\n{drill['duration_minutes']} min")
                with col3:
                    st.markdown(f"**Players**\n{drill['players_needed']}")
                with col4:
                    tags_display = ", ".join([f"#{tag}" for tag in drill["tags"]])
                    st.markdown(f"**Skills**\n{tags_display}")
               
                st.markdown("---")
                st.markdown(f"**📝 Description:** {drill['description']}")
                st.markdown(f"**🛠️ Setup:** {drill['setup']}")
                st.markdown(f"**🔄 Reps:** {drill['reps']}")
                st.markdown(f"**🎯 Objective:** {drill['objective']}")
               
                if st.button(f"✅ Save This Drill", key=f"save_{idx}"):
                    st.success(f"✅ Saved '{drill['name']}' to your favorites!")

# =====================================================
# PAGE 3: AI MATCH ANALYST
# =====================================================
elif page == "🧠 AI Match Analyst":
    st.markdown("### 🧠 Match Analysis")
    st.write("Get personalized feedback on your performance")
   
    # Check if user is logged in
    if not st.session_state.user_name:
        st.warning("👤 Please enter your name on the Home page first!")
        st.stop()
   
    # Create columns for better layout
    col1, col2 = st.columns(2)
   
    with col1:
        st.markdown("#### 📊 Match Stats")
        passes = st.number_input(
            "✅ Passes completed",
            min_value=0,
            max_value=200,
            value=0,
            step=1
        )
        turnovers = st.number_input(
            "❌ Times you lost the ball",
            min_value=0,
            max_value=50,
            value=0,
            step=1
        )
   
    with col2:
        st.markdown("#### ⚽ Goals & Assists")
        goals = st.number_input(
            "⚽ Goals scored",
            min_value=0,
            max_value=10,
            value=0,
            step=1
        )
        assists = st.number_input(
            "🎯 Assists",
            min_value=0,
            max_value=10,
            value=0,
            step=1
        )
   
    st.markdown("---")
   
    st.markdown("#### 💭 Feedback")
    weakness = st.text_area(
        "What was your biggest weakness today?",
        placeholder="e.g., I struggled with passing under pressure in midfield",
        height=80
    )
   
    notes = st.text_area(
        "Any other match notes? (optional)",
        placeholder="e.g., Played well in the first half, lost focus in the second",
        height=80
    )
   
    st.markdown("---")
   
    # Calculate pass accuracy for display
    if passes > 0:
        pass_accuracy = ((passes - turnovers) / passes * 100) if passes > 0 else 0
    else:
        pass_accuracy = 0
   
    # Stats display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pass Accuracy", f"{pass_accuracy:.0f}%", delta=None)
    with col2:
        st.metric("Goals", goals)
    with col3:
        st.metric("Assists", assists)
    with col4:
        st.metric("Ball Losses", turnovers)
   
    st.markdown("---")
   
    # Analyse button
    if st.button("🔍 Analyse My Match", use_container_width=True):
        if not weakness:
            st.error("❌ Tell your coach what your biggest weakness was!")
        else:
            with st.spinner("🤔 Your coach is analysing your match..."):
                # Find matching drills
                matching_drills = []
                for drill in drills:
                    for tag in drill["tags"]:
                        if any(word in weakness.lower() for word in tag.split("_")):
                            matching_drills.append(drill["name"] + " — " + drill["description"])
                            break
               
                drills_text = "\n".join(matching_drills[:3]) if matching_drills else "general training drills"
               
                prompt = f"""You are an elite UEFA Pro License football coach.

Player: {st.session_state.user_name}
Position: {st.session_state.user_position}
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
1. Overall match rating out of 10 (with emoji)
2. Top strength from today
3. Top weakness to work on
4. 2 specific drills from the database above to fix the weakness
5. One motivational message to end

Be direct, specific and encouraging like a real coach. Use emojis and formatting."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
               
                st.markdown("---")
                st.markdown("### 📋 Coach's Feedback:")
                st.markdown(response.choices[0].message.content)
                st.markdown("---")
               
                # Recommendation section
                st.success("💡 Next Steps:")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("✅ **This Week**\nFocus on the recommended drills")
                with col2:
                    st.markdown("📈 **Track Progress**\nAnalyse your match again next week")

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Made with ❤️ for football lovers | Powered by AI</p>
    <p style='font-size: 0.8rem;'>© 2024 Soccer AI Coach | All rights reserved</p>
</div>
""", unsafe_allow_html=True)
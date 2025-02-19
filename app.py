import streamlit as st
import random
import pandas as pd
from datetime import date, datetime

# Initialize Session State for User Data
if "users" not in st.session_state:
    st.session_state.users = {}
if "streaks" not in st.session_state:
    st.session_state.streaks = {}
if "last_login" not in st.session_state:
    st.session_state.last_login = {}

# App Title
st.title("🚀 Growth Mindset Interactive Web App")

# Sidebar - User Input
st.sidebar.header("👤 Your Information")
name = st.sidebar.text_input("Enter Your Name:", value="").strip()
goal = st.sidebar.text_input("What is Your Learning Goal?")
learning_style = st.sidebar.selectbox(
    "What is Your Preferred Learning Style?", ["Visual", "Reading/Writing", "Hands-on", "Listening"]
)

def generate_challenge():
    challenges = [
        "Write down 3 things you learned today.",
        "Teach someone a new concept you learned.",
        "Read an article on a topic you find difficult.",
        "Practice a skill for at least 30 minutes today.",
        "Watch a TED Talk related to personal growth.",
        "Write a journal entry about your learning progress."
    ]
    return random.choice(challenges)

def generate_tip():
    tips = [
        "Stay consistent and keep pushing forward!",
        "Break your learning into small, manageable tasks.",
        "Celebrate small wins to stay motivated.",
        "Find a study buddy to keep yourself accountable.",
        "Use the Pomodoro technique for better focus.",
        "Sleep well! A fresh mind learns faster.",
    ]
    return random.choice(tips)

# Check if user entered a name
if name:
    if name not in st.session_state.users:
        st.session_state.users[name] = {"Effort Level": 5, "Learning Progress": 5, "Feedback": "", "Last Active": str(date.today()), "Login Count": 1}
        st.session_state.streaks[name] = 1
        st.session_state.last_login[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        st.session_state.users[name]["Login Count"] += 1
        st.session_state.last_login[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update Streaks
    if st.session_state.users[name]["Last Active"] != str(date.today()):
        st.session_state.users[name]["Last Active"] = str(date.today())
        st.session_state.streaks[name] += 1
    
    # Welcome Message
    st.markdown(f"### 🌟 Welcome, {name}! Your Goal: **{goal if goal else 'Not Set'}**")
    
    # Streak Display
    st.sidebar.markdown(f"🔥 **Current Streak:** {st.session_state.streaks[name]} days")
    st.sidebar.markdown(f"📅 **Total Logins:** {st.session_state.users[name]['Login Count']}")

    # Daily Challenge
    st.subheader("🎯 Today's Challenge")
    st.info(generate_challenge())

    # Motivational Quotes
    st.subheader("💡 Inspirational Quote")
    quotes = [
        "Mistakes are the best teachers.",
        "Effort is the key that unlocks success.",
        "Every challenge is a new learning opportunity.",
        "Success comes from persistent effort.",
        "Believe in yourself and your ability to grow.",
        "Failure is not the opposite of success; it is part of success."
    ]
    if st.button("🚀 Show Me a Motivational Quote!"):
        st.success(random.choice(quotes))

    # Growth Tips
    st.subheader("📌 Growth Tip of the Day")
    st.info(generate_tip())

    # Self-Assessment Progress Tracker
    st.subheader("📊 Growth Mindset Progress Tracker")
    st.session_state.users[name]["Effort Level"] = st.slider(
        "How much effort are you putting in? (1-10)", 1, 10, st.session_state.users[name]["Effort Level"]
    )
    st.session_state.users[name]["Learning Progress"] = st.slider(
        "How much are you improving your skills? (1-10)", 1, 10, st.session_state.users[name]["Learning Progress"]
    )
    
    # Progress Bar
    st.progress(st.session_state.users[name]["Learning Progress"] / 10)

    # Feedback System
    st.subheader("📝 Share Your Thoughts")
    st.session_state.users[name]["Feedback"] = st.text_area(
        "What do you think about the growth mindset?",
        value=st.session_state.users[name]["Feedback"]
    )
    if st.button("Submit Feedback"):
        st.success("Thank you! Your feedback has been saved. 🎉")

    # Leaderboard (Top Learners)
    st.subheader("🏆 Top Learners Leaderboard")
    df = pd.DataFrame.from_dict(st.session_state.users, orient="index")
    df = df.sort_values(by=["Effort Level", "Learning Progress"], ascending=False)
    st.table(df)

    # Learning Progress Chart
    st.subheader("📈 Learning Progress Chart")
    st.line_chart(df[["Effort Level", "Learning Progress"]])

    # Display Learning Style
    st.info(f"🧠 Your preferred learning style: **{learning_style}**")  
else:
    st.warning("Please enter your name in the sidebar to continue.")

import streamlit as st
import pandas as pd
import random

# Load the CSV file
csv_url = "https://raw.githubusercontent.com/kwonsungja/My-homepy/main/regular_Nouns_real.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(csv_url)
    df.columns = df.columns.str.lower()
    df["singular"] = df["singular"].str.strip()
    df["level"] = df["level"].str.strip()
    return df

df = load_data()

# Pluralization logic
def pluralize(noun):
    if noun.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z', 'o')):
        return noun + 'es'
    elif noun.endswith('y') and not noun[-2] in 'aeiou':
        return noun[:-1] + 'ies'
    return noun + 's'

# Initialize session state for user state
if "user_state" not in st.session_state:
    st.session_state.user_state = {
        "remaining_nouns": pd.DataFrame(),
        "current_level": None,
        "current_noun": "",
        "score": 0,
        "trials": 0,
        "feedback": "",
        "user_name": "",
    }

# Layout Title and Instructions
st.title("NounSmart: Practice Regular Plural Nouns")
st.markdown("""
## How to Use the App
1. **Enter your name** to personalize the experience.
2. **Follow the steps below** from Step 1 to Step 4.
3. Click **'Show Report'** to see your final score.
""")

# Step 0: Enter User Name
st.subheader("Enter Your Name")
if "user_name" not in st.session_state.user_state:
    st.session_state.user_state["user_name"] = ""  # Ensure key exists
user_name = st.text_input("Your Name", value=st.session_state.user_state["user_name"], placeholder="Enter your name here")

if user_name:
    st.session_state.user_state["user_name"] = user_name
    st.success(f"Welcome, **{user_name}**! 🎉")

# Step 1: Select a Level
st.subheader("Step 1: Select a Level to Start")
levels = df["level"].unique()
selected_level = st.selectbox("Select a Level", levels)

# Step 2: Show the Noun
st.subheader("Step 2: Show the Noun")
if st.button("Click to Show the Noun"):
    state = st.session_state.user_state
    if state["current_level"] != selected_level:
        state["remaining_nouns"] = df[df["level"] == selected_level].copy()
        state["current_level"], state["score"], state["trials"] = selected_level, 0, 0

    if not state["remaining_nouns"].empty:
        state["current_noun"] = random.choice(state["remaining_nouns"]["singular"].tolist())
        state["feedback"] = ""
    else:
        st.warning("No nouns available for this level. Please select a different level.")

current_noun = st.session_state.user_state["current_noun"]
if current_noun:
    st.text_input("Singular Noun", value=current_noun, disabled=True)

# Step 3: Type Your Answer
st.subheader("Step 3: Type Your Answer")
user_input = st.text_input("Type the plural form here:")

# Step 4: Check Answer
st.subheader("Step 4: Check Answer")
if st.button("Check Answer"):
    state = st.session_state.user_state
    if not state["current_noun"]:
        st.warning("Please click 'Show the Noun' first!")
    else:
        correct_plural = pluralize(state["current_noun"])
        state["trials"] += 1

        if user_input.strip().lower() == correct_plural.lower():
            state["score"] += 1
            state["feedback"] = f"✅ Correct! The plural form of '{state['current_noun']}' is '{correct_plural}'."
            state["remaining_nouns"] = state["remaining_nouns"][
                state["remaining_nouns"]["singular"] != state["current_noun"]
            ]
        else:
            state["feedback"] = f"❌ Incorrect. The correct plural form of '{state['current_noun']}' is '{correct_plural}'."

        st.success(state["feedback"])
        st.write(f"### {state['user_name']}, Your Score: {state['score']} / {state['trials']}")

# Final Report
if st.button("Show Report"):
    state = st.session_state.user_state
    user_name_display = state.get("user_name", "Player")  # Safeguard fallback
    st.subheader("Final Report")
    st.write(f"**{user_name_display}, Your Total Score:** {state['score']} correct out of {state['trials']} attempts.")

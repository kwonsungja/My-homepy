import streamlit as st
import pandas as pd
import random

# Load the CSV file
csv_url = "https://raw.githubusercontent.com/kwonsungja/My-homepy/main/regular_Nouns_real.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(csv_url)
        df.columns = df.columns.str.lower()
        df["singular"] = df["singular"].str.strip()
        df["level"] = df["level"].str.strip()
        return df
    except Exception as e:
        st.error(f"Failed to load CSV file: {e}")
        return pd.DataFrame()

df = load_data()

# Initialize session state
if "user_state" not in st.session_state:
    st.session_state.user_state = {
        "remaining_nouns": pd.DataFrame(),
        "current_level": None,
        "score": 0,
        "trials": 0,
        "current_index": -1,
        "level_scores": {level: {"score": 0, "trials": 0} for level in ["s", "es", "ies"]}
    }

def pluralize(noun):
    noun = noun.strip()
    if noun.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z', 'o')):
        return noun + 'es'
    elif noun.endswith('y') and not noun[-2] in 'aeiou':
        return noun[:-1] + 'ies'
    else:
        return noun + 's'

# UI Components
st.title("NounSmart: Practice Regular Plural Nouns")
st.markdown("### Follow the steps to practice your plural noun skills!")

# Step 0: User Name
user_name = st.text_input("**Step 0: Enter Your Name**", placeholder="Enter your name here")
if user_name:
    st.write(f"### Welcome, {user_name}! 🎉")

# Step 1: Select Level
st.write("### Step 1: Select a Level")
levels = ["s", "es", "ies"]
level = st.selectbox("Select a Level", levels)

if st.button("Step 2: Show the Noun"):
    state = st.session_state.user_state
    if state["current_level"] != level:
        state["remaining_nouns"] = df[df["level"] == level].copy()
        state["current_level"] = level
        state["score"], state["trials"] = 0, 0

    if not state["remaining_nouns"].empty:
        state["current_index"] = random.randint(0, len(state["remaining_nouns"]) - 1)
        current_noun = state["remaining_nouns"].iloc[state["current_index"]]["singular"]
        state["current_noun"] = current_noun
        st.session_state.feedback = ""
        st.write(f"### What's the plural form of: **{current_noun}**?")
    else:
        st.warning("No nouns available for this level.")

# Step 3: Input Answer
user_input = st.text_input("**Step 3: Type Your Answer**", placeholder="Type the plural form here")

# Step 4: Check Answer
if st.button("Check Answer"):
    state = st.session_state.user_state
    if "current_noun" in state and state["current_noun"]:
        correct_plural = pluralize(state["current_noun"])
        state["trials"] += 1
        if user_input.strip().lower() == correct_plural:
            state["score"] += 1
            st.success(f"✅ Correct! The plural form is '{correct_plural}'.")
            state["remaining_nouns"] = state["remaining_nouns"].drop(state["remaining_nouns"].index[state["current_index"]])
        else:
            st.error(f"❌ Incorrect! The correct plural form is '{correct_plural}'.")
    else:
        st.warning("Please show a noun first!")

# Display Score
st.write(f"### Score: {st.session_state.user_state['score']} / {st.session_state.user_state['trials']}")




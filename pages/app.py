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

# Pluralization function
def pluralize(noun):
    noun = noun.strip()
    if noun.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z', 'o')):
        return noun + 'es'
    elif noun.endswith('y') and not noun[-2] in 'aeiou':
        return noun[:-1] + 'ies'
    return noun + 's'

# Initialize Streamlit state
if "user_state" not in st.session_state:
    st.session_state.user_state = {
        "remaining_nouns": pd.DataFrame(),
        "current_level": None,
        "score": 0,
        "trials": 0,
        "current_index": -1,
        "current_noun": None,
        "feedback": "",
    }

# Layout in Streamlit
st.title("NounSmart: Practice Regular Plural Nouns")
st.write("### Follow the steps to improve your plural noun skills!")

# Step 0: Enter Your Name
user_name = st.text_input("**Step 0: Enter Your Name**", placeholder="Enter your name here")
if user_name:
    st.write(f"### Welcome, **{user_name}!**")

# Step 1: Select a Level
st.write("### Step 1: Select a Level to Start")
levels = ["s", "es", "ies"]
selected_level = st.selectbox("Choose a Level", levels)

# Step 2: Show the Noun
if st.button("Step 2: Show the Noun"):
    state = st.session_state.user_state
    
    # Reset game state if level changes
    if state["current_level"] != selected_level:
        state["remaining_nouns"] = df[df["level"] == selected_level].copy()
        state["current_level"], state["score"], state["trials"] = selected_level, 0, 0

    # Pick a random noun
    if not state["remaining_nouns"].empty:
        state["current_index"] = random.randint(0, len(state["remaining_nouns"]) - 1)
        state["current_noun"] = state["remaining_nouns"].iloc[state["current_index"]]["singular"]
        state["feedback"] = ""
        st.write(f"### What's the plural form of: **{state['current_noun']}**?")
    else:
        st.warning("No nouns available for this level. Please select another level.")

# Step 3: Input the Plural Form
user_input = st.text_input("**Step 3: Type Your Answer**", placeholder="Enter the plural form here")

# Step 4: Check Answer
if st.button("Step 4: Check Answer"):
    state = st.session_state.user_state

    if state.get("current_noun") is None:
        st.warning("Please click 'Show the Noun' first!")
    else:
        correct_plural = pluralize(state["current_noun"])
        state["trials"] += 1

        if user_input.strip().lower() == correct_plural.lower():
            state["score"] += 1
            state["feedback"] = f"✅ Correct! The plural form of '{state['current_noun']}' is '{correct_plural}'."
            # Remove the noun from remaining nouns
            state["remaining_nouns"] = state["remaining_nouns"].drop(
                state["remaining_nouns"].index[state["current_index"]]
            ).reset_index(drop=True)
        else:
            state["feedback"] = f"❌ Incorrect. The correct plural form of '{state['current_noun']}' is '{correct_plural}'."

        # Display feedback and score
        st.write(state["feedback"])
        st.write(f"### Score: {state['score']} / {state['trials']}")

# Final Report
if st.button("Show Report"):
    state = st.session_state.user_state
    st.write("### Final Report")
    st.write(f"**Total Score:** {state['score']} correct out of {state['trials']} attempts.")

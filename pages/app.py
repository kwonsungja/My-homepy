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
    noun = noun.strip()
    if noun.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z', 'o')):
        return noun + 'es'
    elif noun.endswith('y') and not noun[-2] in 'aeiou':
        return noun[:-1] + 'ies'
    return noun + 's'

# Initialize session state
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "remaining_nouns": pd.DataFrame(),
        "current_level": None,
        "current_noun": "",
        "score": 0,
        "trials": 0,
        "feedback": "",
    }

# UI Layout
st.title("NounSmart: Practice Regular Plural Nouns")
st.write("### Follow the steps below to practice forming plural nouns!")

# Step 1: Select Level
st.write("### Step 1: Select a Level")
levels = df["level"].unique()
selected_level = st.selectbox("Choose a Level", levels)

# Step 2: Show the Noun
if st.button("Step 2: Show the Noun"):
    game_state = st.session_state.game_state
    if game_state["current_level"] != selected_level:
        game_state["remaining_nouns"] = df[df["level"] == selected_level].copy()
        game_state["current_level"] = selected_level
        game_state["score"] = 0
        game_state["trials"] = 0

    if not game_state["remaining_nouns"].empty:
        game_state["current_noun"] = random.choice(game_state["remaining_nouns"]["singular"].tolist())
        st.session_state.feedback = ""
    else:
        st.warning("No nouns available for this level. Please select a different level.")

# Display the noun
current_noun = st.session_state.game_state["current_noun"]
if current_noun:
    st.text_input("Singular Noun", value=current_noun, disabled=True)

# Step 3: Input the plural form
st.write("### Step 3: Type Your Answer")
user_input = st.text_input("Type the plural form here:")

# Step 4: Check the answer
if st.button("Step 4: Check Answer"):
    game_state = st.session_state.game_state
    if current_noun:
        correct_plural = pluralize(current_noun)
        game_state["trials"] += 1

        if user_input.strip().lower() == correct_plural.lower():
            game_state["score"] += 1
            game_state["feedback"] = f"✅ Correct! The plural form of '{current_noun}' is '{correct_plural}'."
            # Remove the noun after answering correctly
            game_state["remaining_nouns"] = game_state["remaining_nouns"][
                game_state["remaining_nouns"]["singular"] != current_noun
            ]
        else:
            game_state["feedback"] = f"❌ Incorrect. The correct plural form of '{current_noun}' is '{correct_plural}'."

        # Show feedback
        st.success(game_state["feedback"])
        st.write(f"### Score: {game_state['score']} / {game_state['trials']}")
    else:
        st.warning("Please click 'Show the Noun' first!")

# Final Report
if st.button("Show Report"):
    game_state = st.session_state.game_state
    st.write("### Final Report")
    st.write(f"**Total Score:** {game_state['score']} correct out of {game_state['trials']} attempts.")




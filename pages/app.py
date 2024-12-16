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

# Initialize session state for game_state
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "remaining_nouns": pd.DataFrame(),
        "current_level": None,
        "current_noun": "",
        "score": 0,
        "trials": 0,
        "feedback": "",
        "user_name": None,  # Ensure user_name is initialized as None
    }

# Layout
st.title("NounSmart: Practice Regular Plural Nouns")
st.markdown("""
## How to Use the App
1. Enter your name to personalize the experience.
2. Follow the steps **from Step 1 to Step 4**.
3. Click **'Show Report'** to view overall feedback across all levels.
""")

# Step 0: Enter User Name
if st.session_state.game_state["user_name"] is None:
    st.markdown("### **Step 0: Enter Your Name**")
    user_name = st.text_input("Your Name", placeholder="Enter your name here")
    if user_name:
        st.session_state.game_state["user_name"] = user_name
        st.success(f"Welcome, **{user_name}**! 🎉")
        st.experimental_rerun()
else:
    user_name = st.session_state.game_state["user_name"]
    st.write(f"### 👋 Welcome, **{user_name}!**")

# Step 1: Select a Level
st.markdown("### **Step 1: Select a Level to Start**")
levels = ["s", "es", "ies"]
selected_level = st.selectbox("Choose a Level", levels)

# Step 2: Show the Noun
if st.button("Step 2: Show the Noun"):
    state = st.session_state.game_state
    if state["current_level"] != selected_level:
        state["remaining_nouns"] = df[df["level"] == selected_level].copy()
        state["current_level"], state["score"], state["trials"] = selected_level, 0, 0

    if not state["remaining_nouns"].empty:
        state["current_noun"] = random.choice(state["remaining_nouns"]["singular"].tolist())
        state["feedback"] = ""
    else:
        st.warning("No nouns available for this level. Please select a different level.")

# Display the noun
current_noun = st.session_state.game_state["current_noun"]
if current_noun:
    st.text_input("Singular Noun", value=current_noun, disabled=True)

# Step 3: Input the Plural Form
st.markdown("### **Step 3: Type Your Answer**")
user_input = st.text_input("Type the plural form here:")

# Step 4: Check Answer
if st.button("Step 4: Check Answer"):
    state = st.session_state.game_state
    if not state["current_noun"]:
        st.warning("Please click 'Show the Noun' first!")
    else:
        correct_plural = pluralize(state["current_noun"])
        state["trials"] += 1

        if user_input.strip().lower() == correct_plural.lower():
            state["score"] += 1
            state["feedback"] = f"✅ Correct! The plural form of '{state['current_noun']}' is '{correct_plural}'."
            # Remove answered noun
            state["remaining_nouns"] = state["remaining_nouns"][
                state["remaining_nouns"]["singular"] != state["current_noun"]
            ]
        else:
            state["feedback"] = f"❌ Incorrect. The correct plural form of '{state['current_noun']}' is '{correct_plural}'."

        # Show feedback and score
        st.success(state["feedback"])
        st.write(f"### {state['user_name']}, Your Score: {state['score']} / {state['trials']}")

# Show Report
if st.button("Show Report"):
    state = st.session_state.game_state
    st.markdown("### **Final Report**")
    st.write(f"**{state['user_name']}, Your Total Score:** {state['score']} correct out of {state['trials']} attempts.")



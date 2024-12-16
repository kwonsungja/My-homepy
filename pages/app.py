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

# State initialization
if "state" not in st.session_state:
    st.session_state.state = {
        "remaining_nouns": pd.DataFrame(),
        "current_level": None,
        "score": 0,
        "trials": 0,
        "current_index": -1,
        "level_scores": {"s": {"score": 0, "trials": 0}, 
                         "es": {"score": 0, "trials": 0}, 
                         "ies": {"score": 0, "trials": 0}}
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
st.write("Follow the steps to practice your plural noun skills!")

# Step 1: Select a level
levels = df["level"].unique()
selected_level = st.selectbox("Step 1: Select a Level", options=levels)

# Update nouns based on level
if st.button("Step 2: Show the Noun"):
    filtered = df[df["level"] == selected_level].copy()
    if not filtered.empty:
        st.session_state.state["remaining_nouns"] = filtered
        st.session_state.state["current_level"] = selected_level
        st.session_state.state["current_index"] = random.randint(0, len(filtered) - 1)
        current_noun = filtered.iloc[st.session_state.state["current_index"]]["singular"]
        st.session_state.state["current_noun"] = current_noun
        st.write(f"What's the plural form of: **{current_noun}**?")
    else:
        st.error("No nouns found for the selected level.")

# Step 3: Input answer
user_input = st.text_input("Step 3: Type the plural form here")

# Step 4: Check answer
if st.button("Check Answer"):
    state = st.session_state.state
    if "current_noun" in state:
        correct_plural = pluralize(state["current_noun"])
        if user_input.strip().lower() == correct_plural.strip().lower():
            st.success(f"✅ Correct! '{correct_plural}' is the plural form.")
        else:
            st.error(f"❌ Incorrect. The correct plural form is '{correct_plural}'.")
    else:
        st.warning("Please click 'Show the Noun' first.")


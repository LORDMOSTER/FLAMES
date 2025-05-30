import streamlit as st
import os

# Function to calculate FLAMES
def calculate_flames(name1, name2):
    name1 = name1.replace(" ", "").lower()
    name2 = name2.replace(" ", "").lower()

    for letter in name1[:]:
        if letter in name2:
            name1 = name1.replace(letter, "", 1)
            name2 = name2.replace(letter, "", 1)

    count = len(name1 + name2)

    flames = ['F', 'L', 'A', 'M', 'E', 'S']
    while len(flames) > 1:
        split_index = (count % len(flames)) - 1
        if split_index >= 0:
            flames = flames[split_index+1:] + flames[:split_index]
        else:
            flames = flames[:len(flames)-1]

    result_map = {
        'F': 'Friendship 💛',
        'L': 'Love ❤️',
        'A': 'Affection 💖',
        'M': 'Marriage 💍',
        'E': 'Enemies 💔',
        'S': 'Siblings 🤗'
    }

    return result_map[flames[0]]

# Page config
st.set_page_config(page_title="FLAMES Game", layout="centered")

# Load and apply custom CSS (handle missing file gracefully)
if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("Custom styles not found. Please ensure 'styles.css' exists.")

# Session state
if "started" not in st.session_state:
    st.session_state.started = False
if "result" not in st.session_state:
    st.session_state.result = None

# UI
st.markdown('<div class="background"></div>', unsafe_allow_html=True)  # background div

if not st.session_state.started:
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh;">
            <h1 class='welcome-text'>💘 Welcome to the FLAMES Game 💘</h1>
            <h4 class='subtext'>Discover your fate with your crush ✨</h4>
            <div style="margin-top: 2rem;">
                <!-- Button will be rendered by Streamlit below -->
            </div>
        </div>
    """, unsafe_allow_html=True)
    # Center the button using Streamlit's container
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("💝 Start Game"):
            st.session_state.started = True
            # No rerun needed; Streamlit will update the UI automatically
else:
    st.markdown("<h2 class='subtext'>Enter the names below:</h2>", unsafe_allow_html=True)
    name1 = st.text_input("Your Name", key="name1", placeholder="Enter your name", help="Type your name here")
    name2 = st.text_input("Crush's Name", key="name2", placeholder="Enter your crush's name", help="Type your crush's name here")

    if st.button("🔮 Predict"):
        # Input validation
        if not name1.strip() or not name2.strip():
            st.warning("Please fill both names!")
            st.session_state.result = None
        elif not (name1.replace(" ", "").isalpha() and name2.replace(" ", "").isalpha()):
            st.warning("Names should only contain alphabetic characters!")
            st.session_state.result = None
        else:
            result = calculate_flames(name1, name2)
            st.session_state.result = result
            # st.balloons()  # Removed balloons animation

    if st.session_state.result:
        st.success(f"Result: {st.session_state.result}")

    if st.button("🔄 Play Again"):
        st.session_state.started = False
        st.session_state.result = None
        st.experimental_rerun()

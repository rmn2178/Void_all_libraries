import streamlit as st
import requests
from streamlit_lottie import st_lottie

# --- PAGE CONFIG ---
st.set_page_config(page_title="Animated To-Do", page_icon="✅")


# --- COMPATIBILITY LAYER ---
def trigger_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


# --- LOAD ASSETS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


# Newer stable links
lottie_todo = load_lottieurl("https://lottie.host/570e30d7-df7e-469b-891c-9988f047065e/l5k55C2hC7.json")
lottie_success = load_lottieurl("https://lottie.host/804d092d-961d-4034-8025-055998a41753/mJ96z9jP90.json")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .task-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        animation: fadeIn 0.4s ease-out;
        border-left: 5px solid #ff4b4b;
        color: #31333F;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "todos" not in st.session_state:
    st.session_state.todos = []

# --- UI LAYOUT ---
st.title("✅ Animated To-Do List")

col1, col2 = st.columns([1, 3])
with col1:
    if lottie_todo:
        st_lottie(lottie_todo, height=100, key="main_icon")
    else:
        st.write("📝")

# Input Section - Using a form for better UX
with st.form("todo_form", clear_on_submit=True):
    new_todo = st.text_input("Add a new task:", placeholder="What needs doing?")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_todo:
        st.session_state.todos.append({"task": new_todo, "done": False})
        trigger_rerun()

# Replaced st.divider() with Markdown for older versions
st.markdown("---")

# --- DISPLAY TASKS ---
if not st.session_state.todos:
    st.info("No tasks yet! Add one above.")
else:
    for i, todo in enumerate(st.session_state.todos):
        with st.container():
            c1, c2, c3 = st.columns([1, 8, 1])

            # Checkbox
            done = c1.checkbox("", value=todo["done"], key=f"check_{i}")
            if done != todo["done"]:
                st.session_state.todos[i]["done"] = done
                trigger_rerun()

            # Text Style
            text_style = "text-decoration: line-through; opacity: 0.5;" if todo["done"] else ""
            c2.markdown(f"<div class='task-card' style='{text_style}'>{todo['task']}</div>", unsafe_allow_html=True)

            # Delete
            if c3.button("🗑️", key=f"del_{i}"):
                st.session_state.todos.pop(i)
                trigger_rerun()

# --- SUCCESS CELEBRATION ---
if len(st.session_state.todos) > 0 and all(t["done"] for t in st.session_state.todos):
    st.balloons()
    if lottie_success:
        st_lottie(lottie_success, height=150)
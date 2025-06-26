import streamlit as st
import json

# Load FAQs
with open("faqs.json", "r") as f:
    faqs = json.load(f)

st.set_page_config(page_title="SupportHub", layout="wide")

st.markdown("""
    <style>
        .navbar {
            background-color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 999;
            margin-top: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar-title {
            font-size: 3rem;
            font-weight: 900;
            color: #222;
        }

        .nav-links a {
            margin-left: 1.5rem;
            text-decoration: none;
            color: #333;
            font-size: 1rem;
            font-weight: 500;
        }

        .nav-links a:hover {
            color: #007bff;
        }
    </style>

    <div class="navbar">
        <div class="navbar-title">SupportHub</div>
        <div class="nav-links">
            <a href="#home">Home</a>
            <a href="#support">Support</a>
            <a href="#contact">Contact</a>
        </div>
    </div>
""", unsafe_allow_html=True)
# --- Hero Section ---
st.markdown("""
    <div class='hero' id='home' style='margin-top: 3rem; text-align: center;'>
        <h1 style='font-size: 3rem; font-weight: 700; margin-bottom: 1rem;'>How can we help you today?</h1>
        <p style='font-size: 1.2rem; color: #555;'>Find answers to your questions or get in touch with our support team.</p>
    </div>
""", unsafe_allow_html=True)

search = st.text_input("Search for help...", key="search_box")

# --- FAQs Section ---
st.markdown("<div id='support'></div>", unsafe_allow_html=True)
st.markdown("## 📌 Frequently Asked Questions", unsafe_allow_html=True)
filtered_faqs = [f for f in faqs if search.lower() in f['question'].lower()] if search else faqs[:5]
for item in filtered_faqs:
    with st.expander(item["question"]):
        st.markdown(item["answer"])

# --- Support Cards ---
st.markdown("### 💬 Other Options")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Live Chat")
    st.write("Connect with our support bot for quick assistance.")
    if st.button("Start Chat"):
        st.session_state["chat_active"] = True

with col2:
    st.subheader("Guides")
    st.write("Access detailed guides and tutorials to help you get started.")

# --- ChatBot ---
if st.session_state.get("chat_active"):
    st.markdown("---")
    st.subheader("Support Bot")
    user_msg = st.text_input("Type your question:", key="chat_input")
    if user_msg:
        matched = next((f for f in faqs if user_msg.lower() in f["question"].lower()), None)
        answer = matched["answer"] if matched else "Sorry, I don’t have that answer. Try the contact form below."
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Bot:** {answer}")

# --- Contact Form ---
st.markdown("---")
st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
st.subheader("📨 Contact Us")
with st.form("contact_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submitted = st.form_submit_button("Send Message")
    if submitted:
        st.success("Thank you! We'll get back to you soon.")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 SupportHub. All rights reserved.", unsafe_allow_html=True)
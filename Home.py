import streamlit as st
from utils import show_logo_and_title
# --- LOGO + TITLE (Header Section) ---
show_logo_and_title()


# --- PAGE CONFIG ---
st.set_page_config(page_title="BookHub | Home", page_icon="📚", layout="wide")

# --- APPLY CUSTOM CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- STYLE ADJUSTMENTS FOR SIDEBAR & TOOLBAR ---
st.markdown("""
    <style>
    [data-testid="stHeader"] {
        background: none;
        height: 0px;
    }
    [data-testid="stToolbar"] button {
        visibility: visible !important;
        opacity: 1 !important;
        background-color: #1e3cfc !important;
        color: white !important;
        border: none !important;
        border-radius: 4px;
        padding: 0.25rem 0.6rem;
        transition: 0.2s ease-in-out;
    }
    [data-testid="stToolbar"] button:hover {
        background-color: #315efb !important;
        transform: scale(1.05);
    }
    [data-testid="stToolbar"] {
        right: 1rem;
        top: 0.5rem;
        display: flex !important;
        align-items: center;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: 1rem;
    }
            

        
    </style>
""", unsafe_allow_html=True)




# --- ABOUT SECTION ---
st.markdown("""
<div class='about-section'>
<h3>💡 Our Motive</h3>
<p>
Many valuable books remain unused after a period of time, while countless students and learners struggle to access the same resources due to cost or availability.

BookHub bridges this gap by connecting book donors with learners through a simple and accessible platform. Donors can easily share their unused books, and users can explore, request, and access them based on their needs.

By supporting free sharing, optional paid access, and secure borrowing through refundable deposits, BookHub promotes a sustainable ecosystem of knowledge exchange.

Our mission is to make learning more accessible, encourage responsible sharing, and create equal opportunities for everyone.
</p>

<h3>🌟 Key Features</h3>
<ul>
<li>📚 Free & Paid Book Access System</li>
<li>🤝Transparent Donor Details</li>
<li>🔐Simple Login & Signup System</li>
<li>🔍 Smart Search & Category Filtering</li>
<li>📦 Real-time Request Tracking</li>
<li>🔒 Security Deposit for Safe Borrowing</li>
<li>🛠️ Admin Dashboard with Analytics</li>
</ul>
            
<h3>🚀 How It Works</h3>
<ol>
<li> Donors upload books (Free / Paid / Deposit)</li>
<li>Users browse and request books</li>
<li>Admin approves and manages delivery</li>
<li>Users track request and receive books</li>
<li>Deposit is refunded after return (if applicable)</li>
</ol>


</div>
""", unsafe_allow_html=True)

# --- CALL TO ACTION (Get Started Button) ---
st.markdown("<div class='get-started-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Get Started", key="get_started_btn"):
        st.switch_page("pages/login.py")
st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div class='footer'>© 2026 BookHub | Empowering Learning Through Sharing </div>", unsafe_allow_html=True)

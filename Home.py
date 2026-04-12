import streamlit as st
from utils import show_logo_and_title

# --- PAGE CONFIG (must be first Streamlit command) ---
st.set_page_config(page_title="BookHub | Home", page_icon="📚", layout="wide")

# --- APPLY CUSTOM CSS ---
def local_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- EXTRA HOME PAGE CSS ---
st.markdown("""
<style>
/* Remove default top header space */
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

[data-testid="stToolbar"] {
    right: 1rem;
    top: 0.5rem;
    display: flex !important;
    align-items: center;
}

[data-testid="stToolbar"] button {
    visibility: visible !important;
    opacity: 1 !important;
    background-color: #1e3cfc !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.3rem 0.7rem !important;
    transition: 0.2s ease-in-out;
}

[data-testid="stToolbar"] button:hover {
    background-color: #315efb !important;
    transform: scale(1.05);
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
}

/* Hero Section */
.hero-box {
    background: linear-gradient(135deg, #e0f2fe, #bfdbfe);  /* lighter blue */
    color: #0f172a;  /* dark text instead of white */
    border-radius: 24px;
    padding: 55px 35px;
    text-align: center;
    margin: 10px 0 25px 0;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
}

/* Title */
.hero-title {
    font-size: 50px;
    font-weight: 800;
    margin-bottom: 12px;
    color: #0f172a !important;  /* dark text */
}

/* Subtitle */
.hero-subtitle {
    font-size: 22px;
    line-height: 1.8;
    max-width: 900px;
    margin: 0 auto;
    color: #1e293b !important;  /* softer dark */
}
/* Highlight Stats */
.stats-box {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    border: 1px solid #dbeafe;
}

.stats-number {
    font-size: 28px;
    font-weight: 800;
    color: white !important;
    margin-bottom: 6px;
}

.stats-label {
    font-size: 16px;
    color: #dbeafe !important;
}

/* Section Card */
.section-card {
    background: linear-gradient(135deg, #e0f2fe, #bfdbfe);
    border-radius: 22px;
    padding: 35px;
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.15);
    margin-top: 20px;
    border: 1px solid #bfdbfe;
}
.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #1e3a8a !important;
    margin-bottom: 15px;
}

.section-text {
    font-size: 21px;
    line-height: 1.95;
    color: #0f172a !important;
}

/* Feature cards */
.feature-card {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-radius: 20px;
    padding: 28px 22px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.12);
    border: 1px solid #dbeafe;

    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 30px rgba(37, 99, 235, 0.16);
}

.feature-icon {
    font-size: 38px;
    margin-bottom: 14px;
    line-height: 1;
}

.feature-title {
    font-size: 22px;
    font-weight: 700;
    color: #1e3a8a !important;
    margin-bottom: 14px;
     min-height: 56px;   /* title area same height */
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.feature-desc {
    font-size: 17px;
    line-height: 1.7;
    color: #334155 !important;
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

/* Steps */
.step-card {
    background: #ffffff;
    border-left: 6px solid #2563EB;
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
    margin-bottom: 16px;
}

.step-title {
    font-size: 22px;
    font-weight: 700;
    color: #1e3a8a !important;
    margin-bottom: 6px;
}

.step-desc {
    font-size: 18px;
    color: #334155 !important;
    line-height: 1.7;
}

/* CTA wrapper */
.cta-box {
    background: linear-gradient(135deg, #e0f2fe, #bfdbfe);
    border-radius: 22px;
    padding: 35px 25px;
    text-align: center;
    margin-top: 30px;
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.15);
}

.cta-title {
    font-size: 34px;
    font-weight: 800;
    color: #1e3a8a !important;
    margin-bottom: 8px;
}

.cta-text {
    font-size: 20px;
    color: #334155 !important;
    margin-bottom: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #334155;
    font-size: 16px;
    margin-top: 35px;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# --- LOGO + TITLE ---
show_logo_and_title()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-box">
    <div class="hero-title">📚 Discover, Share & Learn</div>
    <div class="hero-subtitle">
        A smart and student-friendly platform where donors can share books, 
        learners can discover the resources they need, and knowledge can reach 
        more people through free access, borrowing, and flexible delivery options.
    </div>
</div>
""", unsafe_allow_html=True)

# --- QUICK HIGHLIGHTS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stats-box">
        <h3 class="stats-number">2 Modes</h3>
        <p class="stats-label">Free Access & Borrow System</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-box">
        <h3 class="stats-number">Smart Flow</h3>
        <p class="stats-label">Request, Courier Payment & Tracking</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-box">
        <h3 class="stats-number">Admin Control</h3>
        <p class="stats-label">Manage Delivery, Returns & Analytics</p>
    </div>
    """, unsafe_allow_html=True)

# --- MOTIVE SECTION ---
st.markdown("""
<div class="section-card">
    <div class="section-title">💡 Our Motive</div>
    <div class="section-text">
        Many useful books remain unused after a period of time, while many students and learners 
        still search for the same resources but cannot afford them easily. BookHub is designed to 
        bridge this gap by connecting donors and learners on one simple platform.
        <br><br>
        Through BookHub, donors can share books they no longer need, and users can browse, request, 
        and access books in a transparent and organized way. By supporting free sharing, optional paid 
        access, and deposit-based borrowing, BookHub promotes knowledge sharing, sustainability, and 
        equal learning opportunities for everyone.
    </div>
</div>
""", unsafe_allow_html=True)

# --- FEATURES SECTION ---
st.markdown("<div class='section-title' style='margin-top:30px; text-align:center;'>🌟 Key Features</div>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Free & Borrow Access</div>
        <div class="feature-desc">
            Books can be accessed freely or borrowed for a limited period with proper return tracking.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Smart Search & Filters</div>
        <div class="feature-desc">
            Easily explore books using category, genre, and other helpful filters for faster discovery.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔐</div>
        <div class="feature-title">Secure Login System</div>
        <div class="feature-desc">
            A simple and organized login and signup system for both users and admin.
        </div>
    </div>
    """, unsafe_allow_html=True)

f4, f5, f6 = st.columns(3)
with f4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📦</div>
        <div class="feature-title">Request Tracking</div>
        <div class="feature-desc">
            Users can follow the request process from approval to delivery in a transparent way.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">↩️</div>
        <div class="feature-title">Borrow & Return Tracking</div>
        <div class="feature-desc">
            Borrowed books include return status and due-date tracking for a more organized circulation system.
        </div>
    </div>
    """, unsafe_allow_html=True)
with f6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🛠️</div>
        <div class="feature-title">Admin Dashboard</div>
        <div class="feature-desc">
            Admin can manage dispatch, delivery, return confirmation, courier payment verification, and analytics.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- HOW IT WORKS ---
st.markdown("""
<div class="step-card">
    <div class="step-title">Step 1: Donors Upload Books</div>
    <div class="step-desc">Books are added with category, genre, type, delivery option, and images for better organization.</div>
</div>

<div class="step-card">
    <div class="step-title">Step 2: Users Explore and Request</div>
    <div class="step-desc">Learners browse the available collection and request the books they need.</div>
</div>

<div class="step-card">
    <div class="step-title">Step 3: Auto Approval & Courier Payment</div>
    <div class="step-desc">Requests are auto-approved, and courier payment is required only when courier delivery is selected.</div>
</div>

<div class="step-card">
    <div class="step-title">Step 4: Dispatch and Delivery</div>
    <div class="step-desc">Admin manages dispatch and delivery so users can track the complete request flow.</div>
</div>

<div class="step-card">
    <div class="step-title">Step 5: Borrow Return Tracking</div>
    <div class="step-desc">If a book is borrowed, the system tracks return date, overdue status, and return confirmation.</div>
</div>
""", unsafe_allow_html=True)

# --- CTA SECTION ---
st.markdown("""
<div class="cta-box">
    <div class="cta-title">Start Your Book Sharing Journey Today</div>
    <div class="cta-text">
        Join BookHub to donate books, request learning resources, and make knowledge more accessible.
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("🚀 Get Started", key="get_started_btn", use_container_width=True):
        st.switch_page("pages/login.py")

# --- FOOTER ---
st.markdown(
    "<div class='footer'>© 2026 BookHub | Empowering Learning Through Sharing</div>",
    unsafe_allow_html=True
)

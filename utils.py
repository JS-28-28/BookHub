import streamlit as st
import base64


def logout_button():

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.clear()

        st.switch_page("Home.py")

        
def show_logo_and_title():
    """Displays the BookHub logo and title side-by-side in a professional, centered layout."""

    # Read and encode logo image
    with open("logo.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    # Render logo + title in a flexbox container
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    ">
        <img src="data:image/png;base64,{encoded}" 
             alt="BookHub Logo"
             style="width: 250px; height: auto; border-radius: 10px;">
        <div style="text-align: left;">
            <h1 style="
                font-size: 4rem; 
                font-weight: 800; 
                color: #0d1b5e;  /* Original deep blue */
                margin: 0;
            ">
                Welcome to the BookHub
            </h1>
            <p style="
                font-size: 1.35rem; 
                color: #333; 
                margin: 0.3rem 0 0;
                font-style: italic;
            ">
                A platform to donate, share, and spread knowledge freely.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
def show_top_profile():
    if "user" in st.session_state:
        username = st.session_state["user"]["username"]
        role = st.session_state["user"]["role"]

        st.markdown(
            f"""
            <div  style="
                display:flex;
                justify-content:flex-end;
                align-items:center;
                margin-top:-10px;
                margin-bottom:10px;
            ">
                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    background:#ffffff;
                    padding:8px 14px;
                    border-radius:12px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.1);
                ">
                    <div style="
                        width:36px;
                        height:36px;
                        border-radius:50%;
                        background:#2563EB;
                        color:white;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-weight:bold;
                        font-size:16px;
                    ">
                        {username[0].upper()}
                    </div>
                    <div style="line-height:1.2;">
                        <div style="font-weight:600; color:#111827;">{username}</div>
                        <div style="font-size:12px; color:#6B7280;">{role.capitalize()}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
import streamlit as st
from db_connection import get_connection
import pandas as pd
from utils import logout_button,show_top_profile

st.set_page_config(page_title="Donors List", page_icon="🧑‍🤝‍🧑", layout="wide")
show_top_profile()

logout_button()



# Apply common CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")





if 'user' not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()




st.title("📋 Donors List")

# Fetch donors
conn = get_connection()
df = pd.read_sql("SELECT donor_name, email, phone, donor_type FROM donations", conn)
conn.close()

st.dataframe(df)

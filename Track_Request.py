import streamlit as st
import pandas as pd
from db_connection import get_connection
from utils import logout_button, show_top_profile
import uuid

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Track Requests", page_icon="📦", layout="wide")
show_top_profile()

# ---------------- CSS ----------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ---------------- LOGIN CHECK ----------------
if "user" not in st.session_state:
    st.warning("Please login first")
    st.stop()

logout_button()

st.title("📦 Track Your Book Requests")
st.divider()

username = st.session_state['user']['username']

# ---------------- DB QUERY ----------------
conn = get_connection()

query = """
SELECT 
    r.id,
    d.book_title,
    d.author,
    d.book_type,
    d.price,
    d.security_deposit,
    r.request_date,
    r.status,
    r.delivery_status,
    r.delivery_date,
    r.payment_status,
    r.deposit_status,
    r.refund_status,
    r.transaction_id
FROM requests r
JOIN donations d ON r.book_id = d.id
WHERE r.username = %s
ORDER BY r.request_date DESC
"""

df = pd.read_sql(query, conn, params=(username,))
conn.close()

# ---------------- DISPLAY ----------------
if df.empty:
    st.info("You have not requested any books yet 📭")

else:
    for index, row in df.iterrows():
        with st.container(border=True):
            st.subheader(f"📘 {row['book_title']}")
            st.write(f"**Author:** {row['author']}")
            st.write(f"**Request Date:** {row['request_date']}")

            # -------- BOOK TYPE INFO --------
            if row["book_type"] == "Free":
                st.success("🟢 Free Book")
            elif row["book_type"] == "Paid":
                st.info(f"💰 Paid Book — ₹{float(row['price']):.2f}")
            elif row["book_type"] == "Deposit":
                st.warning(f"🔒 Security Deposit — ₹{float(row['security_deposit']):.2f}")

            # -------- REQUEST STATUS --------
            if row["status"] == "Approved":
                st.success("Status: Approved")
            elif row["status"] == "Rejected":
                st.error("Status: Rejected")
            else:
                st.warning("Status: Pending Approval")

            # -------- PAYMENT / DEPOSIT --------
            if row["book_type"] == "Paid":
                st.write(f"**Payment Status:** {row['payment_status']}")
            elif row["book_type"] == "Deposit":
                st.write(f"**Deposit Status:** {row['deposit_status']}")
                st.write(f"**Refund Status:** {row['refund_status']}")

            if pd.notna(row["transaction_id"]) and row["transaction_id"]:
                st.write(f"**Transaction ID:** {row['transaction_id']}")

            # -------- USER PAYMENT BUTTONS --------
            if row["status"] == "Approved":
                if row["book_type"] == "Paid" and row["payment_status"] == "Pending":
                    if st.button(f"Pay ₹{float(row['price']):.2f}", key=f"pay_{row['id']}"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        txn_id = "TXN" + str(uuid.uuid4()).replace("-", "")[:10].upper()

                        cursor.execute(
                            """
                            UPDATE requests
                            SET payment_status = 'Paid', transaction_id = %s
                            WHERE id = %s
                            """,
                            (txn_id, row["id"])
                        )

                        conn.commit()
                        conn.close()
                        st.success("Payment completed successfully!")
                        st.rerun()

                elif row["book_type"] == "Deposit" and row["deposit_status"] == "Pending":
                    if st.button(f"Pay Deposit ₹{float(row['security_deposit']):.2f}", key=f"deposit_{row['id']}"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        txn_id = "TXN" + str(uuid.uuid4()).replace("-", "")[:10].upper()

                        cursor.execute(
                            """
                            UPDATE requests
                            SET deposit_status = 'Paid', transaction_id = %s
                            WHERE id = %s
                            """,
                            (txn_id, row["id"])
                        )

                        conn.commit()
                        conn.close()
                        st.success("Security deposit paid successfully!")
                        st.rerun()

            # -------- DELIVERY --------
            if row["delivery_status"] == "Delivered":
                st.success(f"Delivered on {row['delivery_date']}")
            elif row["delivery_status"] == "Dispatched":
                st.info("Book Dispatched 🚚")
            else:
                st.warning("Waiting for Dispatch")

            # -------- PROGRESS BAR --------
            progress = 10

            if row["status"] == "Approved":
                progress = 30

            if row["book_type"] == "Paid" and row["payment_status"] == "Paid":
                progress = 50

            if row["book_type"] == "Deposit" and row["deposit_status"] == "Paid":
                progress = 50

            if row["delivery_status"] == "Dispatched":
                progress = 75

            if row["delivery_status"] == "Delivered":
                progress = 100

            st.progress(progress)
            st.divider()
import streamlit as st
import pandas as pd
from datetime import date
from db_connection import get_connection
from utils import logout_button, show_top_profile
from payment_utils import generate_upi_link, generate_qr_image, UPI_ID
import os

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
COURIER_CHARGE = 50

os.makedirs("payment_screenshots", exist_ok=True)

# ---------------- DB QUERY ----------------
conn = get_connection()

query = """
SELECT 
    r.id,
    d.book_title,
    d.author,
    d.book_type,
    d.delivery_method,
    r.request_date,
    r.status,
    r.delivery_status,
    r.delivery_date,
    r.payment_status,
    r.payment_proof,
    r.return_status,
    r.return_date
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
            st.write(f"**Delivery Method:** {row['delivery_method']}")

            # -------- BOOK TYPE INFO --------
            if row["book_type"] == "Free":
                st.success("🟢 Free Book")
            elif row["book_type"] == "Borrow":
                st.info("📘 Borrow Book")

            # -------- REQUEST STATUS --------
            if row["status"] == "Approved":
                st.success("Status: Approved")
            elif row["status"] == "Rejected":
                st.error("Status: Rejected")
            else:
                st.warning("Status: Pending Approval")

            # -------- COURIER PAYMENT INFO --------
            if row["delivery_method"] == "Courier":
                st.write(f"**Courier Charge:** ₹{COURIER_CHARGE}")
                st.write(f"**Payment Status:** {row['payment_status']}")

            # -------- BORROW INFO --------
            # -------- BORROW INFO --------
            if row["book_type"] == "Borrow":
               st.write(f"**Return Status:** {row['return_status']}")
               if pd.notna(row["return_date"]):
                    st.write(f"**Return Date:** {row['return_date']}")

                    # Overdue warning
                    if row["return_status"] != "Returned":
                         today = date.today()
                         return_dt = pd.to_datetime(row["return_date"]).date()

                         if today > return_dt:
                            overdue_days = (today - return_dt).days
                            st.error(f"⏰ Overdue by {overdue_days} day(s)")

            # -------- COURIER PAYMENT SECTION --------
            if row["status"] == "Approved" and row["delivery_method"] == "Courier":
                payment_status = str(row["payment_status"]).strip()

                if payment_status in ["Pending", "Not Paid", "None", "nan"]:
                    upi_link = generate_upi_link(COURIER_CHARGE)
                    qr_img = generate_qr_image(upi_link)

                    st.markdown("### 🚚 Courier Payment")

                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.image(qr_img, caption="Scan with any UPI app", width=200)

                    with col2:
                        st.write(f"**Courier Charge:** ₹{COURIER_CHARGE}")
                        st.write(f"**UPI ID:** {UPI_ID}")
                        st.code(upi_link, language="text")
                        st.markdown("""
**How to pay**
1. Scan the QR code using any UPI app  
2. Complete the payment  
3. Take screenshot of payment success  
4. Upload it below and click confirm
                        """)

                    screenshot = st.file_uploader(
                        f"Upload courier payment screenshot for Request ID {row['id']}",
                        type=["png", "jpg", "jpeg"],
                        key=f"courier_upload_{row['id']}"
                    )

                    if screenshot is not None:
                        st.image(screenshot, caption="Uploaded Screenshot", width=250)

                    if st.button(f"✅ I Have Paid ₹{COURIER_CHARGE}", key=f"pay_btn_{row['id']}"):
                        if screenshot is None:
                            st.warning("Please upload payment screenshot first.")
                        else:
                            file_path = f"payment_screenshots/courier_{row['id']}_{screenshot.name}"
                            with open(file_path, "wb") as f:
                                f.write(screenshot.getbuffer())

                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                """
                                UPDATE requests
                                SET payment_status = %s,
                                    payment_proof = %s
                                WHERE id = %s
                                """,
                                ("Pending Verification", file_path, row["id"])
                            )
                            conn.commit()
                            conn.close()

                            st.success("Courier payment proof uploaded successfully. Waiting for admin verification.")
                            st.rerun()

                elif payment_status == "Pending Verification":
                    st.info("Courier payment uploaded. Waiting for admin verification.")
                elif payment_status == "Paid":
                    st.success("Courier payment verified successfully.")

            # -------- DELIVERY --------
            if row["delivery_status"] == "Delivered":
                st.success(f"Delivered on {row['delivery_date']}")
            elif row["delivery_status"] == "Dispatched":
                st.info("Book Dispatched 🚚")
            else:
                st.warning("Waiting for Dispatch")

            # -------- RETURN BOOK OPTION (ONLY FOR BORROW BOOKS) --------
            if row["book_type"] == "Borrow" and row["delivery_status"] == "Delivered":
                if row["return_status"] == "Not Returned":
                    if st.button(f"↩️ Return Book", key=f"return_{row['id']}"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            """
                            UPDATE requests
                            SET return_status = 'Return Requested'
                            WHERE id = %s
                            """,
                            (row["id"],)
                        )
                        conn.commit()
                        conn.close()
                        st.success("Return request sent to admin.")
                        st.rerun()

                elif row["return_status"] == "Return Requested":
                    st.info("Return request sent. Waiting for admin confirmation.")

                elif row["return_status"] == "Returned":
                    st.success("Book return confirmed by admin.")

            # -------- PROGRESS BAR --------
            progress = 10

            if row["status"] == "Approved":
                progress = 30

            if row["delivery_method"] == "Courier" and str(row["payment_status"]).strip() == "Pending Verification":
                progress = 45

            if row["delivery_method"] == "Courier" and str(row["payment_status"]).strip() == "Paid":
                progress = 55

            if row["delivery_status"] == "Dispatched":
                progress = 75

            if row["delivery_status"] == "Delivered":
                progress = 90

            if row["book_type"] == "Borrow" and row["return_status"] == "Returned":
                progress = 100
            elif row["delivery_status"] == "Delivered" and row["book_type"] == "Free":
                progress = 100

            st.progress(progress)
            st.divider()

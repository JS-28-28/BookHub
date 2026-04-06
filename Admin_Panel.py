import streamlit as st
from db_connection import get_connection
import pandas as pd
from utils import logout_button
import plotly.express as px

st.set_page_config(page_title="Admin Panel", page_icon="🛠", layout="wide")

logout_button()

# ---------------- CSS ----------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

st.title("🛠️ Admin Panel")

# ---------------- SESSION ----------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":
        st.session_state.admin_logged_in = True
        st.rerun()
    elif password != "":
        st.error("Wrong Password")

# ---------------- ADMIN DASHBOARD ----------------
if st.session_state.admin_logged_in:
    conn = get_connection()

    if conn is None:
        st.error("Database connection failed.")
        st.stop()

    # =========================================================
    # SYSTEM OVERVIEW
    # =========================================================
    st.subheader("📊 System Overview")

    total_users = pd.read_sql("SELECT COUNT(*) AS total FROM users", conn)
    total_books = pd.read_sql("SELECT COUNT(*) AS total FROM donations", conn)
    total_requests = pd.read_sql("SELECT COUNT(*) AS total FROM requests", conn)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", total_users["total"][0])
    col2.metric("Total Books", total_books["total"][0])
    col3.metric("Total Requests", total_requests["total"][0])

    st.divider()

    # =========================================================
    # ADMIN ANALYTICS
    # =========================================================
    st.subheader("📈 Admin Analytics")

    status_query = """
        SELECT status, COUNT(*) AS count
        FROM requests
        GROUP BY status
    """
    df_status = pd.read_sql(status_query, conn)

    delivery_query = """
        SELECT delivery_status, COUNT(*) AS count
        FROM requests
        GROUP BY delivery_status
    """
    df_delivery = pd.read_sql(delivery_query, conn)

    metric1, metric2, metric3, metric4, metric5 = st.columns(5)

    pending_count = df_status[df_status["status"] == "Pending"]["count"].sum() if not df_status.empty else 0
    approved_count = df_status[df_status["status"] == "Approved"]["count"].sum() if not df_status.empty else 0
    rejected_count = df_status[df_status["status"] == "Rejected"]["count"].sum() if not df_status.empty else 0
    dispatched_count = df_delivery[df_delivery["delivery_status"] == "Dispatched"]["count"].sum() if not df_delivery.empty else 0
    delivered_count = df_delivery[df_delivery["delivery_status"] == "Delivered"]["count"].sum() if not df_delivery.empty else 0

    metric1.metric("⏳ Pending", int(pending_count))
    metric2.metric("✅ Approved", int(approved_count))
    metric3.metric("❌ Rejected", int(rejected_count))
    metric4.metric("🚚 Dispatched", int(dispatched_count))
    metric5.metric("📦 Delivered", int(delivered_count))

    st.divider()

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("### Request Status Chart")
        if not df_status.empty:
            fig_status = px.pie(df_status, names="status", values="count", hole=0.4)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No request status data available.")

    with chart2:
        st.markdown("### Delivery Status Chart")
        if not df_delivery.empty:
            fig_delivery = px.pie(df_delivery, names="delivery_status", values="count", hole=0.4)
            st.plotly_chart(fig_delivery, use_container_width=True)
        else:
            st.info("No delivery status data available.")

    st.divider()

    # ---------------- PAYMENT ANALYTICS ----------------
    st.markdown("### 💳 Payment / Deposit Analytics")

    payment_query = """
        SELECT payment_status, COUNT(*) AS count
        FROM requests
        GROUP BY payment_status
    """
    deposit_query = """
        SELECT deposit_status, COUNT(*) AS count
        FROM requests
        GROUP BY deposit_status
    """
    refund_query = """
        SELECT refund_status, COUNT(*) AS count
        FROM requests
        GROUP BY refund_status
    """

    df_payment = pd.read_sql(payment_query, conn)
    df_deposit = pd.read_sql(deposit_query, conn)
    df_refund = pd.read_sql(refund_query, conn)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.write("**Payment Status**")
        st.dataframe(df_payment, use_container_width=True)
    with p2:
        st.write("**Deposit Status**")
        st.dataframe(df_deposit, use_container_width=True)
    with p3:
        st.write("**Refund Status**")
        st.dataframe(df_refund, use_container_width=True)

    st.divider()

    # =========================================================
    # REQUESTS SECTION
    # =========================================================
    st.subheader("📦 Book Requests")

    query_requests = """
        SELECT 
            r.id,
            r.username,
            r.book_id,
            r.request_date,
            r.status,
            r.delivery_status,
            r.payment_status,
            r.deposit_status,
            r.refund_status,
            r.transaction_id,
            d.book_title,
            d.author,
            d.book_type,
            d.price,
            d.security_deposit
        FROM requests r
        JOIN donations d ON r.book_id = d.id
        ORDER BY r.request_date DESC
    """

    df_requests = pd.read_sql(query_requests, conn)

    if df_requests.empty:
        st.info("No requests found")

    else:
        for index, row in df_requests.iterrows():
            with st.container(border=True):
                st.write(f"### Request ID: {row['id']}")
                st.write(f"**User:** {row['username']}")
                st.write(f"**Book:** {row['book_title']}")
                st.write(f"**Author:** {row['author']}")
                st.write(f"**Request Date:** {row['request_date']}")
                st.write(f"**Book Type:** {row['book_type']}")

                if row["book_type"] == "Paid":
                    st.write(f"**Price:** ₹{float(row['price']):.2f}")
                    st.write(f"**Payment Status:** {row['payment_status']}")

                elif row["book_type"] == "Deposit":
                    st.write(f"**Security Deposit:** ₹{float(row['security_deposit']):.2f}")
                    st.write(f"**Deposit Status:** {row['deposit_status']}")
                    st.write(f"**Refund Status:** {row['refund_status']}")

                else:
                    st.write("**Payment:** Not Required")

                if pd.notna(row["transaction_id"]) and row["transaction_id"]:
                    st.write(f"**Transaction ID:** {row['transaction_id']}")

                # ---------------- STATUS DISPLAY ----------------
                if row["status"] == "Approved":
                    st.success(f"Status: {row['status']}")
                elif row["status"] == "Rejected":
                    st.error(f"Status: {row['status']}")
                else:
                    st.warning(f"Status: {row['status']}")

                if row["delivery_status"] == "Delivered":
                    st.success(f"Delivery: {row['delivery_status']}")
                elif row["delivery_status"] == "Dispatched":
                    st.info(f"Delivery: {row['delivery_status']}")
                else:
                    st.warning(f"Delivery: {row['delivery_status']}")

                # =====================================================
                # CLEAN ACTION BUTTONS
                # =====================================================

                # 1. Pending request -> Approve / Reject
                if row["status"] == "Pending":
                    col1, col2 = st.columns(2)

                    if col1.button("Approve", key=f"approve_{row['id']}"):
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE requests SET status='Approved', approved_by='Admin' WHERE id=%s",
                            (row['id'],)
                        )
                        conn.commit()
                        st.success("Request Approved")
                        st.rerun()

                    if col2.button("Reject", key=f"reject_{row['id']}"):
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE requests SET status='Rejected' WHERE id=%s",
                            (row['id'],)
                        )
                        cursor.execute(
                            "UPDATE donations SET availability_status='Available' WHERE id=%s",
                            (row['book_id'],)
                        )
                        conn.commit()
                        st.warning("Request Rejected")
                        st.rerun()

                # 2. Approved but not dispatched yet
                elif row["status"] == "Approved" and row["delivery_status"] == "Not Dispatched":
                    allow_dispatch = False

                    if row["book_type"] == "Free":
                        allow_dispatch = True
                    elif row["book_type"] == "Paid" and row["payment_status"] == "Paid":
                        allow_dispatch = True
                    elif row["book_type"] == "Deposit" and row["deposit_status"] == "Paid":
                        allow_dispatch = True

                    if allow_dispatch:
                        if st.button("Dispatch", key=f"dispatch_{row['id']}"):
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE requests SET delivery_status='Dispatched' WHERE id=%s",
                                (row['id'],)
                            )
                            conn.commit()
                            st.success("Book Dispatched")
                            st.rerun()
                    else:
                        if row["book_type"] == "Paid":
                            st.info("Waiting for payment")
                        elif row["book_type"] == "Deposit":
                            st.info("Waiting for deposit payment")

                # 3. Dispatched -> Delivered
                elif row["delivery_status"] == "Dispatched":
                    if st.button("Delivered", key=f"deliver_{row['id']}"):
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE requests SET delivery_status='Delivered', delivery_date=CURDATE() WHERE id=%s",
                            (row['id'],)
                        )
                        conn.commit()
                        st.success("Book Delivered")
                        st.rerun()

                # 4. Delivered -> only Deposit case gets Refund / Forfeit
                elif row["delivery_status"] == "Delivered":
                    if row["book_type"] == "Deposit" and row["refund_status"] == "Pending":
                        col1, col2 = st.columns(2)

                        if col1.button("Refund", key=f"refund_{row['id']}"):
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE requests SET refund_status='Refunded' WHERE id=%s",
                                (row['id'],)
                            )
                            conn.commit()
                            st.success("Deposit Refunded")
                            st.rerun()

                        if col2.button("Forfeit Deposit", key=f"forfeit_{row['id']}"):
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE requests SET refund_status='Forfeited' WHERE id=%s",
                                (row['id'],)
                            )
                            conn.commit()
                            st.error("Deposit Forfeited")
                            st.rerun()
                    else:
                        st.success("No further action required")

                st.divider()

    conn.close()
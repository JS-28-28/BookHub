import streamlit as st
from db_connection import get_connection
import pandas as pd
from utils import logout_button, show_top_profile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Available Books", page_icon="📚", layout="wide")

show_top_profile()
# ---------------- APPLY CSS ----------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ---------------- LOGIN CHECK ----------------
if 'user' not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

logout_button()

# ---------------- TITLE ----------------
st.title("📖 Available Books")

# ---------------- FETCH DATA ----------------
conn = get_connection()

if conn is None:
    st.error("Database connection failed.")
    st.stop()

df = pd.read_sql(
    """
    SELECT id, book_title, author, category, genre, condition_status,
           donor_name, book_image, availability_status,
           book_type, price, security_deposit
    FROM donations
    WHERE availability_status = 'Available'
    """,
    conn
)

requested_df = pd.read_sql(
    """
    SELECT book_id
    FROM requests
    WHERE username = %s
    """,
    conn,
    params=(st.session_state['user']['username'],)
)

conn.close()

requested_book_ids = set(requested_df["book_id"].tolist()) if not requested_df.empty else set()

# ---------------- CLEAN DATA ----------------
if df.empty:
    st.info("No books available right now.")
    st.stop()

df["category"] = df["category"].fillna("Others").astype(str).str.strip()
df["genre"] = df["genre"].fillna("General").astype(str).str.strip()
df["book_title"] = df["book_title"].fillna("").astype(str)
df["author"] = df["author"].fillna("Unknown").astype(str)
df["condition_status"] = df["condition_status"].fillna("Not Specified").astype(str)
df["book_type"] = df["book_type"].fillna("Free").astype(str).str.strip()
df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
df["security_deposit"] = pd.to_numeric(df["security_deposit"], errors="coerce").fillna(0)

# ---------------- FILTER SECTION ----------------
st.subheader("🔍 Search and Filter Books")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    search_text = st.text_input("Search by Book Title")

with col2:
    category_options = ["All", "Academic", "Competitive", "Technical", "Others"]
    selected_category = st.selectbox("Category", category_options)

with col3:
    if selected_category == "Academic":
        genre_options = ["All", "Physics", "Chemistry", "Mathematics", "Biology"]
    elif selected_category == "Competitive":
        genre_options = ["All", "UPSC", "CGPSC", "JEE", "NEET", "SSC", "Banking"]
    elif selected_category == "Technical":
        genre_options = ["All", "Computer Science", "Computer Science & Applications", "IT", "Electronics"]
    elif selected_category == "Others":
        genre_options = ["All", "General"]
    else:
        genre_options = ["All"] + sorted(
            [g for g in df["genre"].dropna().unique().tolist() if g and str(g).lower() != "none"]
        )

    selected_genre = st.selectbox("Genre", genre_options)

with col4:
    selected_book_type = st.selectbox("Book Type", ["All", "Free", "Paid", "Deposit"])

with col5:
    sort_option = st.selectbox("Sort By", ["Newest", "Title A-Z"])

# ---------------- AUTO FILTER ----------------
filtered_df = df.copy()

if search_text:
    filtered_df = filtered_df[
        filtered_df["book_title"].str.contains(search_text, case=False, na=False)
    ]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["genre"] == selected_genre]

if selected_book_type != "All":
    filtered_df = filtered_df[filtered_df["book_type"] == selected_book_type]

if sort_option == "Title A-Z":
    filtered_df = filtered_df.sort_values("book_title")
else:
    filtered_df = filtered_df.sort_values("id", ascending=False)

st.markdown("---")

# ---------------- GRID DISPLAY ----------------
if filtered_df.empty:
    st.warning("No books match your search/filter.")
else:
    cols = st.columns(3)

    for i, row in filtered_df.iterrows():
        with cols[i % 3]:
            with st.container(border=True):

                if pd.notna(row["book_image"]) and str(row["book_image"]).strip() != "":
                    image_path = row["book_image"]
                    if os.path.exists(image_path):
                        st.image(image_path, width=150)
                    else:
                        st.info("No Image")
                else:
                    st.info("No Image")

                st.subheader(row["book_title"])
                st.write(f"👤 {row['author']}")

                category = row["category"] if row["category"] and row["category"].lower() != "none" else "Others"
                genre = row["genre"] if row["genre"] and row["genre"].lower() != "none" else "General"

                st.write(f"🏷 {category} | {genre}")
                st.write(f"⭐ {row['condition_status']}")
                st.write(f"🙍 Donor: {row['donor_name']}")

                # -------- BOOK TYPE DISPLAY --------
                if row["book_type"] == "Free":
                    st.success("🟢 Free Book")
                elif row["book_type"] == "Paid":
                    st.info(f"💰 Paid Book — ₹{row['price']:.2f}")
                elif row["book_type"] == "Deposit":
                    st.warning(f"🔒 Security Deposit — ₹{row['security_deposit']:.2f} (Refundable)")

                if row["availability_status"] == "Available":
                    st.success("📘 Available")
                else:
                    st.error("Not Available")

                if row["id"] in requested_book_ids:
                    st.info("✅ Already Requested")
                else:
                    st.checkbox("Select", key=f"book_{row['id']}")

    st.markdown("---")

    # ---------------- REQUEST BUTTON ----------------
    if st.button("Request Selected Books"):
        selected_books = []

        for book_id in filtered_df["id"].tolist():
            if st.session_state.get(f"book_{book_id}", False):
                selected_books.append(book_id)

        if selected_books:
            conn = get_connection()

            if conn is None:
                st.error("Database connection failed.")
                st.stop()

            cursor = conn.cursor()
            new_requests = 0
            skipped_requests = 0

            for book_id in selected_books:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM requests
                    WHERE username = %s AND book_id = %s
                    """,
                    (st.session_state['user']['username'], book_id)
                )
                already_requested = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT availability_status, book_type
                    FROM donations
                    WHERE id = %s
                    """,
                    (book_id,)
                )
                result = cursor.fetchone()

                if already_requested > 0:
                    skipped_requests += 1
                    continue

                if result is None or result[0] != "Available":
                    skipped_requests += 1
                    continue

                book_type = result[1]

                payment_status = "Not Required"
                deposit_status = "Not Required"
                refund_status = "Not Applicable"

                if book_type == "Paid":
                    payment_status = "Pending"

                elif book_type == "Deposit":
                    deposit_status = "Pending"
                    refund_status = "Pending"

                cursor.execute(
                    """
                    INSERT INTO requests
                    (username, book_id, payment_status, deposit_status, refund_status)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        st.session_state['user']['username'],
                        book_id,
                        payment_status,
                        deposit_status,
                        refund_status
                    )
                )

                cursor.execute(
                    """
                    UPDATE donations
                    SET availability_status = 'Requested'
                    WHERE id = %s
                    """,
                    (book_id,)
                )

                new_requests += 1

            conn.commit()
            conn.close()

            if new_requests > 0:
                st.success(f"{new_requests} request(s) submitted successfully!")

            if skipped_requests > 0:
                st.warning(f"{skipped_requests} skipped (already requested/unavailable)")

            st.rerun()

        else:
            st.warning("Please select at least one book.")
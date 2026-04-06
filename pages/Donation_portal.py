import streamlit as st
import mysql.connector
from datetime import date
from utils import logout_button, show_top_profile
import os

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Book Donation Portal", layout="wide")

show_top_profile()
logout_button()

# ---------- CSS ----------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ---------- LOGIN CHECK ----------
if 'user' not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

# ---------- DB CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="book"
    )

# ---------- PAGE WRAPPER ----------
st.markdown("""
<div class="page-form-container">
    <h1 class="page-title">📚 Book Donation Portal</h1>
    <p class="page-subtitle">Donate your books and help others learn!</p>
</div>
""", unsafe_allow_html=True)

# ---------- DONOR INFO ----------
st.markdown('<div class="page-form-container">', unsafe_allow_html=True)

st.subheader("Donor Information")
donor_name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
donor_type = st.selectbox("Donor Type", ["Student", "Faculty", "Businessman", "Other"])

# ---------- BOOKS ----------
st.subheader("Books Information")

num_books = st.number_input(
    "How many books do you want to donate?",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

books = []

for i in range(num_books):
    st.markdown(f"### Book {i+1} Details")

    book_title = st.text_input(f"Book Title {i+1}", key=f"title_{i}")
    author = st.text_input(f"Author Name {i+1}", key=f"author_{i}")

    category = st.selectbox(
        f"Select Category {i+1}",
        ["Academic", "Competitive", "Technical", "Others"],
        key=f"category_{i}"
    )

    if category == "Academic":
        genre = st.selectbox(
            f"Select Genre {i+1}",
            ["Physics", "Chemistry", "Mathematics", "Biology"],
            key=f"genre_{i}_{category}"
        )
    elif category == "Competitive":
        genre = st.selectbox(
            f"Select Genre {i+1}",
            ["UPSC", "CGPSC", "JEE", "NEET", "SSC", "Banking"],
            key=f"genre_{i}_{category}"
        )
    elif category == "Technical":
        genre = st.selectbox(
            f"Select Genre {i+1}",
            ["Computer Science & Applications", "IT", "Electronics"],
            key=f"genre_{i}_{category}"
        )
    else:
        genre = st.text_input(
            f"Enter Genre {i+1}",
            key=f"genre_{i}_{category}"
        )

    condition_status = st.selectbox(
        f"Book Condition {i+1}",
        ["New", "Used - Good", "Used - Average"],
        key=f"condition_{i}"
    )

    book_type = st.selectbox(
        f"Book Type {i+1}",
        ["Free", "Paid", "Deposit"],
        key=f"book_type_{i}"
    )

    price = 0.0
    security_deposit = 0.0

    if book_type == "Paid":
        price = st.number_input(
            f"Enter Price for Book {i+1} (₹)",
            min_value=0.0,
            step=10.0,
            key=f"price_{i}"
        )

    elif book_type == "Deposit":
        security_deposit = st.number_input(
            f"Enter Security Deposit for Book {i+1} (₹)",
            min_value=0.0,
            step=10.0,
            key=f"deposit_{i}"
        )

    book_image = st.file_uploader(
        f"Upload Image of Book {i+1}",
        type=["png", "jpg", "jpeg"],
        key=f"image_{i}"
    )

    books.append((
        book_title,
        author,
        category,
        genre,
        condition_status,
        book_type,
        price,
        security_deposit,
        book_image
    ))

# ---------- DATE ----------
donation_date = st.date_input("Donation Date", value=date.today())

# ---------- SUBMIT BUTTON ----------
submitted = st.button("📤 Submit Donation")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- INSERT ----------
if submitted:
    if donor_name and all([b[0] for b in books]):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            os.makedirs("book_images", exist_ok=True)

            for book in books:
                (
                    book_title,
                    author,
                    category,
                    genre,
                    condition_status,
                    book_type,
                    price,
                    security_deposit,
                    book_image
                ) = book

                if book_type == "Paid" and price <= 0:
                    st.warning(f"Please enter valid price for '{book_title}'.")
                    st.stop()

                if book_type == "Deposit" and security_deposit <= 0:
                    st.warning(f"Please enter valid security deposit for '{book_title}'.")
                    st.stop()

                img_path = None
                if book_image:
                    img_path = f"book_images/{book_image.name}"
                    with open(img_path, "wb") as f:
                        f.write(book_image.getbuffer())

                query = """
                    INSERT INTO donations
                    (
                        donor_name, email, phone, donor_type,
                        book_title, author, category, genre,
                        condition_status, donation_date, book_image,
                        availability_status, book_type, price, security_deposit
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    donor_name,
                    email,
                    phone,
                    donor_type,
                    book_title,
                    author,
                    category,
                    genre,
                    condition_status,
                    donation_date,
                    img_path,
                    "Available",
                    book_type,
                    price,
                    security_deposit
                )

                cursor.execute(query, values)

            conn.commit()
            conn.close()

            st.success("✅ Donation submitted successfully!")

        except Exception as e:
            st.error(f"Database Error: {e}")
    else:
        st.warning("Please fill in donor name and all book titles.")

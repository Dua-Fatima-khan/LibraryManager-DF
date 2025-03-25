import streamlit as st
import json


st.set_page_config(
    page_title="BookVaultX",
    page_icon=":💡",
    layout="wide",
)
# File Handling Functions
def load_library(username):
    """Load the user's personal library from a file."""
    try:
        with open(f"library_{username}.txt", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library(username, library):
    """Save the user's personal library to a file."""
    with open(f"library_{username}.txt", "w") as file:
        json.dump(library, file)

# User Authentication (Simple Username Input)
st.sidebar.header("User Login")
username = st.sidebar.text_input("Enter your username", value="guest")

# Load library for the specific user
library = load_library(username)

# Streamlit UI
st.title("BookVaultX 💡")

# Sidebar Navigation
menu = st.sidebar.radio("Select an option", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"])

# Add Book
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as Read")
    
    if st.button("Add Book"):
        if title and author and year and genre:
            book = {"title": title, "author": author, "year": year, "genre": genre, "read": read_status}
            library.append(book)
            save_library(username, library)
            st.success("✅ Book added successfully!")
        else:
            st.error("❌ Please fill all fields!")

# Remove Book
elif menu == "Remove Book":
    st.subheader("🗑 Remove a Book")
    titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", titles)
    
    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(username, library)
        st.success("✅ Book removed successfully!")

# Search Book
elif menu == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter Title or Author")
    if search_query:
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                status = "Read" if book["read"] else "Unread"
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning("❌ No matching books found!")

# Display All Books
elif menu == "Display All Books":
    st.subheader("📋 Your Library")
    if library:
        for book in library:
            status = "Read" if book["read"] else "Unread"
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.warning("❌ No books in the library!")

# Statistics
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"📚 Total Books: {total_books}")
    st.write(f"✅ Books Read: {read_books}")
    st.write(f"📖 Percentage Read: {percentage_read:.2f}%")

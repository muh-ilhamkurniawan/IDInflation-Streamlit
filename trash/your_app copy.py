import streamlit as st

# Membuat fungsi utama untuk navigasi
st.set_page_config(layout="wide")

def main():
    st.title("Navigasi Horizontal dengan Tombol Full Width di Streamlit")

    # Menyusun tombol navigasi dalam tiga kolom yang berjejer secara horizontal
    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        if st.button("Home", use_container_width=True):
            st.session_state["page"] = "Home"

    with col2:
        if st.button("Page 1", use_container_width=True):
            st.session_state["page"] = "Page 1"

    with col3:
        if st.button("Page 2", use_container_width=True):
            st.session_state["page"] = "Page 2"

    # Menampilkan konten berdasarkan pilihan
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        show_home()
    elif st.session_state["page"] == "Page 1":
        show_page1()
    elif st.session_state["page"] == "Page 2":
        show_page2()

# Fungsi untuk menampilkan halaman
def show_home():
    st.header("Selamat Datang di Home")
    st.write("Ini adalah halaman utama.")

def show_page1():
    st.header("Ini adalah Page 1")
    st.write("Konten untuk halaman 1 ditampilkan di sini.")

def show_page2():
    st.header("Ini adalah Page 2")
    st.write("Konten untuk halaman 2 ditampilkan di sini.")

if __name__ == "__main__":
    main()

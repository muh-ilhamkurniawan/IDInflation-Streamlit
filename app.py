import streamlit as st

# Membuat fungsi utama untuk navigasi
st.set_page_config(layout="wide")

def main():
    st.title("Visualization of Indonesian Inflation Data")

    # Menyusun tombol navigasi dalam tiga kolom yang berjejer secara horizontal
    col1, col2, col3 = st.columns([2,1,1])

    with col2:
        if st.button("Home", use_container_width=True):
            st.session_state["page"] = "Home"

    with col3:
        if st.button("Comparison of Methods", use_container_width=True):
            st.session_state["page"] = "Page 1"

    # Menampilkan konten berdasarkan pilihan
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        show_home()
    elif st.session_state["page"] == "Page 1":
        show_page1()

# Fungsi untuk menampilkan halaman
def show_home():
    st.header("Selamat Datang di Home")
    st.write("Ini adalah halaman utama.")

def show_page1():
    st.header("Ini adalah Page 1")
    st.write("Konten untuk halaman 1 ditampilkan di sini.")


if __name__ == "__main__":
    main()

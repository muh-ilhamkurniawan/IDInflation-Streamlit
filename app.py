import streamlit as st
from home import show_home
from testing import show_testing

# Set the page configuration for the Streamlit app
st.set_page_config(layout="wide")

def main():
    # Set the title of the Streamlit app
    st.title('DASHBOARD - IDInflation')
    # st.header('Indonesia Inflation Data ')

    # Menyusun tombol navigasi dalam tiga kolom yang berjejer secara horizontal
    col1, col2, col3,col4 = st.columns([4,1,1,1])

    with col2:
        if st.button("Home", use_container_width=True):
            st.session_state["page"] = "Home"

    with col3:
        if st.button("Methods", use_container_width=True):
            st.session_state["page"] = "Methods"
    
    with col4:
        if st.button("About", use_container_width=True):
            st.session_state["page"] = "Page 1"

    # Menampilkan konten berdasarkan pilihan
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        show_home()
    elif st.session_state["page"] == "Methods":
        show_testing()

if __name__ == "__main__":
    main()

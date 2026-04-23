import stack
import streamlit as st

# Membuat visualisasi stack dengan streamlit
st.set_page_config(page_title="📊Stack Visualization", layout="wide")
# Judul Aplikasi
st.title("Stack Visualizer")
def display_stack():
    temp = st.session_state.stack.head
    while temp:
        st.write(temp.data)
        temp = temp.next
    st.write("None")
# Inisialisasi Stack
if 'stack' not in st.session_state:
    st.session_state.stack = stack.Stack()

# Input Data
with st.form("input_form"):
    data = st.text_input("Masukkan Data")
    submit = st.form_submit_button("Tambah ke Stack")

    if submit and data:
        st.session_state.stack.push(data)
        st.rerun()


# Tampilkan Stack
st.subheader("Stack Visualization")
# Tombol Pop
if st.button("Pop"):
    st.session_state.stack.pop()
    st.rerun()

# Tampilan Stack Teratas
st.subheader("Stack Teratas")
st.write(st.session_state.stack.peek())

# Tampilan Apakah Stack Kosong
st.subheader("Apakah Stack Kosong?")
st.write(st.session_state.stack.is_empty())

# Menampilkan seluruh isi stack
st.subheader("Seluruh Isi Stack")
st.write(display_stack())
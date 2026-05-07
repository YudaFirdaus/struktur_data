# Visualisasi Antrian di RS dengan GTTS untuk pemanggilan Antrian

import queue2
from gtts import gTTS
import streamlit as st

# Title
st.title("Visualisasi Antrian di RS dengan GTTS dan Streamlit")
# Membuat function audio output


# Inisialisasi session Antrian
if 'queue2' not in st.session_state:
    st.session_state.queue2 = queue2.Queue()
    st.session_state.counter = 1

# Halaman Depan
st.header("Halaman Depan")
Pasien = st.text_input("Masukkan Nama Pasien")
if st.button("Tambah Pasien"):
    st.session_state.queue2.enqueue(Pasien)
    st.session_state.counter += 1  

# Menampilkan Antrian
st.header("Antrian Saat Ini")

if not st.session_state.queue2.is_empty():
    st.write(f"Jumlah Antrian: {st.session_state.queue2.size}")
    # Menampilkan seluruh Antrian
    st.subheader("Menampilkan seluruh Antrian")
    current=st.session_state.queue2.head
    no = 1
    while current:
        st.write(f"Antrian {no}: {current.data}")
        no += 1
        current=current.next

if st.button("Panggil Pasien Berikutnya"):
    if not st.session_state.queue2.is_empty():
        nama_pasien = st.session_state.queue2.head.data
        tts = gTTS(f"Pasien atas nama {nama_pasien}, Silahkan Menuju Ruang Dokter", lang='id')
        tts.save("audio.mp3")
        st.audio("audio.mp3", autoplay=True)
        st.session_state.queue2.dequeue()
    else:
        st.warning("Antrian Kosong")
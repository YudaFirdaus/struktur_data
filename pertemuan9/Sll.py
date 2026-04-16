import streamlit as st

# Setup Page
st.set_page_config(page_title="UINSSC Beats", layout="wide")
st.title("🎵 UINSSC Beats: Industry Linked List Simulation")

# Inisialisasi Session State
if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()
    # Default Songs
    st.session_state.playlist.add_song("Bohemian Rhapsody", "Queen")
    st.session_state.playlist.add_song("Lathi", "Weird Genius")

# --- UI LAYOUT ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📻 Now Playing")
    curr = st.session_state.playlist.current
    
    if curr:
        st.info(f"### {curr.title}\n**Artist:** {curr.artist}")
        
        # Tombol Navigasi
        btn_prev, btn_del, btn_next = st.columns(3)
        with btn_prev:
            if st.button("⏮️ Previous"):
                st.session_state.playlist.current = curr.prev
                st.rerun()
        with btn_del:
            if st.button("🗑️ Delete Song"):
                st.session_state.playlist.delete_current()
                st.rerun()
        with btn_next:
            if st.button("Next ⏭️"):
                st.session_state.playlist.current = curr.next
                st.rerun()
    else:
        st.warning("Playlist is Empty. Please add some songs.")

with col2:
    st.subheader("➕ Add New Song")
    t = st.text_input("Song Title")
    a = st.text_input("Artist Name")
    if st.button("Insert to Playlist"):
        st.session_state.playlist.add_song(t, a)
        st.success(f"Added {t} to the chain!")
        st.rerun()

# --- VISUALISASI STRUKTUR DATA (MEMORI) ---
st.markdown("---")
st.subheader("🧠 Memory Structure Visualization")
if st.session_state.playlist.head:
    nodes = []
    temp = st.session_state.playlist.head
    while True:
        is_active = "👉" if temp == st.session_state.playlist.current else ""
        nodes.append(f"{is_active} **[{temp.title}]**")
        temp = temp.next
        if temp == st.session_state.playlist.head: break
    
    # Menampilkan alur Circular
    st.write(" ↔️ ".join(nodes) + " ↔️ (Back to Head)")

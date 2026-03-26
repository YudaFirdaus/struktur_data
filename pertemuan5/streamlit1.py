import streamlit as st

st.title("Aplikasi Dictionary")
st.subheader("Hitung kata dalam Paragraf")

textInput = st.text_area("Masukkan Paragraf", height = 200)

if st.button("Hitung Analisis"):
    words = textInput.lower().split()
    count = {}
    
    for word in words:
        count[word] = count.get(word, 0) + 1

    st.subheader("Hasil Analisis")
    st.write(count)
    st.bar_chart(count)
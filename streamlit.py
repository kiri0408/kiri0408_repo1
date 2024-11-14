import streamlit as st

st.title('My First Streamlit App')

name = st.text_input('あなたの名前を入力してください')
if name:
    st.write(f'こんにちは、{name}さん!')

age = st.slider('あなたの年齢は?', 0, 100, 25)
st.write(f'あなたは{age}歳です。')

if st.button('Click me!'):
    st.balloons()
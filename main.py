import streamlit as st
st.title('私の最初のウェブサイトを作る!')
a=st.text_input('名前は何ですか')
b=st.selectbox('好きな食べ物を選択してください!',['이차현이먹고남긴 쓰레기음식','이차현이 만든 냄새나는음식'])
if st.button('인사말 생성'):
  st.info(a+'님,안녕하세요! 반갑습니다!')
  st.warning(b+'를 좋아하냐 취향꼬라지')
  st.error('어쩌라고')
  st.balloons()

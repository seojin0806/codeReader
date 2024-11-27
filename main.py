import streamlit as st
from langchain_community.llms import OpenAI

# OpenAI API 사용을 위한 LLM 초기화
llm = OpenAI(
    temperature=0.2,
    openai_api_key="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"
)

#수정확인
print("헬로!")

# Streamlit UI
st.title("Code Analysis Tool")
code_input = st.text_area("Enter your code here:")

#아니지... 그냥 코드 어날리스트 하면 될듯?

if st.button("Analyze Code"):
    # LLM을 사용하여 코드 분석
    analysis = llm(f"Analyze the following code:\n\n{code_input}")
    st.write("### Code Analysis:")
    st.write(analysis)

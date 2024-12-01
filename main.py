import ast
import os
import streamlit as st
from graphviz import Digraph
from langchain_openai import OpenAI

# LangChain 설정
llm = OpenAI(
    temperature=0.2,  # 안정적인 응답을 위해 낮은 온도 설정
    openai_api_key="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"  # 유효한 OpenAI API 키 입력
)

# Streamlit UI
st.title("코드 분석 및 클래스 다이어그램 생성기")
code_input = st.text_area("분석할 Python 코드를 여기에 붙여넣으세요:")

if st.button("코드 분석하기"):
    try:
        # Abstract Syntax Tree (AST) 기반 분석
        tree = ast.parse(code_input)
        analysis_results = []
        graph = Digraph(format="png", engine="dot")

        def analyze_node(node, parent_name=None):
            if isinstance(node, ast.ClassDef):  # 클래스 정의일 경우
                graph.node(node.name, shape="box", style="filled", color="lightblue")
                if parent_name:
                    graph.edge(parent_name, node.name)
                class_analysis = llm(f"이 코드를 읽고 이 안의 {node.name} 클래스가 어떤 정의인지 한국어로 말해줘:\n\n{code_input}")
                analysis_results.append(f"클래스: {node.name} - {class_analysis}")
                for item in node.body:  # 클래스 내부 요소 분석
                    analyze_node(item, node.name)
            elif isinstance(node, ast.FunctionDef):  # 함수 정의일 경우
                function_analysis = llm(f"이 코드를 읽고 이 안의 {node.name} 함수가 어떤 정의인지 한국어로 말해줘:\n\n{code_input}")
                analysis_results.append(f"함수: {node.name} - {function_analysis}")
                graph.node(node.name, shape="ellipse", style="filled", color="lightgreen")
                if parent_name:
                    graph.edge(parent_name, node.name)

        for node in tree.body:
            analyze_node(node)

        # LangChain을 사용한 추가 분석 (한국어로 요청)
        st.write("### 해당 코드 요약")
        langchain_analysis = llm(f"이 코드를 읽고 한국어로 어떤 코드인지 요약해줘:\n\n{code_input}")
        st.write(langchain_analysis)

        # AST 분석 결과 출력 (한국어로 제공)
        st.write("### 함수의 역할 분석")
        for result in analysis_results:
            st.write(f"- {result}")

        # 클래스 다이어그램 생성 및 표시
        st.write("### 클래스 다이어그램")
        graph.render("class_diagram", format="png", cleanup=True)

        if os.path.exists("class_diagram.png"):
            st.image("class_diagram.png")
        else:
            st.error("클래스 다이어그램 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"코드 분석 중 오류가 발생했습니다: {e}")






#streamlit run /workspaces/codeReader/main.py
#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
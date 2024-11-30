import ast
import streamlit as st
from graphviz import Digraph

# Streamlit UI
st.title("코드 분석 및 클래스 다이어그램 생성기")
code_input = st.text_area("분석할 Python 코드를 여기에 붙여넣으세요:")

if st.button("코드 분석하기"):
    try:
        # Abstract Syntax Tree (AST) 파싱
        tree = ast.parse(code_input)
        analysis_results = []
        graph = Digraph(format="png", engine="dot", directory="C:/Program Files/Graphviz/bin")

        # AST 노드를 분석하는 함수
        def analyze_node(node, parent_name=None):
            if isinstance(node, ast.ClassDef):  # 클래스 정의일 경우
                graph.node(node.name, shape="box", style="filled", color="lightblue")
                if parent_name:
                    graph.edge(parent_name, node.name)
                analysis_results.append(f"클래스: {node.name} - {node.name} 클래스의 역할을 정의합니다.")
                for item in node.body:  # 클래스 내부 요소 분석
                    analyze_node(item, node.name)
            elif isinstance(node, ast.FunctionDef):  # 함수 정의일 경우
                analysis_results.append(f"함수: {node.name} - {node.name} 함수의 역할을 수행합니다.")
                graph.node(node.name, shape="ellipse", style="filled", color="lightgreen")
                if parent_name:
                    graph.edge(parent_name, node.name)

        # AST 노드 처리
        for node in tree.body:
            analyze_node(node)

        # 분석 결과 출력
        st.write("### 분석 결과")
        for result in analysis_results:
            st.write(f"- {result}")

        # 클래스 다이어그램 출력
        st.write("### 클래스 다이어그램")
        graph.render("class_diagram", format="png", cleanup=True)
        st.image("class_diagram.png")

    except Exception as e:
        st.error(f"코드 분석 중 오류가 발생했습니다: {e}")



#streamlit run /workspaces/codeReader/main.py
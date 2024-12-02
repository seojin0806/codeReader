import ast
import os
import streamlit as st
from graphviz import Digraph
from langchain_openai import OpenAI

# LangChain 설정
llm = OpenAI(
    temperature=0.2,
    openai_api_key="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"  # 유효한 OpenAI API 키 입력
)

# Streamlit UI
st.title("코드 분석")
code_input = st.text_area("분석할 코드를 여기에 붙여넣으세요:")

if st.button("코드 분석 및 다이어그램 생성"):
    try:
        # AST 기반 분석
        tree = ast.parse(code_input)
        uml_graph = Digraph(format="png", engine="dot")
        uml_graph.attr(rankdir="TB")

        class_relations = []
        analysis_results = []

        def analyze_class(node):
            """클래스를 UML 형식으로 분석."""
            class_name = node.name
            bases = [base.id for base in node.bases if isinstance(base, ast.Name)]

            # 클래스 노드 추가
            attributes = []
            methods = []

            class_analysis = llm(f"이 코드를 읽고 이 안의 {node.name} 클래스가 어떤 정의인지 한국어로 말해줘:\n\n{code_input}")
            analysis_results.append(f"클래스: {node.name} - {class_analysis}")

            for item in node.body:
                if isinstance(item, ast.FunctionDef):  # 메서드
                    methods.append(item.name)
                    method_analysis = llm(f"이 코드를 읽고 이 안의 {item.name} 메소드가 어떤 정의인지 한국어로 말해줘:\n\n{code_input}")
                    analysis_results.append(f"메소드: {item.name} - {method_analysis}")
                elif isinstance(item, ast.Assign):  # 속성
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            attributes.append(target.id)

            # UML 스타일 노드 생성
            label = f"""<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                <TR><TD BGCOLOR="lightblue"><B>{class_name}</B></TD></TR>
                <TR><TD ALIGN="LEFT">{'\\l'.join(attributes) if attributes else 'No Attributes'}\\l</TD></TR>
                <TR><TD ALIGN="LEFT">{'\\l'.join(methods) if methods else 'No Methods'}\\l</TD></TR>
                </TABLE>>"""
            uml_graph.node(class_name, label=label, shape="plaintext")

            # 상속 관계 추가
            for base in bases:
                class_relations.append((base, class_name))

        # AST 분석
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                analyze_class(node)

        # 상속 관계 연결
        for parent, child in class_relations:
            uml_graph.edge(parent, child, arrowhead="empty")

        # LangChain을 사용한 코드 요약 (한국어로)
        st.write("### 해당 코드 요약")
        langchain_analysis = llm(f"이 코드를 읽고 한국어로 어떤 코드인지 요약해줘:\n\n{code_input}")
        st.write(langchain_analysis)

        st.write("### 함수의 역할 분석")
        for result in analysis_results:
            st.write(f"- {result}")

        # 클래스 다이어그램 출력
        st.write("### UML 클래스 다이어그램")
        uml_graph.render("class_diagram", format="png", cleanup=True)

        if os.path.exists("class_diagram.png"):
            st.image("class_diagram.png")
        else:
            st.error("클래스 다이어그램 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"코드 분석 중 오류가 발생했습니다: {e}")


#streamlit run /workspaces/codeReader/main.py
#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
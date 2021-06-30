import streamlit as st


def write_aligned_header(text: str, alignment: str = "left", level: int = 3):
    st.markdown(
        f"""
            <div style='text-align: {alignment};'> 
                <h{level}>{text}</h{level}>
            </div>
        """,
        unsafe_allow_html=True,
    )

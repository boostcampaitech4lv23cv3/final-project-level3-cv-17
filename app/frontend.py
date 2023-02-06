import streamlit as st


def intro():
    import streamlit as st

    st.write("# Welcome to Sixth Sense Page! 👋")
    st.sidebar.success("Select a demo Above")

    st.markdown(
        """

        **👈 Select a demo from the left** 

        ### What kind of work do you want to do?

        - Image
        - Video
    """
    )
    
page_names_to_funcs = {
    "frontend": intro,
}

page_names_to_funcs["frontend"]()

import tempfile
import streamlit as st
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    st.sidebar.markdown("---")

def render_uiux_review_input():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Screenshot Upload
    with col1:
        st.subheader("🖼️ Upload UI Screenshot")
        uploaded_screenshot = st.file_uploader(
            "Upload a screenshot of your website or app",
            type=["jpg", "jpeg", "png"]
        )

    # Optional UI Metadata Section (in Column 2)
    with col2:
        st.subheader("📝 Optional Info")
        platform_type = st.selectbox("Platform Type", ["Web", "Mobile", "Tablet", "Other"])
        focus_area = st.multiselect(
            "Areas to Review",
            ["Layout", "Visual Hierarchy", "Accessibility", "Color Contrast", "Usability"]
        )

    return {
        "uploaded_screenshot": uploaded_screenshot,
        "platform_type": platform_type,
        "focus_area": focus_area
    }

def generate_uiux_review(review_inputs):
    # Save the uploaded screenshot to a temporary file
    uploaded_screenshot = review_inputs["uploaded_screenshot"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_screenshot.getvalue())
        screenshot_path = tmp.name

    platform_type = review_inputs["platform_type"]
    focus_areas = review_inputs["focus_area"]

    # Create the agent
    uiux_reviewer_agent = Agent(
        model=OpenAIChat(id="o4-mini", api_key=st.session_state.openai_api_key),
        name="UI/UX Reviewer",
        role="An experienced design reviewer who critiques UI layouts and provides actionable suggestions to improve user experience.",
        description=(
            "You are a helpful and detail-oriented design reviewer. Your job is to analyze the uploaded UI screenshot and provide "
            "a comprehensive review covering layout quality, usability, accessibility, and design consistency."
        ),
        instructions=[
            "Start by observing the layout in the uploaded screenshot.",
            "Then evaluate it based on the specified platform type and selected focus areas.",
            "If no focus areas are selected, assume the user wants a general UX critique.",
            "Avoid using placeholder phrases like 'image not clear'. Base suggestions strictly on visual elements present in the screenshot.",
            "Structure your output with clear sections, including:\n\n"
            "### 🖼️ Visual Assessment\n"
            "<Describe the visual structure, design elements, and immediate impressions>\n\n"
            "### 🔍 UX Observations\n"
            "<List observations tied to focus areas like layout, accessibility, contrast, etc.>\n\n"
            "### ✅ Recommendations\n"
            "<Provide clear, actionable suggestions for improvement>\n\n"
            "### 🎯 Final Summary\n"
            "<Conclude with a quick UX rating or summary of priority improvements>"
        ],
        markdown=True
    )

    # Prompt sent to the agent
    focus_summary = ", ".join(focus_areas) if focus_areas else "a general review"
    prompt = f"""
    A user has uploaded a UI screenshot for review.

    Platform: {platform_type}  
    Areas to focus on: {focus_summary}

    Please perform a structured and insightful critique based on what's visible in the screenshot, and format the response accordingly.
    """

    # Run the agent
    uiux_response = uiux_reviewer_agent.run(prompt.strip(), images=[Image(filepath=screenshot_path)])
    uiux_review = uiux_response.content
    
    return uiux_review

def main() -> None:
    # Page config
    st.set_page_config(page_title="UI/UX Reviewer Bot", page_icon="🧠", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"], div[data-testid="stSelectbox"], div[data-testid="stMultiSelect"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🧠 UI/UX Reviewer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to UI/UX Reviewer Bot — your smart design assistant. Upload a screenshot of your app or website to receive insightful UX critique and actionable improvement suggestions.",
        unsafe_allow_html=True
    )

    render_sidebar()
    uiux_input = render_uiux_review_input()

    st.markdown("---")

    # Trigger analysis button
    if st.button("🔍 Generate Review"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not uiux_input["uploaded_screenshot"]:
            st.error("Please upload a UI screenshot to proceed.")
        else:
            with st.spinner("Analyzing the UI and generating review..."):
                review = generate_uiux_review(uiux_input)

                # Save results to session state
                st.session_state.review = review
                st.session_state.review_image = uiux_input["uploaded_screenshot"]

    # Display result if available
    if "review" in st.session_state and "review_image" in st.session_state:
        st.markdown("## 🖼️ Uploaded Screenshot")
        st.image(st.session_state.review_image, use_container_width=False)

        st.markdown("## 📋 UI/UX Review Report")
        st.markdown(st.session_state.review)

        st.markdown("---")

        st.download_button(
            label="📥 Download Review Report",
            data=st.session_state.review,
            file_name="uiux_review.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
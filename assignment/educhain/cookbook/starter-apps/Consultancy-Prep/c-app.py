import streamlit as st
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# ------------------------- Gemini Model Initialization -------------------------
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key = st.secrets["GOOGLE_API_KEY"]  # Replace with your actual Google API Key
)

Gemini_config = LLMConfig(custom_model=gemini_flash)
client = Educhain(Gemini_config)  # Initialize Educhain with Gemini config

# ------------------------- Framework Generator using Gemini -------------------------
def generate_framework_with_gemini(prompt):
    """
    Generates a structured consulting framework for the provided prompt using Gemini.
    """
    query = f"""
    You are a management consulting expert. Based on the following business case or problem, suggest a structured framework that can be used to approach and solve the case:

    {prompt}

    Provide the framework in clear bullet points.
    """
    response = gemini_flash.invoke(query)
    return response.content  # Extract text content from Gemini response

# ------------------------- Guesstimate Generator using Gemini -------------------------
def generate_guesstimate_with_gemini(prompt):
    """
    Generates a consulting guesstimate problem and approach using Gemini.
    """
    query = f"""
    You are helping a candidate prepare for consulting interviews. Generate a guesstimate problem based on this prompt:

    {prompt}

    Also, provide a structured approach to solve this guesstimate.
    """
    response = gemini_flash.invoke(query)
    return response.content  # Extract text content from Gemini response

# ------------------------- Streamlit App Interface -------------------------
st.title("🧩 Consulting Interview Prep App")
st.write("Generate practice questions, guesstimates, and frameworks for management consultancy interviews.")

# User selects input type and difficulty level
input_type = st.selectbox("Choose Input Type", ["Manual Prompt", "Upload PDF File", "Website URL"])
difficulty_type = st.selectbox("Choose Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

user_prompt = None
input_source_type = None  # To keep track of source type for Educhain

# ------------------------- Input Handling -------------------------
if input_type == "Manual Prompt":
    user_prompt = st.text_area("Enter your case prompt:", "Profitability case for an e-commerce company")
    if user_prompt and len(user_prompt.strip()) < 10:
        st.warning("Please provide a more detailed prompt (at least 10 characters).")
        user_prompt = None

elif input_type == "Upload PDF File":
    uploaded_file = st.file_uploader("Upload a PDF Casebook:", type="pdf")
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
            st.error("File size too large. Please upload a file smaller than 10MB.")
            uploaded_file = None
        else:
            user_prompt = uploaded_file  # File object
            input_source_type = "pdf"

elif input_type == "Website URL":
    url = st.text_input("Enter Website URL to extract cases:")
    if url:
        import re
        url_pattern = re.compile(r'^https?://.+')
        if not url_pattern.match(url):
            st.error("Please enter a valid URL starting with http:// or https://")
            url = None
        else:
            user_prompt = url  # URL string
            input_source_type = "url"

# ------------------------- Content Generation Trigger -------------------------
if st.button("Generate Interview Prep Content"):
    if user_prompt:
        with st.spinner('Generating content...'):

            # MCQ Generation: Manual Prompt vs File/URL
            if input_type == "Manual Prompt":
                mcq_list = client.qna_engine.generate_questions(
                    topic=user_prompt,
                    num=3,
                    difficulty_level=difficulty_type,
                    question_type="Multiple Choice"
                )
                questions = mcq_list.questions
            else:
                mcq_list = client.qna_engine.generate_questions_from_data(
                    source=user_prompt,
                    source_type=input_source_type,
                    num=3,
                    question_type="Multiple Choice",
                    difficulty_level=difficulty_type,
                    custom_instructions="Generate consulting related MCQs"
                )
                questions = mcq_list.questions

            # Framework & Guesstimate Generation using Gemini
            if input_type == "Manual Prompt":
                framework_prompt = user_prompt
                guesstimate_prompt = user_prompt
            else:
                framework_prompt = f"Based on the uploaded {'PDF' if input_type == 'Upload PDF File' else 'website'} content, identify a business case and create a structured consulting framework to approach it."
                guesstimate_prompt = f"Based on the uploaded {'PDF' if input_type == 'Upload PDF File' else 'website'} content, create a relevant guesstimate problem that would be appropriate for a consulting interview."

            framework = generate_framework_with_gemini(
                framework_prompt
            )
            guesstimate = generate_guesstimate_with_gemini(
                guesstimate_prompt
            )

            # ------------------------- Display Generated Content -------------------------
            st.subheader("🔍 Multiple Choice Questions (MCQs)")
            for idx, q in enumerate(questions, 1):
                st.write(f"{idx}. {q.question}")
                for opt_idx, opt in enumerate(q.options, 1):
                    # Handle both string options and object options
                    if isinstance(opt, str):
                        st.write(f" - {chr(64+opt_idx)}. {opt}")
                    else:
                        st.write(f"   {chr(64+opt_idx)}. {opt.text}")  # fallback for Option object

                # Display correct answer if available
                if hasattr(q, 'answer') and q.answer:
                    with st.expander("Show Answer"):
                        st.write(f"**Correct Answer:** {q.answer}")
                        if hasattr(q, 'explanation') and q.explanation:
                            st.write(f"**Explanation:** {q.explanation}")
                st.write("---")

            st.subheader("📝 Suggested Framework")
            st.write(framework)

            st.subheader("📊 Guesstimate Problem")
            st.write(guesstimate)
    else:
        st.warning("Please provide valid input to generate content.")
else:
    st.info("Provide input and click 'Generate Interview Prep Content' to start.")

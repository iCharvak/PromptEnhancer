import streamlit as st
import sys
import subprocess

# Debug information
st.write("## 🔍 Debug Information")
st.write(f"Python version: {sys.version}")
st.write("Checking installed packages...")

# Try to import openai and show detailed error
try:
    import openai
    from openai import OpenAI
    st.success("✅ OpenAI package imported successfully!")
    st.write(f"OpenAI version: {openai.__version__}")
except ImportError as e:
    st.error(f"❌ OpenAI import failed: {str(e)}")
    st.write("Let's check what packages are installed:")
    
    # Show installed packages
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    st.code(result.stdout)
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Prompt Enhancer",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .enhanced-prompt {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def enhance_prompt(role, context, task, api_key):
    """Enhance the user's prompt using OpenAI API"""
    try:
        client = OpenAI(api_key=api_key)
        
        enhancement_prompt = f"""
        You are an expert prompt engineer. Enhance the following prompt components:

        Role: {role}
        Context: {context}
        Task: {task}

        Create an enhanced prompt with:
        1. Clear role definition
        2. Comprehensive context
        3. Specific task requirements
        4. Assumptions made
        5. Questions for clarification

        Format as:
        **ENHANCED PROMPT:** [enhanced prompt]
        **ASSUMPTIONS:** [assumptions]
        **QUESTIONS:** [clarifying questions]
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert prompt engineer."},
                {"role": "user", "content": enhancement_prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Prompt Enhancer</h1>', unsafe_allow_html=True)
    
    # API Key input
    st.sidebar.markdown("### 🔑 OpenAI API Key")
    api_key = st.sidebar.text_input("Enter API Key:", type="password")
    
    if api_key:
        st.sidebar.success("✅ API key provided")
    else:
        st.sidebar.warning("⚠️ Please enter your API key")
    
    # Main interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Input Components")
        role = st.text_area("Role:", height=80, placeholder="e.g., Senior marketing strategist...")
        context = st.text_area("Context:", height=120, placeholder="e.g., Launching eco-friendly products...")
        task = st.text_area("Task:", height=80, placeholder="e.g., Create marketing strategy...")
        
        if st.button("🚀 Enhance Prompt", type="primary"):
            if not api_key:
                st.error("Please enter your API key")
            elif not all([role, context, task]):
                st.warning("Please fill in all fields")
            else:
                with st.spinner("Enhancing..."):
                    result = enhance_prompt(role, context, task, api_key)
                    st.session_state.enhanced_result = result
    
    with col2:
        st.subheader("✨ Enhanced Output")
        if hasattr(st.session_state, 'enhanced_result'):
            if st.session_state.enhanced_result.startswith("Error:"):
                st.error(st.session_state.enhanced_result)
            else:
                st.markdown('<div class="enhanced-prompt">', unsafe_allow_html=True)
                st.markdown(st.session_state.enhanced_result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.download_button(
                    "📋 Download Result",
                    data=st.session_state.enhanced_result,
                    file_name="enhanced_prompt.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
import streamlit as st
import openai
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Prompt Enhancer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .enhanced-prompt {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def enhance_prompt(role, context, task, api_key):
    """
    Enhance the user's prompt using OpenAI API
    """
    try:
        client = OpenAI(api_key=api_key)
        
        enhancement_prompt = f"""
        You are an expert prompt engineer. I need you to enhance the following prompt components into a comprehensive, detailed prompt that will generate high-quality AI responses.

        Given components:
        - Role: {role}
        - Context: {context}
        - Task: {task}

        Please create an enhanced prompt that:
        1. Clearly defines the AI's role and expertise
        2. Provides comprehensive context and background
        3. Specifies the exact task with clear deliverables
        4. Includes any necessary assumptions you're making
        5. Lists questions or clarifications that would improve the output quality

        Format your response as:

        **ENHANCED PROMPT:**
        [Your enhanced prompt here]

        **ASSUMPTIONS MADE:**
        [List any assumptions you made about the request]

        **QUESTIONS FOR CLARIFICATION:**
        [List questions that would help improve the output]

        Make the enhanced prompt professional, detailed, and actionable.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert prompt engineer who specializes in creating detailed, effective prompts for AI systems."},
                {"role": "user", "content": enhancement_prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Main header
    st.markdown('<h1 class="main-header">🚀 Prompt Enhancer</h1>', unsafe_allow_html=True)
    st.markdown("Transform your basic prompts into powerful, detailed instructions for AI systems!")

    # Information box
    st.markdown("""
    <div class="info-box">
        <strong>🔒 Privacy Notice:</strong> Your OpenAI API key is never stored on our servers. 
        It's only used temporarily for your current session to enhance your prompts.
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for API key
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="Get your API key from: https://platform.openai.com/api-keys"
        )
        
        if api_key:
            st.success("API key provided ✓")
        else:
            st.warning("Please enter your OpenAI API key to use the enhancer.")

        st.markdown("---")
        st.markdown("### 📚 How to use:")
        st.markdown("""
        1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
        2. Enter your API key in the field above
        3. Fill in the Role, Context, and Task
        4. Click 'Enhance Prompt'
        5. Copy your enhanced prompt!
        """)
        
        st.markdown("---")
        st.markdown("### ❓ Need help?")
        with st.expander("Getting OpenAI API Key"):
            st.markdown("""
            1. Go to [OpenAI Platform](https://platform.openai.com)
            2. Sign up or log in to your account
            3. Navigate to API Keys section
            4. Create a new API key
            5. Copy and paste it here
            """)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<h2 class="section-header">📝 Input Your Prompt Components</h2>', unsafe_allow_html=True)
        
        role = st.text_area(
            "🎭 Role:",
            height=100,
            placeholder="e.g., You are a senior marketing strategist with 10 years of experience in digital marketing and brand development...",
            help="Define what role or persona the AI should adopt"
        )

        context = st.text_area(
            "🌍 Context:",
            height=150,
            placeholder="e.g., Our company is launching a new eco-friendly product line targeting millennials who are environmentally conscious and tech-savvy...",
            help="Provide background information and relevant details"
        )

        task = st.text_area(
            "✅ Task:",
            height=100,
            placeholder="e.g., Create a comprehensive marketing strategy including target channels, budget allocation, timeline, and key performance indicators...",
            help="Specify exactly what you want the AI to do"
        )

        enhance_button = st.button("🚀 Enhance Prompt", type="primary", use_container_width=True)

    with col2:
        st.markdown('<h2 class="section-header">✨ Enhanced Prompt Output</h2>', unsafe_allow_html=True)
        
        if enhance_button:
            if not api_key:
                st.error("🔑 Please enter your OpenAI API key in the sidebar to get started.")
            elif not role or not context or not task:
                st.warning("📝 Please fill in all three components (Role, Context, Task) before enhancing.")
            else:
                with st.spinner("🤖 AI is enhancing your prompt..."):
                    enhanced_result = enhance_prompt(role, context, task, api_key)
                
                if enhanced_result.startswith("Error:"):
                    st.error(f"❌ {enhanced_result}")
                else:
                    st.markdown('<div class="enhanced-prompt">', unsafe_allow_html=True)
                    st.markdown(enhanced_result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Copy button
                    st.download_button(
                        label="📋 Download Enhanced Prompt",
                        data=enhanced_result,
                        file_name="enhanced_prompt.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Option to enhance again with modifications
                    if st.button("🔄 Enhance Again", help="Modify your inputs above and enhance again"):
                        st.rerun()

    # Example section
    with st.expander("💡 See an Example"):
        st.markdown("**Example Input:**")
        st.markdown("**Role:** Content marketing specialist")
        st.markdown("**Context:** SaaS company launching project management tool")
        st.markdown("**Task:** Create blog post outline")
        
        st.markdown("**Enhanced Output would include:**")
        st.markdown("- Detailed role definition with expertise areas")
        st.markdown("- Comprehensive context about the SaaS market")
        st.markdown("- Specific deliverables and structure requirements")
        st.markdown("- Assumptions about target audience")
        st.markdown("- Questions about brand voice, competitors, etc.")

    # Footer
    st.markdown("---")
    col_footer1, col_footer2, col_footer3 = st.columns(3)
    with col_footer1:
        st.markdown("🛠️ **Built with:** Streamlit & OpenAI")
    with col_footer2:
        st.markdown("🔒 **Privacy:** API keys never stored")
    with col_footer3:
        st.markdown("💡 **Purpose:** Better AI interactions")

if __name__ == "__main__":
    main()
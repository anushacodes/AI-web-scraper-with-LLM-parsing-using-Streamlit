import streamlit as st
from scraper import scrape_website
from llm_analyzer import analyze_with_llm
from styles import custom_css
import time

# Set page config
st.set_page_config(
    page_title="AI Web Scraper with LLM Parsing",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Title and introduction
st.title("🔍 AI Web Scraper with LLM Parsing")
st.markdown("""
This tool allows you to scrape content from any website and analyze it using Large Language Models.
Simply enter a URL, customize your scraping preferences, and let the AI extract insights for you!
""")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    st.markdown("---")
    st.header("About")
    st.info("""
    This application combines web scraping capabilities with the power of Large Language Models
    to extract and analyze web content. Use it to quickly gather insights from any website!
    """)

# Main layout
col1, col2 = st.columns([2, 3])

with col1:
    st.header("Input")
    
    # URL input
    url = st.text_input("Enter Website URL", "https://example.com")
    
    # Advanced options
    with st.expander("Advanced Scraping Options"):
        css_selector = st.text_input("CSS Selector (Optional)", 
                                     placeholder="e.g. article, .content, #main-content")
        st.info("Leave blank to auto-detect main content")
    
    # Query input
    st.subheader("What would you like to know about this content?")
    query = st.text_area("Your Query", 
                         placeholder="e.g. Summarize the main points, Extract contact information, etc.")
    
    # Submit button
    submit = st.button("Scrape and Analyze")

# Results section
with col2:
    st.header("Results")
    
    if submit:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        with st.spinner("Scraping website..."):
            scraped_content = scrape_website(url, css_selector)
            
        if "Error" in scraped_content:
            st.error(scraped_content)
        else:
            # Display scraped content
            with st.expander("View Scraped Content", expanded=False):
                st.markdown(f'<div class="scraped-content">{scraped_content[:5000]}</div>', unsafe_allow_html=True)
                if len(scraped_content) > 5000:
                    st.info(f"Showing first 5000 characters of {len(scraped_content)} total.")
            
            # Process with LLM if query is provided
            if query and api_key:
                with st.spinner("Analyzing content with LLM..."):
                    time.sleep(0.5)  # Slight delay for better UX
                    llm_analysis = analyze_with_llm(scraped_content, query, api_key)
                    
                st.subheader("AI Analysis")
                st.markdown(f'<div class="llm-analysis">{llm_analysis}</div>', unsafe_allow_html=True)
                
                # Download options
                st.download_button(
                    label="Download Analysis",
                    data=f"Web Scraping Analysis\n\nURL: {url}\nQuery: {query}\n\nAnalysis:\n{llm_analysis}",
                    file_name="web_analysis.txt",
                    mime="text/plain"
                )
            elif not api_key and query:
                st.warning("Please enter your OpenAI API key in the sidebar to analyze content.")
            elif not query and api_key:
                st.info("Enter a query to analyze the scraped content.")

# Add footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit, BeautifulSoup, and OpenAI API", 
    unsafe_allow_html=True
)

from openai import OpenAI

def analyze_with_llm(text, query, api_key):
    """
    Analyze text content using OpenAI's LLM.
    
    Args:
        text (str): The text content to analyze
        query (str): The user's query about the content
        api_key (str): OpenAI API key
        
    Returns:
        str: Analysis result from the LLM
    """
    try:
        client = OpenAI(api_key=api_key)
        
        # Prepare the prompt
        prompt = f"""
        You are an AI assistant specialized in analyzing web content.
        
        CONTENT:
        {text[:9000]}  # Limiting to first 9000 chars to stay within context limits
        
        USER QUERY:
        {query}
        
        Please analyze the content and answer the query. Focus on extracting key information relevant to the query.
        If the content doesn't contain relevant information, please state that clearly.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes web content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing with LLM: {str(e)}"

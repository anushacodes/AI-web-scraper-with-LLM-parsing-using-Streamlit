import re

def clean_text(text)
  # to clean up excessive whitespace
  text = re.sub(r'\n+', '\n', text)
  text = re.sub(r' +', ' ', text)
  
  return text

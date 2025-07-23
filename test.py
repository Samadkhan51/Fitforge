import google.generativeai as genai

# Set your API key
GOOGLE_API_KEY = "AIzaSyDdxFSA719_cipQGXZrZdFqI7VdJGKjSvs"
genai.configure(api_key=GOOGLE_API_KEY)

# Instantiate the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# Prompt to test the model
prompt = "Explain the theory of relativity in simple terms. in 4 lines"

# Generate response
try:
    response = model.generate_content(prompt)
    print("Model response:\n")
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")

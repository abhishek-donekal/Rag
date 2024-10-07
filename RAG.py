import streamlit as st
import pandas as pd
import openai

# Streamlit UI
st.title("RAG Pipeline for Excel Database Exploration")

# Prompt user for OpenAI API key
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Set OpenAI API key
if api_key:
    openai.api_key = api_key

    # Load Excel Data
    @st.cache
    def load_data(file_path):
        """Load the Excel sheet and return it as a Pandas DataFrame."""
        return pd.read_excel(file_path)

    # Define function to generate OpenAI responses
    def query_openai(prompt):
        """Query OpenAI API with the given prompt."""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()

    # RAG Pipeline Function
    def generate_field_suggestions(query, dataframe):
        """Generate relevant field suggestions based on the user's query."""
        fields = dataframe.columns.tolist()
        
        # Create a detailed prompt for GPT to understand the context
        prompt = f"""
        I have the following fields in my database: {fields}.
        Based on the user's query: "{query}", suggest the most relevant fields to use.
        Also, provide a brief description of why each field might be useful for the query.
        """

        # Get suggestions from GPT
        suggestions = query_openai(prompt)
        return suggestions

    # Upload Excel File
    uploaded_file = st.file_uploader("Upload your Excel sheet", type=["xlsx"])

    if uploaded_file:
        # Load the Excel file into a DataFrame
        df = load_data(uploaded_file)
        st.write("### Loaded Data Preview")
        st.dataframe(df.head())

        # User Query Input
        user_query = st.text_input("Enter your query to explore fields in the database")

        if user_query:
            # Get field suggestions using RAG
            with st.spinner("Generating field suggestions..."):
                suggestions = generate_field_suggestions(user_query, df)
            
            # Display GPT's suggestions
            st.write("### Suggested Fields and Descriptions")
            st.write(suggestions)

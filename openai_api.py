import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo")

def get_response_from_openai(match_details: str):
    prompt_template = PromptTemplate(
        input_variables=["match_details"],
        template="""Analyze the following match data and provide a detailed description of who was the carry and who was the most useless. Make the analysis detailed and include some humorous or funny comments.
        Here are some examples of how to analyze the data:
        Example 1:
        The carry was Player A due to *stats and praises*. Meanwhile, Player B was the least useful human being due to *stats and literal insults*.
        Now analyze the following match data:
        {match_details}"""
    )
    sequence = prompt_template | llm
    response = sequence.invoke({"match_details": match_details})
    return response

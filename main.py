from llamaapi import LlamaAPI
import json

# Replace 'Your_API_Token' with your actual API token
api_token = 'LA-6bd0b23628cf4afc8ca7096f73393c315fe0fe451b554273977c18f2ed67ceda'

llama = LlamaAPI(api_token)

from openai import OpenAI
from model import QuestionAnswer, InterviewRecord, ProfileInfo

def test(name) :
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_token,
        base_url="https://api.llama-api.com"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Bonjour, je m'appelle " + name,
            }
        ],
        functions = None,
        model="llama3.1-70b",
        max_tokens=50,
        stream=True
    )

    result = "";

    for chunk in chat_completion:
        result += str(chunk.choices[0].delta.content)

    result = result[:-4]
    return result

def generateFeedback(record: InterviewRecord) :
    for questionAnswer in record.question_answers:
        questionAnswer.feedback = "Feedback for question: "+questionAnswer.question
    return record

def generateQuestions(profile: ProfileInfo) :
    return ["Qu'est-ce que le NoSQL ?", "Comment gérer vous les problèmes ?", "Impréssionner moi"]

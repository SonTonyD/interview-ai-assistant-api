from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from model import QuestionAnswer, InterviewRecord, ProfileInfo, FeedbackRequest
from typing import List

import main as main_program

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # URL de votre application Angular
        "http://127.0.0.1:4200",
        "https://prototype-ai-school-frontend.vercel.app",  # Ajoutez aussi cette variante
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les headers
)

@app.get("/")
async def root():
    return {"message": "Job Interview AI Assistant"}

@app.post("/interview", response_model=InterviewRecord)
async def generate_feedback(feedbackRequest: FeedbackRequest):

    newRecord: InterviewRecord = main_program.generateFeedback(feedbackRequest.record, feedbackRequest.profile);
    return newRecord

@app.post("/question", response_model=List[str])
async def generate_questions(profile: ProfileInfo):
    new_questions = main_program.generateQuestions(profile)
    return new_questions
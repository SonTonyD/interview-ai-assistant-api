from pydantic import BaseModel
from typing import List, Optional

class QuestionAnswer(BaseModel):
    question: str
    answer: str
    feedback: Optional[str] = None

class InterviewRecord(BaseModel):
    id: str
    user_id: str
    question_answers: List[QuestionAnswer]

class ProfileInfo(BaseModel):
    id: str
    user_id: str
    personnal_description: str
    secteur: str
    poste: str
    objectif_entretien: str
    offre_emploi: str

class FeedbackRequest(BaseModel):
    record: InterviewRecord
    profile: ProfileInfo
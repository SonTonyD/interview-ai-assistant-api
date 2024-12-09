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

import json
import re

def extract_and_parse_json(llm_response: str) -> list[str]:
    """
    Extrait un objet JSON de la réponse brute du LLM et le parse en une liste de chaînes.
    
    :param llm_response: La réponse brute du LLM (peut contenir du texte autour du JSON)
    :return: Liste de questions (chaînes de caractères)
    """
    try:
        # Regex pour extraire un JSON valide de type liste
        json_match = re.search(r'\[.*\]', llm_response, re.DOTALL)
        if not json_match:
            raise ValueError("Aucun objet JSON valide trouvé dans la réponse.")
        
        # Extraction du JSON
        json_str = json_match.group(0)
        
        # Chargement du JSON
        questions = json.loads(json_str)
        
        # Validation : s'assurer que c'est une liste de chaînes
        if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
            return questions
        else:
            raise ValueError("Le JSON n'est pas une liste de chaînes.")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Erreur lors du parsing JSON : {e}")
    except ValueError as e:
        raise RuntimeError(f"Validation échouée : {e}")

def promptToLLM(prompt: str):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_token,
        base_url="https://api.llama-api.com"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
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

def generateQuestions(profile: ProfileInfo) :
    prompt = f"""
    Voici un profil utilisateur pour lequel je souhaite préparer un entretien d'embauche.

    **Profil utilisateur :**
    - **Description personnelle** : {profile.personnal_description}
    - **Secteur d'activité** : {profile.secteur}
    - **Poste visé** : {profile.poste}
    - **Objectif de l'entretien** : {profile.objectif_entretien}
    - **Offre d'emploi analysée** :  
    {profile.offre_emploi}

    **Tâche** :  
    Sur la base des informations ci-dessus, génère une liste de 20 questions d'entretien que cette personne pourrait rencontrer.  
    - La liste doit être composée de questions techniques (pertinentes pour le poste et le secteur) et de questions personnelles ou comportementales.  
    - Veille à varier les types de questions pour couvrir différents aspects de l'entretien (techniques, expériences, soft skills, etc.).  
    - Classe les questions en deux catégories :  
    - **Questions techniques**  
    - **Questions personnelles et comportementales**  

    Rends les questions claires et directes, en adaptant leur niveau de complexité au contexte du poste visé.

    Retourne les questions sous forme de liste JSON comme suit :  
    [
    "Question 1",
    "Question 2",
    ...
    ]   
    """

    llm_response = promptToLLM(prompt)
    result = extract_and_parse_json(llm_response)

    return result

def generateFeedback(record: InterviewRecord, profile: ProfileInfo) :
    for questionAnswer in record.question_answers:

        prompt = f"""
        Tu es un coach spécialisé en préparation aux entretiens d'embauche. Ton rôle est de fournir un feedback constructif et des reformulations adaptées pour améliorer les réponses données par l'utilisateur.

        Voici le profil de l'utilisateur :
        - Description personnelle : {profile.personnal_description}
        - Secteur : {profile.secteur}
        - Poste visé : {profile.poste}
        - Objectif de l'entretien : {profile.objectif_entretien}
        - Offre d'emploi : {profile.offre_emploi}

        Question : "{questionAnswer.question}"
        Réponse donnée par l'utilisateur : "{questionAnswer.answer}"

        1. Donne une analyse détaillée de la réponse de l'utilisateur :
        - Points forts
        - Points faibles
        - Pertinence par rapport au poste et au secteur

        2. Propose une ou plusieurs reformulations plus adaptées en gardant à l'esprit les attentes pour ce poste et ce secteur.

        Réponds de manière concise et professionnelle.

        """

        llm_response = promptToLLM(prompt)
        questionAnswer.feedback = llm_response
    return record
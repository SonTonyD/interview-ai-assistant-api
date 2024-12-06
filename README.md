Install Python 3.10.0

python -m venv mon_ia_env

# Install dependencies

source mon_ia_env/Scripts/activate
pip install -r requirements.txt

# Run the api

uvicorn api:app --reload

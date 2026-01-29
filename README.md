Activate your virtual environment:

python -m venv venv

source venv/bin/activate

(I used source venv/Scripts/activate on bash terminal having my database in windows)

Install dependencies:
pip install -r requirements.txt

Create a .env file, .env_sample file in folder includes how to do it, replace with your credentials

Run the FastAPI app:
uvicorn app.main:app --reload

Go to FastAPI Swagger UI: http://127.0.0.1:8000/docs

You can test endpoints and see results.

Run pytest:
pytest test.py

NOTE:
I have attached the SQL scripts I used to create the vehicles table in file name 'Used SQL-scripts'.
There are also unused SQL scripts for when I first had tables with relationships but didn't use this approach
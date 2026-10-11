# Flask & MongoDB — DevOps Assignment

Name: Tanishk Singh

## Tasks
1. `GET /api` reads `data.json` and returns the data as JSON.
2. `GET /` displays a form.
3. A valid `POST /` inserts the submission into MongoDB Atlas.
4. Success redirects to `/success` and displays **Data submitted successfully**.
5. Validation/database errors remain on the same form page.

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your MongoDB Atlas connection string.

```powershell
python app.py
```

Open `http://127.0.0.1:5000/`.

## API
Open `http://127.0.0.1:5000/api`.

## GitHub
https://github.com/tanishk162del-create/Flask_and_MongoDB_Tanishk_Singh

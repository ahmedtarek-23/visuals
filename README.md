# NYC Traffic Crashes Analysis Project

## Project Overview
This project analyzes traffic crash data from New York City, providing insights through interactive visualizations using a Dash web application.

## Contents
- `notebook/Milestone1_EDA_Cleaning.ipynb` — EDA, cleaning & integration
- `data/` — cleaned dataset (small sample) or download instructions
- `app/` — interactive website (Dash or React)

## How to run (local)
1. Clone:
   ```bash
   git clone https://github.com/<username>/nyc-crashes-project.git
   cd nyc-crashes-project
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Install required packages:

```powershell
pip install -r requirements.txt
```

4. Run the Dash app locally:

```powershell
python app/app.py
```

## App structure

app/
- app.py               # Dash application entrypoint
- components.py        # small UI helpers
- utils.py             # data loading and helper functions

data/
- place your CSV files here: either the cleaned file `cleaned_integrated_crashes_persons.csv` or the raw `Motor_Vehicle_Collisions_-_Crashes_20251111.csv` and `Motor_Vehicle_Collisions_-_Person_20251111.csv`

## Deployment

You can deploy the app to Render or Heroku. A sample `Procfile` is included for Heroku/Render (uses gunicorn).

1. On Heroku (example):

```powershell
heroku create your-app-name
git push heroku main
heroku ps:scale web=1
```

2. On Render: create a new Web Service, point to this repo, set the Build Command: `pip install -r requirements.txt` and Start Command: `gunicorn app.app:server`.

Make sure to place your data files into the `data/` folder before deploying or provide a way for the app to load remote CSVs.

## Team & Contributions

- Tarek Metwally — data cleaning, notebook and app integration
- (Add other team members here)

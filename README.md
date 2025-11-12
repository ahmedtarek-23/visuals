NYC Collision Insights Dashboard - Data Engineering and Visualization

Project Overview (Milestone 1)

This project navigates the complete data engineering pipeline using a large, real-world dataset on motor vehicle collisions in New York City (NYC). The goal of Milestone 1 was to Explore, Clean, and Integrate the data, followed by the development of an Interactive Dashboard using Dash (Python/Plotly) to visualize key insights dynamically.

The final deliverable is a modular, well-documented data pipeline and a functional web application that allows users to filter, search, and generate reports on crash data in real-time.

🚀 Getting Started

To run this project locally, you must have Python 3.x installed.

1. File Structure

This repository uses a modular structure:

File/Folder

Description

app.py

Main Dashboard App. Defines the Dash layout, loads data, and manages callbacks.

merged_crashes_person.csv

Final Data Source. The cleaned and integrated dataset required by app.py.

notebook/

Contains Milestone1_EDA_Cleaning.ipynb detailing EDA, cleaning, and integration steps.

utils/

Utility functions for modularity.

utils/data_filters.py

Logic for generating dropdown options and filtering data based on user input/search.

utils/chart_generation.py

Functions to generate Plotly figure objects for the dashboard.

2. Local Setup and Dependencies

Clone the Repository:

git clone [Your Repository URL Here]
cd Viusals


Create and Activate Environment: (Highly Recommended)

python -m venv venv
.\venv\Scripts\activate   # For Windows
# source venv/bin/activate # For macOS/Linux


Install Dependencies:

# Core libraries for Dash, Pandas, Plotly, and Gunicorn (for deployment)
pip install dash pandas plotly gunicorn


Data Check: Ensure the merged_crashes_person.csv file is present in the root directory (where app.py expects it).

3. Running the Application

Run the Dash application from the project root:

python app.py


The application will be hosted locally. Open your browser and navigate to the link provided in the terminal (usually http://127.0.0.1:8050/).

🌐 Deployment Instructions

The application is configured to be deployed on platforms like Render or Heroku using a WSGI server (gunicorn).

Procfile: A file named Procfile is required in the root directory:

web: gunicorn app:server


(Note: app is the file name, and server is the Flask instance defined in app.py.)

Hosting: Deploy the entire repository to your chosen platform, ensuring the platform runs the Procfile command.

🤝 Team Contribution Breakdown

This project was completed by a team of 5 members. This section documents the contribution of each member to meet the required submission criteria.

Team Member

Contribution Areas

Research Questions (RQs)

Team Member 1

EDA, Initial Data Cleaning, README.md Drafting, Chart Aesthetics

RQ 1, RQ 5

Team Member 2

Data Integration (pd.merge), Post-Integration Cleaning, app.py Callback Logic

RQ 2, RQ 6

Team Member 3

Dash Layout (app.py UI), Dropdown/Filter Component Implementation, data_filters.py logic

RQ 3, RQ 7

Team Member 4

Outlier Detection (IQR), Validation Visualizations, Search Mode Implementation, Documentation

RQ 4, RQ 8

Team Member 5

chart_generation.py development, Deployment Setup (Procfile, hosting), Final Data Validation

RQ 9, RQ 10

❓ Project Research Questions

The dashboard visualizations are designed to answer the following 10 complex research questions:

Spatial Correlation (GIS): Is there a statistically significant correlation between the crash density per borough and the average severity of injuries (PERSON_INJURY) in that borough? (TM1)

Temporal & Factor Analysis: How has the primary contributing factor for fatal crashes shifted over the past five years (2020-2025), and does this correlate with specific traffic law changes? (TM2)

Vulnerable Populations: Do crashes involving pedestrians show a disproportionate involvement of specific vehicle types during peak commuter hours (7-9 AM, 4-6 PM)? (TM3)

Weather/Time of Day: Which combination of time-of-day (e.g., night vs. day) and crash location type leads to the highest average number of injured persons per collision? (TM4)

Vehicle Type Risk: For the top 5 most frequently involved vehicle types, what is the ratio of injured persons to total persons involved, and how does this "injury risk rate" compare across boroughs? (TM1)

Year-over-Year Fatality Trend: What is the compound annual growth rate (CAGR) of fatalities for the top 3 most common contributing factors? (TM2)

Demographic Impact: Is there a trend in injury severity based on the gender (PERSON_SEX) of the injured party, controlling for the type of crash? (TM3)

Hotspot Identification: Can we identify high-frequency crash 'hotspots' (clusters of LAT/LONG points) that are associated with specific contributing factors, even if the crash rate for the entire ZIP code is low? (TM4)

Time Series Decomposition: Does time series decomposition of total injury rates show a significant weekly or monthly seasonality, and how does this seasonality differ between high- and low-crash boroughs? (TM5)

Factor vs. Person Status: For crashes involving passengers (PERSON_TYPE = Passenger), what is the most common contributing factor, and how does this factor correlate with the severity of their injury? (TM5)

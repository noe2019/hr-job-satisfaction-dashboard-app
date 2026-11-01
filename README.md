# Employee Job Satisfaction & Attrition Dashboard

HR dashboard tracking attrition drivers and job satisfaction by department (web version of the Tableau dashboard).

**Live app:** https://noe-hr-analytics-b50e5f00fc34.herokuapp.com/
**Portfolio:** https://noe2019.github.io/DA-Portfolio-Website/

## Features
- Headcount, attrition rate, average age, salary and tenure
- Attrition by department, role, age band and overtime
- Satisfaction heatmap by job role
- Interactive filters

## Tech stack
Python, Pandas, Streamlit, Plotly

## Data
All data in this app is **simulated** (generated in `data.py` with a fixed random seed) to reproduce the structure of the original project without exposing real or confidential records.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment
Deployed on Heroku (stack `heroku-24`, Python 3.12) using the `Procfile` in this repository.

---
Author: Noé Carème Fouotsa Manfouo

"""Simulated HR dataset (IBM HR Analytics-like)."""
import numpy as np
import pandas as pd

ROLES = {"Sales": ["Sales Executive", "Sales Representative", "Manager"],
         "R&D": ["Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Research Director", "Manager"],
         "Human Resources": ["Human Resources", "Manager"]}


def simulate(n=1470, seed=17):
    r = np.random.default_rng(seed)
    dept = r.choice(list(ROLES), n, p=[.3, .65, .05])
    role = np.array([r.choice(ROLES[d]) for d in dept])
    age = r.normal(37, 9, n).clip(18, 60).round()
    years = np.minimum(r.gamma(1.6, 4.5, n), age - 18).round()
    overtime = r.random(n) < .28
    job_sat, env_sat, wlb = r.integers(1, 5, n), r.integers(1, 5, n), r.choice([1, 2, 3, 4], n, p=[.06, .23, .6, .11])
    income = (2500 + 180 * years + 60 * (age - 18) + np.where(np.isin(role, ["Manager", "Research Director"]), 9000, 0)
              + r.normal(0, 1200, n)).clip(1000).round(-1)
    logit = (-1.2 + 1.3 * overtime - .35 * (job_sat - 2.5) - .3 * (env_sat - 2.5) - .3 * (wlb - 2.7)
             - .06 * (age - 37) - .08 * years - .00012 * (income - 6500) + .5 * (role == "Sales Representative"))
    attr = r.random(n) < 1 / (1 + np.exp(-logit))
    return pd.DataFrame({"employee_id": np.arange(1, n + 1), "age": age, "gender": r.choice(["Female", "Male"], n, p=[.4, .6]),
                         "department": dept, "job_role": role,
                         "education_field": r.choice(["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"], n),
                         "monthly_income": income, "years_at_company": years, "overtime": np.where(overtime, "Yes", "No"),
                         "job_satisfaction": job_sat, "environment_satisfaction": env_sat, "work_life_balance": wlb,
                         "attrition": np.where(attr, "Yes", "No")})

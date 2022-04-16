from tkinter.ttk import Separator
import pandas as pd
import datetime as date

# --------------- possible inputs ---------------
N_cases = 100
d1 = '2020-08-01'
d2 = '2020-08-31'
# -----------------------------------------------

# --------------------------------- cities with more than N_cases cases ---------------------------------
# import covid data from csv, using latin encoding and skipping bad lines
covid_panel = pd.read_csv("../data/microdados.csv", encoding="ISO-8859-1", on_bad_lines="skip", sep=";", parse_dates=["DataDiagnostico"])

# select the confirmed cases, groups by city and saves the ones that surpass N_cases
confirmed = covid_panel[covid_panel['Classificacao'] == 'Confirmados']
confirmed_count = confirmed.groupby('Municipio').size()
confirmed_count[confirmed_count > N_cases].to_csv("../data/N_case_cities.csv")

# -------------------------------------- cases between certain dates --------------------------------------
d1 = date.datetime.strptime(d1, "%Y-%m-%d")
d2 = date.datetime.strptime(d2, "%Y-%m-%d")

# select the confirmed cases between d1 and d2
cases_in_period = confirmed[(confirmed['DataDiagnostico'] >= d1) & (confirmed['DataDiagnostico'] <= d2)]
cases_in_period.to_csv("../data/cases_in_period.csv")

# ------------------------------- city rank by number of cases between dates -------------------------------

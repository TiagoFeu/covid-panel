from tkinter.ttk import Separator
import pandas as pd
import datetime as date

# --------------- possible inputs ---------------
N_cases = 100
d1 = '2020-05-01'
d2 = '2020-05-31'
# -----------------------------------------------

# import covid data from csv, using latin encoding and skipping bad lines
covid_panel = pd.read_csv("../data/microdados.csv", encoding="ISO-8859-1", on_bad_lines="skip", sep=";")

# select the confirmed cases, groups by city and saves the ones that surpass N_cases
confirmed = covid_panel[covid_panel['Classificacao'] == 'Confirmados']
confirmed_count = confirmed.groupby('Municipio').size()
confirmed_count[confirmed_count > N_cases].to_csv("../data/N_case_cities.csv")

# DataDiagnostico 2020-09-28
# Number of confirmed cases between d1 and d2
print(confirmed['DataDiagnostico'].between_time(d1,d2))
from tkinter.ttk import Separator
import pandas as pd
import datetime as date

# ----------------------------------------------- inputs -----------------------------------------------
N_cases = 100
d1 = '2020-08-01'
d2 = '2020-08-31'
analize_city = 'VITORIA'  # input the city name or ALL

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
top_cities_in_period = cases_in_period.groupby('Municipio').size().sort_values(ascending=False)
top_cities_in_period.to_csv("../data/top_cities_in_period.csv")

# ------------------------ percentage of hospitalized, dead, hospitalized-then-dead ------------------------
# checks if data from a city or all
confirmed_in_city = confirmed if analize_city == 'ALL' else confirmed[confirmed['Municipio'] == analize_city]

# percentage of confirmed cases that are hospitalized
confirmed_hospitalized = confirmed_in_city[confirmed_in_city['FicouInternado'] == 'Sim']
hospitalized_percentage = confirmed_hospitalized.size / confirmed_in_city.size
# print(f'Percentage of hospitalized cases: {hospitalized_percentage.round(4) * 100}%')

# percentage of confirmed cases that died
confirmed_dead = confirmed[confirmed['Evolucao'] == 'Óbito pelo COVID-19']
dead_percentage = confirmed_dead.size / confirmed_in_city.size
# print(f'Percentage of dead cases: {dead_percentage.round(4) * 100}%')

hospitalized_that_died = confirmed_hospitalized[confirmed_hospitalized['Evolucao'] == 'Óbito pelo COVID-19']
hospitalized_that_died_percentage = hospitalized_that_died.size / confirmed_hospitalized.size
# print(f'Percentage of hospitalized cases that died: {hospitalized_that_died_percentage.round(4) * 100}%')


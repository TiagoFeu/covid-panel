from tkinter.ttk import Separator
import pandas as pd
import datetime as date

def age_to_days(age):
    days = [int(s) for s in age.split() if s.isdigit()]
    days = days[0] * 365 + days[1] * 30 + days[2]
    return days

# ----------------------------------------------- inputs -----------------------------------------------
N_cases = 100
d1 = '2020-08-01'  # date of diagnosis
d2 = '2020-08-31'
d1_d = '2020-09-01'  # date of death
d2_d = '2020-09-30'
analize_city = 'VITORIA'  # input the city name or ALL
metrics = open('../data/metrics.txt', 'w')

# --------------------------------- cities with more than N_cases cases ---------------------------------
# import covid data from csv, using latin encoding and skipping bad lines
covid_panel = pd.read_csv("../data/microdados.csv", encoding="ISO-8859-1", on_bad_lines="skip", sep=";", parse_dates=["DataDiagnostico",
                                                                                                                      "DataObito"])

# select the confirmed cases, groups by city and saves the ones that surpass N_cases
confirmed = covid_panel[covid_panel['Classificacao'] == 'Confirmados']
confirmed_count = confirmed.groupby('Municipio').size()
confirmed_count[confirmed_count > N_cases].to_csv("../data/N_case_cities.csv")

# -------------------------------------- cases between certain dates --------------------------------------
d1 = date.datetime.strptime(d1, "%Y-%m-%d")
d2 = date.datetime.strptime(d2, "%Y-%m-%d")

# select the confirmed cases between d1 and d2
cases_in_period = confirmed[(confirmed['DataDiagnostico'] >= d1) & (confirmed['DataDiagnostico'] <= d2)]
print(f'Number of cases in period: {cases_in_period.size}', file=metrics)

# ------------------------------- city rank by number of cases between dates -------------------------------
top_cities_in_period = cases_in_period.groupby('Municipio').size().sort_values(ascending=False)
top_cities_in_period.to_csv("../data/top_cities_in_period.csv")

# ------------------------ percentage of hospitalized, dead, hospitalized-then-dead ------------------------
# checks if data from a city or all
confirmed_in_city = confirmed if analize_city == 'ALL' else confirmed[confirmed['Municipio'] == analize_city]

# percentage of confirmed cases that are hospitalized
confirmed_hospitalized = confirmed_in_city[confirmed_in_city['FicouInternado'] == 'Sim']
hospitalized_percentage = confirmed_hospitalized.size / confirmed_in_city.size
print(f'Percentage of hospitalized cases: {hospitalized_percentage.round(4) * 100}%', file=metrics)

# percentage of confirmed cases that died
confirmed_dead = confirmed_in_city[confirmed_in_city['Evolucao'] == 'Óbito pelo COVID-19']
dead_percentage = confirmed_dead.size / confirmed_in_city.size
print(f'Percentage of dead cases: {dead_percentage.round(4) * 100}%', file=metrics)

hospitalized_that_died = confirmed_hospitalized[confirmed_hospitalized['Evolucao'] == 'Óbito pelo COVID-19']
hospitalized_that_died_percentage = hospitalized_that_died.size / confirmed_hospitalized.size
print(f'Percentage of hospitalized cases that died: {hospitalized_that_died_percentage.round(4) * 100}%', file=metrics)

# ------------------ averege, standart deviation and percentage of healthy of dead peopld ------------------
d1_d = date.datetime.strptime(d1_d, "%Y-%m-%d")
d2_d = date.datetime.strptime(d2_d, "%Y-%m-%d")
cases_in_period_of_death = confirmed[(confirmed['DataObito'] >= d1_d) & (confirmed['DataObito'] <= d2_d)]
dead_in_period = cases_in_period_of_death[cases_in_period_of_death['Evolucao'] == 'Óbito pelo COVID-19']

# apply age_to_days to the age column and get the average and standard deviation
age_in_days = dead_in_period['IdadeNaDataNotificacao'].apply(age_to_days)
mean = age_in_days.mean()
deviation = age_in_days.std()

# print age average and standart deviation in years, months and days
print(f'Average age in days: {int(mean // 365)} years, {int((mean % 365) // 30)} months and {int(mean % 365 % 30)} days', file=metrics)
print(f'Standard deviation in days: {int(deviation // 365)} years, {int((deviation % 365) // 30)} months and {int(deviation % 365 % 30)} days', file=metrics)

# calculate percentage of people that died and were healthy
no_comorbidities = dead_in_period[(dead_in_period['ComorbidadePulmao'] == 'Não') & 
                                  (dead_in_period['ComorbidadeCardio'] == 'Não') &
                                  (dead_in_period['ComorbidadeRenal'] == 'Não') &
                                  (dead_in_period['ComorbidadeDiabetes'] == 'Não') &
                                  (dead_in_period['ComorbidadeTabagismo'] == 'Não') &
                                  (dead_in_period['ComorbidadeObesidade'] == 'Não')]
dead_no_comorbidities_percentage = no_comorbidities.size / dead_in_period.size
print(f'Percentage of dead people that had no comorbidities: {dead_no_comorbidities_percentage.round(4) * 100}%', file=metrics)
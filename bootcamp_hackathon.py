# %% Importting modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly_express as px
import requests
import json

url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
data = requests.get(url).json()
sns.set()
# %% Creating initial dataframe from json data
df = pd.DataFrame(data)
# %%
with open("countries.txt", 'w') as f:
    for column in df.columns:
        f.write(f'{df[column].loc["location"]} - {column}')
        f.write("\n")

# %%


def country_data(country_list, country_df) -> dict:
    country_dict = {country: country_df[country].loc["data"] for country
                    in country_list}
    return country_dict


def get_tcpm(dict, country_list):
    tcpm = {country: [covid_dict[country][num]["total_cases_per_million"]
                      for num in range(193)] for country in country_list}
    return tcpm


def get_dates(dict, country_list):
    dates = {country: [covid_dict[country][num]["date"]
                       for num in range(193)] for country in country_list}
    return dates


def create_country_dfs(date_dict, tcpm_dict, country_list):
    mux = pd.MultiIndex.from_product([country_list, ["Dates", "TCPM"]])
    df = pd.DataFrame(data=None, columns=mux)
    for country in country_list:
        df[(country, "Dates")] = date_dict[country]
        df[(country, "TCPM")] = tcpm_dict[country]
    return df


# %%
country_list = ["USA", "GBR", "OWID_WRL", "KOR", "CHN"]
country_df = df[country_list]
covid_dict = country_data(country_list, country_df)
total_cases_per_million, dates = (
    get_tcpm(covid_dict, country_list), get_dates(covid_dict, country_list))
country_data = create_country_dfs(dates, total_cases_per_million, country_list)
# %%
gap = px.data.gapminder()

px.line(df, animation_frame="Dates")

# %%

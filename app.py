import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
from dash.dependencies import Input, Output
from config import API_KEY
from utils import kelvin2celsius, epoch2time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
cities = defaultWeatherImg = None


def load_data():
    global cities, defaultWeatherImg

    cities = ['Barranquilla', 'Bogota', 'London', 'Tokyo',
              'Amsterdam', 'Miami', 'Portland', 'Santiago']
    defaultWeatherImg = {
        'Clear': 'https://d25rq8gxcq0p71.cloudfront.net/dictionary-images/324/sunny.jpg',
        'Clouds': 'https://i.insider.com/57854a5088e4a70f018b7940?width=1100&format=jpeg&auto=webp',
        'Rain': 'https://portugalinews.eu/wp-content/uploads/2019/02/weather.jpg'
    }


def get_city_data(city):
    currentTemp = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}')
    temphistory = requests.get(
        f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}')
    return (currentTemp.json(), temphistory.json())


def create_graph(forecast):
    time = []
    temperatures = []
    for val in forecast:
        time.append(epoch2time(val['dt']))
        temperatures.append(kelvin2celsius(val['main']['temp']))
    df = pd.DataFrame({'time': time, 'temp': temperatures})
    return px.line(df, x="time", y="temp")


def load_style():
    app.layout = html.Div(
        [
            dbc.Row(dbc.Col(
                    html.Div(" "),
                    width={'size': 12})
                    ),
            dbc.Row(
                dbc.Col(
                    html.H1("¿Hola Mundo?"),
                    width={'offset': 5}
                )
            ),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=[{'label': value, 'value': value}
                                 for value in cities],
                        className="m-5",
                        value="Barranquilla"),
                    width={'offset': 1, 'size': 3},
                ),
                dbc.Col(
                    html.H3(id="chosen-city", className="m-5"),
                    width={'size': 7}
                )
            ], justify="center"
            ),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(id="card-img", src="", top=True),
                            dbc.CardBody(
                                [
                                    html.H4("", id="card-title",
                                            className="card-title"),
                                    html.P("", id="card-description",
                                           className="card-text")
                                ]
                            )
                        ], style={"width": "18rem"}
                    ), width={'offset': 2},
                ),
                dbc.Col(
                    dcc.Graph(id='graphic-forecast'),
                    width={'offset': 1, 'width': 6}
                )
            ])
        ]
    )

@ app.callback(
    Output('chosen-city', 'children'),
    Output('card-title', 'children'),
    Output('card-description', 'children'),
    Output('card-img', 'src'),
    Output('graphic-forecast', 'figure'),
    Input('city-dropdown', 'value'))
def update_output(value):
    current, history = get_city_data(value)

    temp = kelvin2celsius(current["main"]["temp"])
    weather = current["weather"][0]["main"]
    forecast = history['list']
    
    if weather in defaultWeatherImg:
        img = defaultWeatherImg[weather]
    else: 
        img = defaultWeatherImg['Clear']
    return([
        f'You have chosen {value}',
        value,
        f'The temperature in {value} is at {temp}ºC \n The sky is {weather}',
        img,
        create_graph(forecast)
    ])


if __name__ == "__main__":
    load_data()
    load_style()
    server = app.server
    app.run_server(debug=True)

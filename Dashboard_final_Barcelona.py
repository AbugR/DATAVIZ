from dash import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
import plotly.express as px

###Importing data###

df_rent = pd.read_csv('Barcelona_rent_price.csv')
df_rent = df_rent.loc[df_rent['Year'] < 2021]
df_rent = df_rent.loc[df_rent['Year'] > 2014]
df_rent = df_rent.replace('Gracia', 'Gràcia')
df_rent = df_rent.replace('Sants-Montjuic', 'Sants-Montjuïc')
df_rent = df_rent.replace('Sarria-Sant Gervasi', 'Sarrià-Sant Gervasi')
df_rent = df_rent.replace('Horta-Guinardo', 'Horta-Guinardó')
df_rent = df_rent.replace('Sant Marti', 'Sant Martí')

df_income = pd.read_csv('income_data_barcelona.csv')
df_income.dropna(inplace=True)
df_income.rename(columns={"Any": "Year"}, inplace=True)
df_income['Year'] = df_income['Year'].astype(int)
df_income = df_income.loc[df_income['Nom_Districte'] != "L'Eixample"]

# Defining style
styles = {
    'top_bar': {
        'backgroundColor': '#483322',
        'textAlign': 'left',
        'padding': '1rem',
        'top': '0',
        'left': '0',
        'height': '100%',
        'display': 'inline_block',
        'width': '10%',
        'position': 'fixed'
    },

    'box_flex': {
        'background-color': '#D6C6B7',
        'color': '#D6C6B7',
        'marginBottom': '20px',
        'display': 'flex',
    },
    'box_graph': {
        'background-color': '#D6C6B7',
        'width': '100%',

    }

}

# Static Graphs
# create stacked bar chart

stacked_bar_df_rent = df_rent.loc[df_rent['Average _rent'] == 'average rent (euro/month)']
stacked_bar_df_income = df_income

income_bar = stacked_bar_df_income[['Year', 'Import_Renda_Bruta']].groupby('Year').mean()['Import_Renda_Bruta'] / 12
rent_bar = stacked_bar_df_rent[['Year', 'Price']].groupby('Year').mean()['Price']
data_rent = (rent_bar / income_bar) * 100
data_income = (income_bar / income_bar) * 100

rent_labels = [f'{val:.1f}%' for val in data_rent.values]

stack_bar_graph = go.Figure(data=[
    go.Bar(name='Income', x=data_income.index, y=data_income.values, base=0, marker=dict(color='#74913b')),
    go.Bar(name='Rent', x=data_rent.index, y=data_rent.values, base=0,
           text=rent_labels, textposition='inside', marker=dict(color='#cc7a00'))
])

stack_bar_graph.update_layout(
    title='Rents Weight on Average Salary Through the Years',
    title_x=0.5,
    xaxis_title='Year',
    yaxis_title='Percentage (%)',
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='sans-serif', size=18, color='#483322'),
    title_font=dict(family='sans-serif', size=18,color='#483322'),
    title_font_size=28,
    title_font_color='#483322',
    title_font_family='sans-serif',
    margin=dict(l=50, r=50, b=50, t=120, pad=4)
)

stack_bar_graph.update_xaxes(title_text='Year')
stack_bar_graph.update_yaxes(title_text='Percentage (%)')

# Components

radio_items = dcc.RadioItems(
    id='year-radio',
    options=[
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018},
        {'label': '2019', 'value': 2019},
        {'label': '2020', 'value': 2020}
    ],
    value=2015,
    labelStyle={'display': 'inline-block', 'padding': '10px 20px'},
    inputStyle={'margin-right': '10px'},
    style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'font-family': 'sans-serif'}
)

dropdown_district = dcc.Dropdown(id='dropdown-district',
                                 clearable=False,
                                 searchable=False,
                                 options=[{'label': 'Barcelona', 'value': 'Barcelona'},
                                          {'label': 'Ciutat Vella', 'value': 'Ciutat Vella'},
                                          {'label': 'Eixample', 'value': 'Eixample'},
                                          {'label': 'Sants-Montjuïc', 'value': 'Sants-Montjuïc'},
                                          {'label': 'Les Corts', 'value': 'Les Corts'},
                                          {'label': 'Gracià', 'value': 'Gràcia'},
                                          {'label': 'Horta-Guinardó', 'value': 'Horta-Guinardó'},
                                          {'label': 'Nou Barris', 'value': 'Nou Barris'},
                                          {'label': 'Sant Andreu', 'value': 'Sant Andreu'},
                                          {'label': 'Sant Martí', 'value': 'Sant Martí'},
                                          {'label': 'Sarrià-Sant Gervasi', 'value': 'Sarrià-Sant Gervasi'}],
                                 value='Barcelona',
                                 style={'margin': '4px', 'box-shadow': '0px 0px #483322', 'border-color': '#483322', 'font-family': 'sans-serif'})

dropdown_month_or_m2 = dcc.Dropdown(id='dropdown-month/m2',
                                    clearable=False,
                                    searchable=False,
                                    options=[{'label': 'Month', 'value': 'month'},
                                             {'label': 'Square Meter', 'value': 'square_meter'}],
                                    value='month',
                                    style={'margin': '4px', 'box-shadow': '0px 0px #483322', 'border-color': '#483322', 'font-family':  'sans-serif'})

###############################
# Define the dashboard layout #
###############################

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Heading', style={'color': 'rgb(214, 198, 183)','backgroundColor': 'rgb(214, 198, 183)'}),
    # Create the side_bar
    html.Div([
        html.Div([
            html.H1('Barcelona Rent and Income Dashboard',
                    style={'color': 'rgb(249, 241, 215)'}),
            html.Label(
                'We aim to explore the evolution in rent prices and average incomes in Barcelona, Spain.'
                ' This dashboard allows for both a more general or more specific analysis, bringing relevant insights about a relevant theme  a simple way.',
                style={'color': 'rgb(197, 187, 177)', 'font-family':  'sans-serif'}),
        ]),

            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            html.Label(
                'Afonso Ramos, R20181134',
                style={'color': 'rgb(197, 187, 177)',
                       'font-family':  'sans-serif',
                       'font-size': '14px'}),
            html.Br(),
            html.Br(),

            html.Label(
            'Beatriz Gonçalves, M20210319',
            style={'color': 'rgb(197, 187, 177)',
                   'font-family': 'sans-serif',
                   'font-size': '14px'}),
            html.Br(),
            html.Br(),

            html.Label(
            'Helena Morais, M20210636',
            style={'color': 'rgb(197, 187, 177)',
                   'font-family': 'sans-serif',
                   'font-size': '14px'}),
            html.Br(),
            html.Br(),

            html.Label(
            'Ricardo Sequeira, M20210623',
            style={'color': 'rgb(197, 187, 177)',
                   'font-family': 'sans-serif',
                   'font-size': '14px'}),

    ], style=styles['top_bar']),

    html.Div([
        html.Div([
            html.Div([
                html.H2('General view - Select a year:', style={ 'font-size': '22px','textAlign': 'center', 'font-family':  'sans-serif'}),
                radio_items
            ]),
            html.Div([
                html.Div([
                    html.H2(id='title_1st', style={'textAlign': 'center'}),
                    # choropleth map
                    dcc.Graph(id='cloro_map')
                ], style={'width': '60%','margin-right': '25px'}),
                html.Div([
                    # bar chart com income
                    html.H2(id='title_2nd', style={'textAlign': 'center'}),
                    dcc.Graph(id='bar_plot')
                ], style={'width': '38%'}),
            ], style=styles['box_flex']),
        ]),
        html.Div([
            html.Div([
                # titulo
                html.H4(
                    'Districts through time - Select a district in Barcelona:',
                    style={
                        'font-size': '22px',
                        'margin-top': '20px',
                        'margin-bottom': '10px',
                        'color': 'black',
                        'text-align': 'center',
                        'font-family': 'sans-serif'
                    }
                )
                ,
                html.Br(),
                # slider_year,
                dropdown_district,
                dropdown_month_or_m2,
            ], style={'width': '99%','display': 'inline-block'}),

        ], style=styles['box_flex']),
        html.Div([
            html.Div([
                dcc.Graph(id='income-graph', style=styles['box_graph'])
            ], style={'width': '33%'}),
            html.Div([
                dcc.Graph(id='rent-graph', style=styles['box_graph'])
            ], style={'width': '33%'}),

            html.Div([
                dcc.Graph(id='percentage-graph', style=styles['box_graph'])
            ], style={'width': '33%'}),

        ], style=styles['box_flex']),
        html.Div([

            # stack bar estático
            dcc.Graph(figure=stack_bar_graph)
        ], style={'width': '99%'}),

    ], style={'padding-left': '12%'})

], style={'background-color': 'rgb(214, 198, 183)'})


#################
# App callbacks #
#################
@app.callback(
    [
        Output("cloro_map", "figure"),
        Output("title_1st", "children"),
        Output("bar_plot", "figure"),
        Output("title_2nd", "children")
    ],
    [
        Input("year-radio", "value")
    ])
def update_cloro_map(year):

    # Filter data for year and average rent
    cloro_df_rent = df_rent.loc[(df_rent['Year'] == year) & (df_rent['Average _rent'] == 'average rent (euro/month)')]

    # Create choropleth map
    fig_cloro_map = px.choropleth_mapbox(cloro_df_rent,
                                         geojson='https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.geojson',
                                         locations='District', color='Price',
                                         featureidkey='properties.NOM',
                                         color_continuous_scale='RdYlGn_r',
                                         range_color=(0, 1800),
                                         mapbox_style="carto-positron",
                                         zoom=10.5, center={"lat": 41.38, "lon": 2.16},
                                         opacity=0.5,
                                         labels={'Price': 'Rent in €'}
                                         )

    fig_cloro_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor='#f2f2f2',
        coloraxis_colorbar={
            'title': {'text': 'Rent price (€/m²)'},
            'thicknessmode': 'pixels', 'thickness': 15,
            'lenmode': 'pixels', 'len': 300,
            'x': 0.85, 'y': 0.5
        },
        geo_scope='europe',
        geo_projection={'type': 'conic conformal', 'rotation': {'lon': 2.5, 'lat': 41.38}},
    )

    # Create bar plot
    bar_plot_df = df_income.loc[df_income['Year'] == year]

    values = bar_plot_df[['Nom_Districte', 'Import_Renda_Bruta']].groupby('Nom_Districte').mean()['Import_Renda_Bruta']
    labels = values.index
    data = [go.Bar(x=labels, y=values)]

    # Define the layout
    layout = go.Layout(
        xaxis={
            'title': 'District',
            'automargin': True,
            'tickangle': -45
        },
        yaxis={
            'title': 'Average Gross Income',
            'automargin': True,
            'showgrid': True,
            'gridcolor': 'grey'
        },
        margin={'l': 50, 'r': 50, 't': 50, 'b': 50},
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    data = [
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color='#74913b')  # set the bar color to green
        )
    ]

    # Create the figure
    fig_bar_plot = go.Figure(data=data, layout=layout)
    fig_bar_plot.update_xaxes(title_text='District')
    fig_bar_plot.update_yaxes(title_text='Amount (Euro)')

    title1 = html.H1(children=f'Rent values distribution per Region in {year}',
                     style={
                         'textAlign': 'center',
                         'fontSize': '28px',
                         'color': '#483322'})

    title2 = html.H2(children=f'Average Gross Income per District in {year}',
                     style={
                         'textAlign': 'center',
                         'fontSize': '28px',
                         'color': '#483322',
                         'marginTop': '7px'}),

    return [fig_cloro_map, title1, fig_bar_plot, title2]


#### 2nd graph

@app.callback(
    [
        Output("income-graph", "figure"),
        Output("rent-graph", "figure"),
        Output("percentage-graph", "figure")
    ],
    [
        Input("dropdown-district", "value"),
        Input("dropdown-month/m2", "value"),
    ]
)
def update_income_and_rent(district, month_or_squarem):
    update_df_income = df_income

    if district != 'Barcelona':
        update_df_income = update_df_income.loc[update_df_income['Nom_Districte'] == district]

    axis_x = update_df_income.Year.unique()

    # income
    fig_income = go.Figure()
    fig_income.add_trace(go.Scatter(
        x=axis_x,
        y=update_df_income[['Import_Renda_Bruta', 'Year']].groupby('Year')['Import_Renda_Bruta'].mean() / 12,
        name='Close',
        line=dict(color='black')
    ))

    fig_income.update_layout(
        title={
            'text': f'Average Income per Month in {district}',
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title={
            'text': 'Year',
            'font': {'size': 16}
        },
        yaxis_title={
            'text': 'Income €',
            'font': {'size': 16}
        },
        margin={'l': 50, 'r': 50, 't': 80, 'b': 50},
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # rent

    update_df_rent = df_rent

    if district != 'Barcelona':
        update_df_rent = update_df_rent.loc[update_df_rent['District'] == district]

    if month_or_squarem == 'month':
        string_ = 'average rent (euro/month)'
        type_ = 'Month'
    else:
        string_ = 'average rent per surface (euro/m2)'
        type_ = 'Square Meter'

    fig_rent = go.Figure()
    fig_rent.add_trace(go.Scatter(
        x=axis_x,
        y=update_df_rent[['Price', 'Average _rent', 'Year']].loc[update_df_rent['Average _rent'] == string_].groupby(
            'Year')['Price'].mean(),
        name='Close',
        connectgaps=True,
        line=dict(color='black')
    ))

    fig_rent.update_layout(
        title={
            'text': f'Average Rent Per {type_} in {district}',
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title={
            'text': 'Year',
            'font': {'size': 16}
        },
        yaxis_title={
            'text': 'Rent Price €',
            'font': {'size': 16}
        },
        margin={'l': 50, 'r': 50, 't': 80, 'b': 50},
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # percentage of income spent on rent

    fig_percentage = go.Figure()
    fig_percentage.add_trace(go.Scatter(
        x=axis_x,
        y=(update_df_rent[['Price', 'Average _rent', 'Year']].loc[update_df_rent['Average _rent'] == string_].groupby(
            'Year')['Price'].mean() / (update_df_income[['Import_Renda_Bruta', 'Year']].groupby('Year')[
                                           'Import_Renda_Bruta'].mean() / 12)) * 100,
        name='Close',
        connectgaps=True,
        line=dict(color='black')
    ))

    fig_percentage.update_layout(
        title={
            'text': f'Percentage of Rent/Income in {district} Per Month',
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title={
            'text': 'Year',
            'font': {'size': 16}
        },
        yaxis_title={
            'text': "Percentage %",
            'font': {'size': 16}
        },
        margin={'l': 50, 'r': 50, 't': 80, 'b': 50},
        plot_bgcolor='white',
        paper_bgcolor='white',
    )

    return [fig_income, fig_rent, fig_percentage]


if __name__ == '__main__':
    app.run_server(debug=True)
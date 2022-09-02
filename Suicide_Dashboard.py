# Importing libraries
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

# Read the suicide data
suicide_data = pd.read_csv('master2.csv')

# Print the data
suicide_data.head()

# Null values
suicide_data.isnull().sum()

# Removing null values
suicide_data.drop(['HDI for year'], axis=1, inplace=True)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([
    
    dbc.Row(
    dbc.Col(html.H1("Suicide Interactive Dashboard",
                   className="text-center text-primary mb-4"),
           width=12)
    ),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='mydrop1', multi=False, value='Albania',
                        options=[{'label':x, 'value':x}
                                for x in sorted(suicide_data['country'].unique())],
                        ),
            dcc.Graph(id='line-fig', figure={})
        ], 
            width={'size':5, 'offset':1, 'order':1}
        ),
        
        dbc.Col([
            dcc.Dropdown(id='mydrop2', multi=False, value='male',
                        options=[{'label':x, 'value':x}
                                for x in sorted(suicide_data['sex'].unique())],
                        ),
            dcc.Graph(id='line-fig2', figure={})
        ],
            width={'size':5, 'offset':0, 'order':2}
        ),

    ], justify='start'),


    dbc.Row([
        dbc.Col([
            html.P("Worldwide data for different age groups",
            className="text-center text-dark mb-4"),
            dcc.Checklist(id='mycheck1', value=['75+ years'],
            options=[{'label':x, 'value':x}
            for x in sorted(suicide_data['age'].unique())]),
            dcc.Graph(id='worldmap2',figure={}),
        ],
        ),

    ],
    ),

    dbc.Row([
        dbc.Col([
            html.P('Bar chart for country-wise suicide data for each age groups',
            className='text-center text-dark mb-4'),
            dcc.Dropdown(id='mydrop4', multi=False, value='Austria',
            options=[{'label':x, 'value':x}
            for x in sorted(suicide_data['country'].unique())]),
            dcc.Graph(id='worldmap3', figure={}),
        ],
        ),

        dbc.Col([
            html.P('Pie chart for country-wise suicide data for each age groups',
            className='text-center text-dark mb-4'),
            dcc.Dropdown(id='mydrop5', multi=False, value='Austria',
            options=[{'label':x, 'value':x}
            for x in sorted(suicide_data['country'].unique())]),
            dcc.Graph(id='pie1', figure={}),
        ],
        ),

    ],
    ),

    dbc.Row([
        dbc.Col([
            html.P('Suicide percentage 1985-2016',
            className='text-center text-dark mb-4'),

            dcc.Graph(
                id='example',figure=px.pie(suicide_data_bar, values='suicides_no', names='year', template="ggplot2")
            )
        ],
            width={'size':5, 'offset':1, 'order':1}
        ),
        dbc.Col([
            html.P('Suicide pie chart for male and female',
            className='text-center text-dark'),

            dcc.Graph(
                id='example2', figure=px.pie(suicide_data_bar, values='suicides_no', names='sex',template="ggplot2")
            )
        ],

            width={'size':5, 'offset':0, 'order':2}
        ),
    ],
    ),

    dbc.Row([
        dbc.Col([
            html.P('Suicides by country',
            className='text-center text-dark'),

            dcc.Graph(
                id='worldmap',figure=px.choropleth(data_frame=worldmap, locations='country', color='suicides_no', locationmode='country names',
                hover_name='country', 
                    color_continuous_scale=px.colors.sequential.Plasma)
            )
        ],
        width={'size':30})
    ],
    ),

    dbc.Row([
        dbc.Col([
            html.P("Suicide for each contient for M and F",
                   className="text-center text-dark mb-4"),

           dcc.Graph(
            id='bar1', figure=px.bar(suicide_data.groupby(['continent','sex'], as_index=False)['suicides_no'].sum(), x='continent', y='suicides_no', color='sex', barmode='group', template='ggplot2')
           )
        ],
        ),
        dbc.Col([
            html.P("Suicide for each continent for all age groups",
                   className="text-center text-dark mb-4"),
                   
                   dcc.Graph(
                    id='bar2', figure=px.bar(suicide_data.groupby(['continent','age'],as_index=False)['suicides_no'].sum(), x='continent', y='suicides_no', color='age', barmode='group', template='ggplot2')
                   )
        ],
        ),
    ],
    ),


    dbc.Row([
        dbc.Col([
            html.P('World suicides by age',
            className='text-center text-dark'),

            dcc.Dropdown(id='mydrop3',multi=True, value=['15-24 years','35-54 years'],
            options=[{'label':x, 'value':x}
            for x in suicide_data['age'].unique()],
            ),
            dcc.Graph(id='line-fig3', figure={})
        ],
            width={'size':5, 'offset':1, 'order':1}
        ),
        dbc.Col([
            html.P('World suicides per year',
            className='text-center text-dark'),

            dcc.Graph(
                id='example3', figure=px.line(suicide_data.groupby(['year'],as_index=False)['suicides_no'].sum(),x='year', y='suicides_no', template="ggplot2",markers=True)
            )
        ],
            width={'size':5, 'offset':0, 'order':2}
        )
    ]
    )

], fluid=True)

@app.callback(
    Output('line-fig', 'figure'),
    Input('mydrop1', 'value')
)
def update_graph(stock_slctd):
    temp = suicide_data.groupby(['country','age','year'], as_index=False)['suicides_no'].sum()
    dff = temp[temp['country']==stock_slctd]
    figln = px.line(dff, x='year', y='suicides_no', color='age', template="ggplot2")
    figln.update_layout(title_text='Total suicides per country',title_x=0.5)
    return figln


@app.callback(
    Output('line-fig2', 'figure'),
    Input('mydrop2', 'value')
)
def update_graph(stock_slctd):
    dff = tempg[tempg['sex']==stock_slctd]
    figln2 = px.line(dff, x='year', y='suicides_no', markers=True,template="ggplot2")
    figln2.update_layout(title_text='Suicide data for male and female', title_x=0.5)
    return figln2

@app.callback(
    Output('worldmap2','figure'),
    Input('mycheck1','value')
)
def update_graph(stock_slctd):
    tempo = suicide_data.groupby(['country','age'],as_index=False)['suicides_no'].sum()
    dff = tempo[tempo['age'].isin(stock_slctd)]
    figmap = px.choropleth(data_frame=dff, locations='country', color='suicides_no', locationmode='country names',
                hover_name='country', 
                    color_continuous_scale=px.colors.sequential.Plasma)
    return figmap

@app.callback(
    Output('worldmap3', 'figure'),
    Input('mydrop4', 'value')
)
def update_graph(stock_slctd):
    tempo = suicide_data.groupby(['country','age'], as_index=False)['suicides_no'].sum()
    dff = tempo[tempo['country']==stock_slctd]
    figwrld = px.bar(dff, x='age', y='suicides_no', barmode='group', template='ggplot2')
    return figwrld

@app.callback(
    Output('pie1', 'figure'),
    Input('mydrop5', 'value')
)
def update_graph(stock_slctd):
    tempo = suicide_data.groupby(['country','age'], as_index=False)['suicides_no'].sum()
    dff = tempo[tempo['country']==stock_slctd]
    figwrld = px.pie(dff, values='suicides_no', names='age',template="ggplot2")
    return figwrld

@app.callback(
    Output('line-fig3','figure'),
    Input('mydrop3','value')
)
def update_graph(stock_slctd):
    temp = pd.DataFrame(suicide_data.groupby(['year','age'],as_index=False)['suicides_no'].sum())
    dff = temp[temp['age'].isin(stock_slctd)]
    figln3 = px.line(dff, x='year', y='suicides_no', color='age',markers=True, template="ggplot2")
    return figln3


# Run the application
if __name__ == '__main__':
    app.run_server()
    
tempg = suicide_data.groupby(['year','sex'],as_index=False)['suicides_no'].sum()

temp2 = suicide_data.groupby(['year'],as_index=False)['suicides_no'].sum()

worldmap = suicide_data.groupby('country', as_index=False)['suicides_no'].sum()

suicide_data_bar = pd.DataFrame(suicide_data.groupby(['continent','age','sex','year'],as_index=False)['suicides_no'].sum())

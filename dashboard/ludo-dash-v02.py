import pandas as pd
import numpy as np
import dash
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pickle

# Load extra layouts
# cyto.load_extra_layouts()

meeples = 'https://mykindofmeeple.com/wp-content/uploads/2019/01/many-meeples-1602-27042020.jpg'

with open('../nodes/artists-nodesfile.data', 'rb') as filehandle:
    # read the data as binary data stream
    nodes = pickle.load(filehandle)


with open('../edges/artist-edgesfile.data', 'rb') as filehandle:
    # read the data as binary data stream
    edges = pickle.load(filehandle)


elm_list = nodes + edges

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#000000',
            'label': 'data(label)',
            'width': "data(node_size)",
            'height': "data(node_size)",
            'font-size': '5px'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'opacity': 0.8,
            'width':0.2
        }
    },
    {
        'selector': '[dominio *= "Expert"]',
        'style': {
            'background-color': '#FF4136'
        }
    },
    {
        'selector': '[dominio *= "Familiares"]',
        'style': {
            'background-color': '#1F8C1D'
        }
    },
    {
        'selector': '[dominio *= "Infantis"]',
        'style': {
            'background-color': '#F0D112'
        }
    }
]

app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            cyto.Cytoscape(
                id='ludo-net',
                minZoom=0.2,
                maxZoom=5,
                layout={'name': 'grid'},
                stylesheet=default_stylesheet,
                elements=elm_list
            ),
            width = {"size":5, "offset": 1}
        ),
        dbc.Col([
            dbc.Card([
                dbc.CardImg(id ="ludoteca",
                    src="https://www.ludopedia.com.br/images/ludo-logo-mascote.png"),
                dbc.CardBody([
                    html.H6(["Made with ",
                             html.A('Dash', href = 'https://dash.plotly.com/',
                                style={'color':'#000000'},
                                target = '_blank)')],
                        style={'textAlign':'right'}),

                    html.H6("by Bruno Vieira Ribeiro - bruno64bits@gmail.com",
                        style={'textAlign':'right'})
                ])
            ],
            color='secondary',
            inverse=False),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H4("Informações do jogo:"),
                        dbc.CardImg(id ="game-img",
                            src=meeples),
                    ],
                    color='secondary',
                    inverse=False,
                    style={"width": "10rem"})
                ], width = {"size":2}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.P(id='game-info',
                                children ="Clique em um nó."),
                        ])
                    ],
                    color='secondary',
                    inverse=False,
                    )
                ], width = {"size":8, "offset": 2})
            ]),
            html.Hr(),
            dbc.Row([
                html.H4(id='edge-artists')
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(id ="nodeA"),
                    ],
                    color='secondary',
                    inverse=False,
                    style={"width": "10rem"})
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(id ="nodeB"),
                    ],
                    color='secondary',
                    inverse=False,
                    style={"width": "10rem"})
                ),
            ])
            ],
        width = {"size":5, "offset": 1}
        )
    ]),

    html.Hr(),

])

@app.callback(
    Output('game-img', 'src'),
    Output('game-info','children'),
    Input('ludo-net','tapNodeData'),
)
def update_layout(tap_node):
    # print(tap_node)
    # print(tap_edge)
    if not tap_node:
        return meeples, "Clique em um nó."

    return (tap_node['img-src'],
            [html.Strong('Título: '),tap_node['title'], html.Br(),
             html.Strong('Ano: '), tap_node['year'], html.Br(),
             html.Strong('Idade recomendada: '), tap_node['age'], html.Br(),
             html.Strong('Jogadores: '), tap_node['players'], html.Br(),
             html.Strong('Tempo de jogo: '), tap_node['time'], 'min', html.Br(),
             html.Strong('Nota (ludopedia): '), tap_node['notarank'], html.Br(),
             html.Strong('Domínio: '), tap_node['dominio'], html.Br(),
             html.Strong('Conexões: '), str(tap_node['conns']), html.Br(),
             ]
           )

@app.callback(
    Output('edge-artists','children'),
    Input('ludo-net','tapEdgeData')
)
def update_layout(tap_edge):
    if not tap_edge:
        return "Clique em um vértice"
    return [html.Strong('Artistas em comum: '), tap_edge['shared']]


@app.callback(
    Output('ludo-net','stylesheet'),
    Input('ludo-net','tapNodeData')
)
def generate_stylesheet(tap_node):
    if not tap_node:
        return default_stylesheet

    # stylesheet = default_stylesheet.copy()

    if tap_node:
        stylesheet = default_stylesheet.copy()
        for edge in tap_node['edges']:
            # print(edge)
            stylesheet.append({
                "selector": 'node[id= "{}"]'.format(edge),
                "style": {
                    'background-color': '#C84DBF',
                    'opacity': 0.9,
                    'width': 15,
                    'height': 15,
                    'shape': 'star'
                }
            })
            if int(tap_node['id']) < int(edge):
                edge_id = tap_node['id']+'-'+edge
            else:
                edge_id = edge+'-'+tap_node['id']
            stylesheet.append({
                "selector": '#{}'.format(edge_id),
                "style":{
                    'opacity': 1,
                    'width':1,
                    'line-color': '#C84DBF'
                }
            })


    return stylesheet

@app.callback(
    Output('nodeA','src'),
    Output('nodeB','src'),
    Input('ludo-net','tapEdgeData')
)
def print_nodes(tap_edge):
    if not tap_edge:
        return meeples, meeples
    nodeA = tap_edge['id'].split('-')[0]
    nodeB = tap_edge['id'].split('-')[1]
    # Getting image-url for each node
    getNodeA = next((sub for sub in nodes if sub['data']['id'] == nodeA), None)
    imgA = str(getNodeA['data']['img-src'])
    getNodeB = next((sub for sub in nodes if sub['data']['id'] == nodeB), None)
    imgB = str(getNodeB['data']['img-src'])
    return imgA, imgB


if __name__ == '__main__':
    app.run_server(debug=True)

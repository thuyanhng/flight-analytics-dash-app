import dash_table

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from data import (sankeyall, intranktab)

from staticFig import fig7

appMenu = html.Div([
    dbc.Row(
        dbc.Col(
            html.I(
                style={"font-size": "16px", "opacity": "70%"},
                children="Select year and indicator to view the result accordingly. "
                         "Click on graphs for more detailed information.",
            )
        )
    ),
    dbc.Row(html.Br()),
    dbc.Row(
        dbc.Col(
            html.H4(style={'text-align': 'center'}, children='Select year:'),
            xs={"size": "auto", "offset": 0},
            sm={"size": "auto", "offset": 0},
            md={"size": "auto", "offset": 3},
            lg={"size": "auto", "offset": 0},
            xl={"size": "auto", "offset": 0},
        ),
    ),
    dbc.Row(
        dbc.Col(
            dcc.Slider(
                id='menu-slidery',
                min=sankeyall['flty'].min(),
                max=sankeyall['flty'].max(),
                value=sankeyall['flty'].min(),
                marks={str(year): str(year) for year in sankeyall['flty'].unique()},
                step=None
            )
        ), style={'font-size': '150%'},
    ),
    dbc.Row(
        dbc.Col(
            html.P(
                style={"font-size": "16px", "opacity": "70%"},
                children="Adjust slider to desired year.",
            )
        )
    ),
    dbc.Row(html.Br()),
    dbc.Row(
        [
            dbc.Col(
                html.H4(style={'text-align': 'center'}, children='Select key indicator:'),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": "auto", "offset": 3},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
            ),
            # Key indicator selection for fig1ovv, fig8,10dom, maybe fig12int
            dbc.Col(
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "16px",
                        "width": "300px",
                        # "display": "block",
                        # "position": "relative",

                    },
                    id='menu-keyind',
                    # options=[{'label': inddict[s], 'value': s} for s in indicator3],
                    # value=indicator3[0],
                    clearable=False,
                ),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": "auto", "offset": 0},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
            ),
        ],
        form=True,
    ),
    dbc.Row(html.Br()),
], className='menu')

extendedInd = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.H4(style={'text-align': 'center'}, children='Select indicator:'),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": "auto", "offset": 3},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
                align='center',
            ),
            # Key indicator selection for fig5, fig6int, fig9, fig11dom
            dbc.Col(
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "16px",
                        # "display": "block",
                        # "position": "relative",
                        "width": "350px",
                    },
                    id='extend-ind',
                    # options=[{'label': inddict[s], 'value': s} for s in indicator3],
                    # value=indicator3[0],
                    clearable=False,
                ),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": "auto", "offset": 0},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
                align='center',
            ),
        ],
        form=True,
    ),
], className='menu')

ovvLayout = html.Div([
    dbc.Row(dbc.Col(html.H2(children='OVERVIEW: FLIGHT NETWORK')), justify='center'),
    dbc.Row(html.Br()),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Change the year or the indicator above to view another aspect of the analysis."
    ), ), align='center', ),
    # Sankey Fig1
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='ovvfig1-sankey',
                      style={"height": "500px"},
                      config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Bubble size represents the volume of flights. "
                 "Click on the graph area and hove the mouse over bubbles to view information."
    ), ), align='center', ),
    # Bubble Fig2 (scatter) pax-rev each country
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='ovvfig2-bubble', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),

    # Subplot horizontal 2 pie chart
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='ovvfig3-sub2pie',
                      config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H4(style={'text-align': 'center'}, children='Select region:'),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": "auto", "offset": 3},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
                align='center',
            ),
            # Region selection for fig 4 (sub 3 line chart vertically)
            dbc.Col(
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "16px",
                        # "display": "block",
                        # "position": "relative",
                        "width": "350px",
                    },
                    id='ovv-sub3linereg',
                    clearable=False,
                ),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": "auto", "offset": 0},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
                align='center',
            ),
        ], justify='center',
        form=True,
    ),
    # Subplot vertical 3 line chart
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='ovvfig4-sub3line', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
], className='app-page')

intLayout1 = html.Div([
    dbc.Row(dbc.Col(html.H2(children='COUNTRY LEVEL ANALYSIS'))),
    # Int Tab1: Ranking table int country - all indicator
    dbc.Row(dbc.Col(
        html.H5(children='Ranking table: International country route by indicators from Jan 2015 to Dec 2019'))),
    dbc.Row(
        dbc.Col(
            html.Div(
                dash_table.DataTable(
                    data=intranktab.to_dict('record'),
                    columns=[{'id': c, 'name': c} for c in intranktab],
                    fixed_rows={'headers': True},
                    style_as_list_view=True,
                    editable=False,
                    style_table={
                        'height': 300,
                        'overflowX': 'auto'
                    },
                    style_header={"backgroundColor": "#f8f5f0", "fontWeight": "bold"},
                    style_cell={'height': 'auto', 'textAlign': 'center', 'padding': '8px',
                                'minWidth': '90px', 'width': '90px', 'maxWidth': '90px',
                                'whiteSpace': 'normal'},
                )),
            xs={"size": "auto", "offset": 0},
            sm={"size": "auto", "offset": 0},
            md={"size": 7, "offset": 0},
            lg={"size": "auto", "offset": 0},
            xl={"size": "auto", "offset": 0},
        ),
        justify='center',
    ),
    # Int Fig12 Fig13: Bar chart top down country & departure airport
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='intfig12-barctr', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Change the year in the slider above to view the result accordingly."
    ), ), align='center', ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='intfig13-bara', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
], className='app-page')

intLayout2 = html.Div([
    # Int Fig5: Timeline country route comparison by indicator

    dbc.Row(
        dbc.Col(
            html.P(
                style={"font-size": "16px", "opacity": "70%"},
                children="""
                    This indicator selection affects two graphs below."""
            )
        )
    ),
    dbc.Row([
        dbc.Col(
            html.H5(style={'text-align': 'center'}, children='Select countries:'),
            xs={"size": "auto", "offset": 0},
            sm={"size": "auto", "offset": 0},
            md={"size": "auto", "offset": 3},
            lg={"size": "auto", "offset": 0},
            xl={"size": "auto", "offset": 0},
            # align='center',
        ),

        # Fig 5 Timeline countries
        dbc.Col(dbc.DropdownMenu(children=[
            dcc.Checklist(
                style={
                    "text-align": "justify",
                    "font-size": "14px",
                    # "width": "300px",
                    "opacity": "70%",
                    "padding": "10px",
                    "margin-right": "10px"
                },
                id='int-timelinectr',
                labelStyle={'display': 'inline-block',
                            'padding': '2px',
                            'margin-right': '5px'},
                inputStyle={
                    "padding": "5px", }
            )], label='Click to select countries',
        ),
            xs={"size": "12", "offset": 0},
            sm={"size": "12", "offset": 0},
            md={"size": "7", "offset": 0},
            lg={"size": "6", "offset": 0},
            xl={"size": "6", "offset": 0},
            # align='center'
        ),
    ],
        justify='start'),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Select countries to see the performance of those routes. To have the best visual effect of the comparison"
                 ", select no more than 5 countries."
    ), ), align='center', ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='intfig5-timeline', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    # Int Fig6: TSA yearline specific country

    dbc.Row([
        dbc.Col(
            html.H5(style={'text-align': 'center'}, children='Select country:'),
            xs={"size": "auto", "offset": 0},
            sm={"size": "auto", "offset": 0},
            md={"size": "auto", "offset": 3},
            lg={"size": "auto", "offset": 0},
            xl={"size": "auto", "offset": 0},
        ),
        dbc.Col(
            dcc.Dropdown(
                style={
                    "text-align": "justify",
                    "font-size": "16px",
                    # "display": "block",
                    # "position": "relative",
                },
                id='int-tsactr',
                placeholder='Select a country',
                clearable=False
            ),
            xs={"size": "12", "offset": 0},
            sm={"size": "12", "offset": 0},
            md={"size": "7", "offset": 0},
            lg={"size": "6", "offset": 0},
            xl={"size": "6", "offset": 0},
        ), ],
        align='start'),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Select country to see its seasonal analysis."
    ), ), align='center', ),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Change the indicator to view another aspect of the analysis."
    ), ), align='center', ),
    # Fig 6 TSA country selection
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='intfig6-tsa', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    dbc.Row(html.Div(html.B(style={"font-size": "16px", "opacity": "70%"}, children="Peak season:"))),
    dbc.Row(html.Div(html.Li(style={"font-size": "16px", "opacity": "70%"}, id='highestm-ctr'))),
    dbc.Row(html.Div(html.Li(style={"font-size": "16px", "opacity": "70%"}, id='shighestm-ctr'))),
    dbc.Row(html.Div(html.B(style={"font-size": "16px", "opacity": "70%"}, children="Low season:"))),
    dbc.Row(html.Div(html.Li(style={"font-size": "16px", "opacity": "70%"}, id='lowestm-ctr'))),
    dbc.Row(html.Br()),
], className='app-page')

domLayout1 = html.Div([
    dbc.Row(html.H2(children='ROUTE ANALYSIS')),
    # Fig 8+ 10: Ind & Year selection

    dbc.Row(
        dbc.Col(
            dcc.Graph(id='domfig8-barroute', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Change the year in the slider above to view the result accordingly."
    ), ), align='center', ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='domfig10-bara', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    # Dom Fig7: Gantt chart active domestic route
    dbc.Row(
        dbc.Col(
            dcc.Graph(
                id='domfig7-gantt',
                config={"displayModeBar": False},
                figure=fig7
            )
        )
    ),
], className='app-page')

domLayout2 = html.Div([
    # Dom Fig9: Timeline domestic route comparison by indicator
    dbc.Row(
        dbc.Col(
            html.P(
                style={"font-size": "16px", "opacity": "70%"},
                children="""
                        This indicator selection affects two graphs below."""
            )
        )
    ),
    dbc.Row([
        dbc.Col(
            html.H5(style={'text-align': 'center'}, children='Select routes:'),
            xs={"size": "auto", "offset": 0},
            sm={"size": "auto", "offset": 0},
            md={"size": "auto", "offset": 3},
            lg={"size": "auto", "offset": 0},
            xl={"size": "auto", "offset": 0},
        ),
        dbc.Col(dbc.DropdownMenu(children=[
            dcc.Checklist(
                style={
                    "text-align": "justify",
                    "font-size": "14px",
                    # "width": "300px",
                    "opacity": "70%",
                    "padding": "10px",
                    "margin-right": "10px"
                },
                id='dom-timelinedomr',
                labelStyle={'display': 'inline-block',
                            'padding': '2px',
                            'margin-right': '5px'},
                inputStyle={
                    "padding": "5px", }
            )], label='Click to select routes',
        ),
            xs={"size": "12", "offset": 0},
            sm={"size": "12", "offset": 0},
            md={"size": "7", "offset": 0},
            lg={"size": "6", "offset": 0},
            xl={"size": "6", "offset": 0},
        ),
    ],
        align='start'),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Select routes to see the performance in those routes. To have the best visual effect of the comparison"
                 ", select no more than 5 routes."
    ), ), align='center', ),
    # Fig 9 Timeline domestic routes selection
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='domfig9-timeline', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    # Dom Fig11: TSA seasonal yearline specific domestic round route

    # Fig 11 dom TSA route selection
    dbc.Row([
        dbc.Col(
            html.H5(style={'text-align': 'center'}, children='Select route:'),
            xs={"size": "auto", "offset": 0},
            sm={"size": "auto", "offset": 0},
            md={"size": "auto", "offset": 3},
            lg={"size": "auto", "offset": 0},
            xl={"size": "auto", "offset": 0},
        ),
        dbc.Col(
            dcc.Dropdown(
                style={
                    "text-align": "justify",
                    "font-size": "14px",
                    "display": "block",
                    "position": "relative",
                },
                id='dom-tsadomr',
                placeholder='Select a domestic route',
                clearable=False,
            ),
            xs={"size": "12", "offset": 0},
            sm={"size": "12", "offset": 0},
            md={"size": "12", "offset": 0},
            lg={"size": "8", "offset": 0},
            xl={"size": "8", "offset": 0},
        ),
    ],
        align='start'),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Select route to see its seasonal analysis."
    ), ), align='center', ),
    dbc.Row(dbc.Col(html.I(
        style={"font-size": "14px", "opacity": "70%"},
        children="Change the indicator to view another aspect of the analysis."
    ), ), align='center', ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='domfig11-tsa', config={"displayModeBar": False}),
            xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 12, "offset": 0},
        )
    ),
    dbc.Row(html.Div(html.B(style={"font-size": "16px", "opacity": "70%"}, children="Peak season:"))),
    dbc.Row(html.Div(html.Li(style={"font-size": "16px", "opacity": "70%"}, id='highestm-domr'))),
    dbc.Row(html.Div(html.Li(style={"font-size": "16px", "opacity": "70%"}, id='shighestm-domr'))),
    dbc.Row(html.Div(html.B(style={"font-size": "16px", "opacity": "70%"}, children="Low season:"))),
    dbc.Row(html.Div(html.Li(style={"font-size": "16px", "opacity": "70%"}, id='lowestm-domr'))),
    dbc.Row(html.Br()),
], className='app-page')

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks

from app import app

import callbacks
from app import srv as server
from layouts import (appMenu, extendedInd, ovvLayout, intLayout1, intLayout2, domLayout1, domLayout2)

app_name = os.getenv("DASH_APP_PATH", "/flight-network-analysis")

# Layout variables, navbar, header, content, and container
nav = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/logo-only.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("Home", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href=f'{app_name}',
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0,
                              className='ms-auto'),
            dbc.Collapse(
                dbc.Nav(
                    [dbc.NavItem(dbc.NavLink("Overview Flight Network", href=f"{app_name}/overview", style={'font-size': '13px'})),
                     dbc.NavItem(dbc.NavLink("Country level analysis", href=f"{app_name}/country", style={'font-size': '13px'})),
                     dbc.NavItem(
                         dbc.NavLink("Route Analysis", href=f"{app_name}/route", style={'font-size': '13px'}), )

                     ],
                    #move nav items to the left side
                    #style={'margin-left': 'auto'},
                    navbar=True,
                    horizontal='end',
                    pills=True,
                    # justified='True',
                ),
                id="navbar-collapse2",
                navbar=True,
                style={'align': 'end'},

            ),

        ],
    ),
    color='light',
    expand='md',
    sticky='top',
    dark=False,
    className="mb-5",
)


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

    # the same function (toggle_navbar_collapse) is used in all three callbacks


app.callback(
    Output(f"navbar-collapse2", "is_open"),
    [Input(f"navbar-toggler2", "n_clicks")],
    [State(f"navbar-collapse2", "is_open")],
)(toggle_navbar_collapse)

header = dbc.Row(
    dbc.Col(
        html.Div(
            html.H1(children="Flight Network Analysis"),

        )
    ),
    className="banner",
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container([header, content])


# Menu callback, set and return
# Declair function  that connects other pages with content to container
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname in ["/", app_name, app_name + "/"]:
        return html.Div(
            [
                dcc.Markdown(
                    """
            ### The Data & Application
            The application is a portfolio project inspired by Dash app Gallery, using Plotly's, faculty.ai's Dash Bootstrap 
            Components and Pandas. The analysis is based on a making up data of operation flight in 2015-2019. 
            The application was designed flexibly and scalably. The data file could be used to connect with a proper database
            server to keep the analysis up to date.

                    """
                ),
                dcc.Markdown(
                    """
                    ### The Analysis
                    The analysis structure includes three main parts:
                    * [Overview:](https://sample-flight-analytics.herokuapp.com/flight-network-analysis/overview) Key indicators performance by regions and countries.
                    * [Country level analysis:](https://sample-flight-analytics.herokuapp.com/flight-network-analysis/country) The performance, the growth and changes through
                    time, the seasonal analysis (peak and low) of each country.
                    * [Route analysis:](https://sample-flight-analytics.herokuapp.com/flight-network-analysis/route) The performance, the growth and changes through
                    time, the seasonal analysis (peak and low) of each route.
                    """
                ),
                dcc.Markdown(
                    """
            The analysis break down flight network performance by indicators, including:
            * Passengers
            * Revenue
            * Flights
            * Others: Load rate, Average revenue per pax, Cargo revenue, Mail revenue, Cargo weight.
        """
                ),
                dcc.Markdown(
                    """
                    **Tips:**
                    * This is an interactive dashboard that shows detailed data in each chart. Click on the graph
                    area and hove the mouse over the plot to see the data.
                    * Number unit converter: 
                        * T (Tera - 1,000,000,000,000): Trillion
                        * G (Giga - 1,000,000,000): Billion
                        * M (Mega - 1,000,000): Million
                        * k (kilo - 1,000): Thousand
                        * m (milli - 0,001): Milli - 0,1%
                    """
                ),
                dcc.Markdown(
                    """
                    ### Screen compatibility
                    The application was designed for medium and large screens, such as tablets, 
                    desktops. Access from mobile could be inappropriate.

                    """
                ),

            ],
            className="home",
        )
    elif pathname.endswith("/overview"):
        return appMenu, ovvLayout
    elif pathname.endswith("/country"):
        return appMenu, intLayout1, extendedInd, intLayout2
    elif pathname.endswith("/route"):
        return appMenu, domLayout1, extendedInd, domLayout2
    else:
        return "ERROR 404: Page not found!"


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([nav, container])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True, port=8286)
# set app server to variable for deployment
srv = app.server

# set app callback exceptions to true
app.config.suppress_callback_exceptions = True

# set application title
app.title = "Flight Network Analytics"

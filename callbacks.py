from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime as dt
from plotly.subplots import make_subplots

from app import app
from data import (sankeyall, ctryear_paxrevflt, regyear_paxrevflt, ctrym_allind, domrouteym_allind,
                  domrouteyear_paxrevflt, intoriayear_paxrevflt, oriayear_paxrevflt, inddict,
                  regioncolors, ctrcolors, domrcolors, indicator3, indicator9)


### callback menu
@app.callback(
    [
        Output('menu-keyind', 'options'),
        Output('menu-keyind', 'value'),
    ],
    [Input('menu-slidery', 'value')]
)
def selection_keyind(slidery):

    keyindopts = [{'label': inddict[k], 'value': k} for k in indicator3]



    return keyindopts, indicator3[0]

@app.callback(
    [
        Output('extend-ind', 'options'),
        Output('extend-ind', 'value')
    ],
    [Input('menu-slidery', 'value')]
)
def selection_keyind(slidery):
    extindopts= [{'label': inddict[e], 'value': e} for e in indicator9]


    return extindopts, indicator9[3]

### OVERVIEW
# Ovv Fig1: Sankey
@app.callback(
    Output('ovvfig1-sankey', 'figure'),
    [Input('menu-slidery', 'value'),
     Input('menu-keyind', 'value')]
)
def ovv_sankey_fig1(ovv_slidery, ovv_sankeyind):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#006666', '#009999', '#0099CC', '#006699', '#CC9900', '#CC9966', '#CC9999',
                    '#CCCCCC', '#CCCC99', '#CCCC66', '#FFCC66', '#FF9900', '#FF6666', '#CC3333',
                    '#999966', '#993366', '#669999', '#666666', '#339999', '#336666', '#CC66CC',
                    '#FFCC00', '#FFCC99', '#996600', '#4B8BBE', '#306998', '#FFE873', '#FFD43B', '#646464',
                    '#999933', '#99CCCC', '#FFCC00']
    df = sankeyall[sankeyall.flty == ovv_slidery]
    cat_cols = ['Network', 'Region', 'country_route']
    value_cols = ovv_sankeyind
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp = list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp

    # remove duplicates from labelList
    # labelList = list(dict.fromkeys(labelList))

    # define colors
    colorList = []
    for idx, colorNum in enumerate(labelList):
        # define colors based on number of levels
        # colorList = colorList + [colorPalette[idx]]*colorNum
        colorList = colorList + [colorPalette[idx]]

    # transform df into a source-target pair
    sourceTargetDf = pd.DataFrame()
    for i in range(len(cat_cols) - 1):
        if i == 0:
            sourceTargetDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            sourceTargetDf.columns = ['source', 'target', 'count']
        else:
            tempDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            tempDf.columns = ['source', 'target', 'count']
            sourceTargetDf = pd.concat([sourceTargetDf, tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source', 'target']).agg({'count': 'sum'}).sort_values(
            by=['source', 'target', 'count'], ascending=False).reset_index()

    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

    # creating the sankey diagram
    node = dict(
        pad=15,
        thickness=80,
        line=dict(
            color="black",
            width=0.5
        ),
        label=labelList,
        color=colorList
    )
    link = dict(
        source=sourceTargetDf['sourceID'],
        target=sourceTargetDf['targetID'],
        value=sourceTargetDf['count']
    )
    fig1 = go.Figure(go.Sankey(link=link, node=node))
    fig1.update_layout(
        title='Flight Network Overview by %s in %s' % (inddict[ovv_sankeyind], str(ovv_slidery)),
        font_size=12
    )
    fig1.update_layout(
        hovermode="x",
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0")

    return fig1


# Ovv Fig2 Bubble
@app.callback(
    Output('ovvfig2-bubble', 'figure'),
    Input('menu-slidery', 'value')
)
def ovv_bubble_fig2(ovv_bubbleyear):
    dfig2 = ctryear_paxrevflt[(ctryear_paxrevflt.flty == ovv_bubbleyear)
        # & (ctryear_paxrevflt.country_route != 'Vietnam')
    ]

    fig2 = px.scatter(dfig2, x='pax_total', y='prev_total',
                      size='flt_count', color='Region', hover_name='country_route',  # text= 'country_route',
                      labels={'pax_total': inddict['pax_total'], 'Region': "<b>Region</b>",
                              'prev_total': inddict['prev_total']},
                      color_discrete_map={k: regioncolors[k] for k in dfig2.Region.unique()},
                      # color_discrete_sequence= px.colors.qualitative.Antique,
                      size_max=55)
    # fig2.update_traces(textposition= 'top left')
    fig2.update_layout(transition_duration= 500)

    fig2.update_traces(hovertemplate="<b>%{hovertext}</b><br>" + "Passengers: %{x:.3s}<br>" +
                                     "Revenue: %{y:.3s}<br>" + "Flights: %{marker.size:.0f}<extra></extra>")
    fig2.update_layout(
        title='Passengers - Revenue performance by country in %s' % (str(ovv_bubbleyear)),
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    fig2.update_layout(
        legend_title_font_size=14)
    fig2.update_xaxes(fixedrange=True)
    fig2.update_yaxes(fixedrange=True)
    return fig2


# Ovv Fig3 Region pie chart
@app.callback(
    Output('ovvfig3-sub2pie', 'figure'),
    Input('menu-slidery', 'value')
)
def ovv_pie_fig3(ovv_pieyear):
    dfig3 = regyear_paxrevflt[regyear_paxrevflt.flty == ovv_pieyear]
    fig3 = make_subplots(rows=1, cols=2,
                         specs=[[{'type': 'domain'}, {'type': 'domain'}]]
                         )
    # Make color :D
    # Opt1: simply drop marker_colors= px.colors.qualitative.Antique inside .add_traces if no need to assign specific color to each criteria
    # Opt2: create dict and maker arg instead of marker_colors:
    crit = dfig3.Region.unique()
    colors = np.array([''] * len(crit), dtype=object)
    for i in np.unique(crit):
        colors[np.where(crit == i)] = regioncolors[str(i)]

    fig3.add_traces(go.Pie(labels=dfig3.Region, values=dfig3.pax_total, textinfo='percent',
                           insidetextorientation='radial',
                           name='total passengers <br>in %s' % (str(ovv_pieyear)),
                           # sort= False,
                           marker={'colors': colors}),
                    1, 1)
    fig3.add_trace(go.Pie(labels=dfig3.Region, values=dfig3.prev_total, textinfo='percent',
                          insidetextorientation='radial',
                          name='total revenue <br>in %s' % (str(ovv_pieyear)),
                          # sort= False,
                          marker={'colors': colors}),
                   1, 2)
    # Use 'hole' to create donut-like
    fig3.update_traces(hole=.4, hoverinfo='label+value',
                       hovertemplate="<b>%{label}</b><br>" + "%{value:.3s}"
                       )
    # fig3.update_layout(transition_duration= 500)
    fig3.update_layout(
        title_text='Passengers - Revenue by Regions in %s' % (str(ovv_pieyear)),
        # Add annotation in the center
        annotations=[dict(text='Passengers', x=0.14, xanchor='left', y=0.5, font_size=15, showarrow=False),
                     dict(text='Revenue', x=0.83, xanchor='right', y=0.5, font_size=15, showarrow=False)],
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1.34),
    )

    return fig3

# Region selection for fig4
@app.callback(
    [Output('ovv-sub3linereg', 'options'),
     Output('ovv-sub3linereg', 'value')],
    Input('menu-slidery', 'value')
)
def ovvfig4_sub3line_regionselect(slidery):
    regiony= sankeyall[sankeyall.flty== slidery]
    regfig4opts = [{'label': reg, 'value': reg} for reg in regiony.Region.unique()]

    return regfig4opts, regiony.Region.unique()[2]

# Ovv Fig4: Subplot 3 bar/line input region selection
@app.callback(
    Output('ovvfig4-sub3line', 'figure'),
    Input('ovv-sub3linereg', 'value')
)
def ovv_stackedbar_fig4(ovv_sub3linereg):
    dfig4 = regyear_paxrevflt[(regyear_paxrevflt.Region == ovv_sub3linereg) &
                              (regyear_paxrevflt.flty != 2020)]
    fig4 = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07)

    fig4.add_traces(go.Scatter(name='Revenue',
                               x=dfig4.flty,
                               y=dfig4.prev_total,
                               mode='lines+markers',
                               marker=dict(color=regioncolors[ovv_sub3linereg]),
                               opacity=1),
                    1, 1)
    fig4.add_traces(go.Scatter(name='Flights',
                               x=dfig4.flty,
                               y=dfig4.flt_count,
                               mode='lines+markers',
                               marker=dict(color=regioncolors[ovv_sub3linereg]),
                               opacity=0.6),
                    2, 1)
    fig4.add_traces(go.Scatter(name='Passengers',
                               x=dfig4.flty,
                               y=dfig4.pax_total,
                               mode='lines+markers',
                               marker=dict(color=regioncolors[ovv_sub3linereg]),
                               opacity=0.3),
                    3, 1)
    fig4.update_xaxes(tickformat="d")
    fig4.update_traces(hovertemplate="%{x}" + ": %{y:.3s}")
    fig4.update_layout(
        title_text='Trendline of revenue, flights & passengers of %s from 2015 to 2019' % (str(ovv_sub3linereg)),
        # Add annotation in the center
        # hovermode= 'x',
        height=720,
        width=1000,
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )

    return fig4


### INTERNATIONAL ROUTE
## IntLayout1:
# Int Tab1: dataTable embedded in layouts
# Int Fig12-13:
@app.callback(
    Output('intfig12-barctr', 'figure'),
    [Input('menu-slidery', 'value'),
     Input('menu-keyind', 'value')]
)
# Int Fig5: Timeline countries comparison
def int_bartopctr_fig12(yearfig12, indfig12):
    dintfig12 = ctryear_paxrevflt[ctryear_paxrevflt.country_route != 'Vietnam']
    dfig12 = dintfig12.loc[dintfig12.flty == yearfig12, ['country_route', indfig12]].sort_values(by=indfig12,
                                                                                                 ascending=False)

    fig12 = go.Figure(
        data=[go.Bar(
            name='International countries',
            x=dfig12.country_route,
            y=dfig12[indfig12],
            marker_color="#AE8F6F",
            opacity=0.8)])
    fig12.update_traces(
        hovertemplate="<b>%{x}</b><br>" + "%s in %s: " % (inddict[indfig12], str(yearfig12)) + "%{y:.3s}<br><extra></extra>",
    )
    fig12.update_layout(
        title="Top down international countries by %s in %s" % (inddict[indfig12], str(yearfig12)),
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    fig12.update_traces(textangle=-60)
    return fig12


@app.callback(
    Output('intfig13-bara', 'figure'),
    [Input('menu-slidery', 'value'),
     Input('menu-keyind', 'value')]
)
def int_bartopdepa_fig13(yearfig13, indfig13):
    dfig13 = intoriayear_paxrevflt.loc[intoriayear_paxrevflt.flty == yearfig13, ['ORI', indfig13]].sort_values(
        by=indfig13, ascending=False)
    dfig13 = dfig13.iloc[:20, :]
    fig13 = go.Figure(
        data=[go.Bar(
            name='International Departure Airport',
            x=dfig13.ORI,
            y=dfig13[indfig13],
            marker_color="#004687",
            opacity=0.8)])
    fig13.update_traces(
        hovertemplate="<b>Depart from %{x}</b><br>" + "%s in %s: " % (
            inddict[indfig13], str(yearfig13)) + "%{y:.3s}<br><extra></extra>",
    )
    fig13.update_layout(
        title="Top 20 international departure airports by %s in %s" % (inddict[indfig13], str(yearfig13)),
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    fig13.update_traces(textangle=-60)
    return fig13


## IntLayout2: fig5, fig6 vs 2 selections ctrs, ctr
@app.callback(
    [
        Output('int-timelinectr', 'options'),
        Output('int-timelinectr', 'value'),
    ],
    [Input('menu-slidery', 'value')]
)
def selection_int_timelinectr(slidery):
    secctrf5 = sankeyall[sankeyall.country_route != 'Vietnam']
    fig5ctropts = [{'label': ctr, 'value': ctr} for ctr in
                   list(secctrf5[secctrf5.flty == slidery]['country_route'].unique())]
    return fig5ctropts, list(secctrf5[secctrf5.flty == slidery]['country_route'].unique())[4:6]


@app.callback(
    Output('intfig5-timeline', 'figure'),
    [Input('int-timelinectr', 'value'),
     Input('extend-ind', 'value')]
)
def int_monthline_fig5(ctrlistfig5, indfig5):
    dfig5 = ctrym_allind[ctrym_allind.country_route.isin(ctrlistfig5)]
    # labely_fig5= inddict[indfig5]

    fig5 = px.line(dfig5, x='flt_ym', y=indfig5,
                   color='country_route',
                   labels={indfig5: inddict[indfig5], 'country_route': "<b>Country</b>",
                           'flt_ym': 'Monthly Timeline'},
                   color_discrete_map={k: ctrcolors[k] for k in ctrlistfig5},
                   title='{} by {} \
                  <br>in Jan2015 - Dec2019</b>'.format(", ".join(ctrlistfig5), inddict[indfig5]))

    fig5.update_xaxes(rangeslider_visible=True,
                      dtick="M1",
                      tickformat="%b\n%Y",  # tickfont=dict(size=10)
                      )
    fig5.update_traces(hovertemplate="<b>%{x}</b><br>" + "%s: " % (inddict[indfig5]) + "%{y:.3s}<br>")
    # fig5.update_layout(legend_title_font_size=14)
    fig5.update_layout(
        #hovermode='x',
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # fig1.update_traces(hovertemplate=None)
    # fig1.update_layout(margin=dict(l=5, r=10, t=25, b=20)) <extra></extra>"
    return fig5


# Int Fig6: TSA seasonal yearline country
@app.callback(
    [
        Output('int-tsactr', 'options'),
        Output('int-tsactr', 'value'),
    ],
    [Input('menu-slidery', 'value')]
)
def selection_int_tsactr(slidery):
    secctrf6 = sankeyall[sankeyall.country_route != 'Vietnam']
    fig6ctropts = [{'label': ctr, 'value': ctr} for ctr in
                   list(secctrf6[secctrf6.flty == slidery]['country_route'].unique())]
    return fig6ctropts, list(secctrf6[secctrf6.flty == slidery]['country_route'].unique())[8]


@app.callback(
    [Output('intfig6-tsa', 'figure'),
     Output('highestm-ctr', 'children'),
     Output('shighestm-ctr', 'children'),
     Output('lowestm-ctr', 'children')],
    [
        Input('extend-ind', 'value'),
        Input('menu-slidery', 'value'),
        Input('int-tsactr', 'value'),
    ]
)
def int_yearline_fig6(indfig6, slidery, ctrfig6="Japan", ):
    dfig6 = ctrym_allind.loc[ctrym_allind.country_route == ctrfig6, :]
    dfig6.flt_ym = dfig6.flt_ym.map(lambda x: dt.datetime.strptime(x, '%Y-%m'))
    dfig6['flty'] = dfig6.flt_ym.dt.year
    dfig6['fltm'] = dfig6['flt_ym'].dt.strftime('%b')
    avgmindlist = dfig6[dfig6.flty != 2020][['fltm', indfig6]].groupby('fltm').agg(
        avg=(indfig6, 'mean')).sort_values(by='avg', ascending=False).reset_index()


    Highestm= f'The highest month of {inddict[indfig6]} of {ctrfig6} route is {avgmindlist.fltm[0]} '
    Shighestm= f'The second highest month of {inddict[indfig6]} of {ctrfig6} route is {avgmindlist.fltm[1]}'
    Lowestm= f'The lowest month {inddict[indfig6]} of {ctrfig6} route is {avgmindlist.fltm[11]}'

    fig6 = go.Figure()

    for i, y in enumerate(dfig6.flty.unique()):
        fig6.add_traces(go.Scatter(name=str(y),
                                    x=dfig6[dfig6.flty == y]['fltm'],
                                    y=dfig6[dfig6.flty == y][indfig6],
                                    mode='lines+markers',
                                    marker=dict(color=px.colors.qualitative.Bold[i]),
                                    opacity=1))

    fig6.update_xaxes(  # rangeslider_visible=True,
        dtick="M1",
        # tickformat="%b\n", #ticklabelmode='period'
        # tickfont=dict(size=10)
    )
    fig6.update_traces(
        hovertemplate="<b>%{x}</b><br>" + "%s: " % (inddict[indfig6]) + "%{y:.3s}<br>",
        marker_symbol='circle'

    )
    # fig6.update_layout(legend_title_font_size=14)
    fig6.update_layout(
        title='{} Seasonal analysis of {} country route\
                     <br>in Jan2015 - Dec2019</b>'.format(inddict[indfig6], ctrfig6),
        #hovermode='x',
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    return fig6, Highestm, Shighestm, Lowestm


### DOMESTIC ROUTE: (fig8-10-7-9-11)

# Dom Fig8+10: Barchart top dom route + top departure airport (share input)
@app.callback(
    [Output('domfig8-barroute', 'figure'),
     Output('domfig10-bara', 'figure')],
    [Input('menu-slidery', 'value'),
     Input('menu-keyind', 'value')]
)
def dom_bartoproute_fig8(yearfig810, indfig810):
    dfig8 = domrouteyear_paxrevflt.loc[
        domrouteyear_paxrevflt.flty == yearfig810, ['city_roundroute', indfig810]].sort_values(by=indfig810,
                                                                                               ascending=False)
    dfig8 = dfig8.iloc[:30, :]
    fig8 = go.Figure(
        data=[go.Bar(
            name='sticoute',
            x=dfig8.city_roundroute,
            y=dfig8[indfig810],
            marker_color="#AE8F6F",
            opacity=0.8)])
    fig8.update_traces(
        hovertemplate="<b>%{x}</b><br>" + "%s in %s: " % (inddict[indfig810], str(yearfig810)) + "%{y:.3s}<br>",
    )
    fig8.update_layout(
        title="Top 30 routes by %s in %s" % (inddict[indfig810], str(yearfig810)),
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    fig8.update_traces(textangle=-60)

    dfig10 = oriayear_paxrevflt.loc[oriayear_paxrevflt.flty == yearfig810, ['ORI', indfig810]].sort_values(by=indfig810,
                                                                                                           ascending=False)
    dfig10 = dfig10.iloc[:15, :]
    fig10 = go.Figure(
        data=[go.Bar(
            name='Departure Airport',
            x=dfig10.ORI,
            y=dfig10[indfig810],
            marker_color="#004687",
            opacity=0.8)])
    fig10.update_traces(
        hovertemplate="<b>Depart from %{x}</b><br>" + "%s in %s: " % (
            inddict[indfig810], str(yearfig810)) + "%{y:.3s}<br><extra></extra>",
    )
    fig10.update_layout(
        title="Top 15 departure airports by %s in %s" % (inddict[indfig810], str(yearfig810)),
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    fig10.update_traces(textangle=-60)
    return fig8, fig10


# Dom Fig7: gantt chart route operation embedded in layouts (from staticFig)

# Dom Fig9: Timeline round routes comparison
@app.callback(
    [
        Output('dom-timelinedomr', 'options'),
        Output('dom-timelinedomr', 'value'),
    ],
    [Input('menu-slidery', 'value')]
)
def selection_dom_timelinedomr(slidery):
    fig9ctropts = [{'label': domr, 'value': domr} for domr in
                   list(domrouteyear_paxrevflt[domrouteyear_paxrevflt.flty == slidery]['city_roundroute'].unique())]
    return fig9ctropts, list(
        domrouteyear_paxrevflt[domrouteyear_paxrevflt.flty == slidery]['city_roundroute'].unique())[21:23]


@app.callback(
    Output('domfig9-timeline', 'figure'),
    [Input('dom-timelinedomr', 'value'),
     Input('extend-ind', 'value')]
)
def dom_monthline_fig9(domrlistfig9, indfig9):
    dfig9 = domrouteym_allind[domrouteym_allind.city_roundroute.isin(domrlistfig9)]
    # labely_fig5= inddict[indfig5]

    fig9 = px.line(dfig9, x='flt_ym', y=indfig9,
                   color='city_roundroute',
                   labels={indfig9: inddict[indfig9], 'city_roundroute': "<b>Route</b>",
                           'flt_ym': 'Monthly Timeline'},
                   color_discrete_map={k: domrcolors[k] for k in domrlistfig9},
                   title='{} by {} \
                  <br>in Jan2015 - Dec2019</b>'.format(", ".join(domrlistfig9), inddict[indfig9]))

    fig9.update_xaxes(rangeslider_visible=True,
                      dtick="M1",
                      tickformat="%b\n%Y",  # tickfont=dict(size=10)
                      )
    fig9.update_traces(hovertemplate="<b>%{x}</b><br>" + "%s: " % (inddict[indfig9]) + "%{y:.3s}<br>")
    # fig5.update_layout(legend_title_font_size=14)
    fig9.update_layout(
        #hovermode='x',
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # fig1.update_traces(hovertemplate=None)
    # fig1.update_layout(margin=dict(l=5, r=10, t=25, b=20)) <extra></extra>"
    return fig9

@app.callback(
    [
        Output('dom-tsadomr', 'options'),
        Output('dom-tsadomr', 'value'),
    ],
    [Input('menu-slidery', 'value')]
)
# Dom Fig11: TSA seasonal yearline round route
def selection_dom_tsadomr(slidery):
    fig11ctropts = [{'label': domr, 'value': domr} for domr in
                    list(domrouteyear_paxrevflt[domrouteyear_paxrevflt.flty == slidery]['city_roundroute'].unique())]
    return fig11ctropts, list(domrouteyear_paxrevflt[domrouteyear_paxrevflt.flty == slidery]['city_roundroute'].unique())[19]


@app.callback(
    [Output('domfig11-tsa', 'figure'),
     Output('highestm-domr', 'children'),
     Output('shighestm-domr', 'children'),
     Output('lowestm-domr', 'children')],
    [
     Input('extend-ind', 'value'),
     Input('menu-slidery', 'value'),
     Input('dom-tsadomr', 'value'),]
)
def int_yeardomrline_fig11statement(indfig11, slidery, domrfig11):
    dfig11 = domrouteym_allind.loc[domrouteym_allind.city_roundroute==domrfig11, :]
    dfig11.flt_ym = dfig11.flt_ym.map(lambda x: dt.datetime.strptime(x, '%Y-%m'))
    dfig11['flty'] = dfig11.flt_ym.dt.year
    dfig11['fltm'] = dfig11['flt_ym'].dt.strftime('%b')
    avgmindlist = dfig11[dfig11.flty != 2020][['fltm', indfig11]].groupby('fltm').agg(
        avg=(indfig11, 'mean')).sort_values(by='avg', ascending=False).reset_index()
    orderm= list(avgmindlist.fltm)


    Highestm= f'The highest month of {inddict[indfig11]} of route {domrfig11} is {orderm[0]}'
    Shighestm= f'The second highest month of {inddict[indfig11]} of route {domrfig11} is {orderm[1]}'
    Lowestm= f'The lowest month of {inddict[indfig11]} of route {domrfig11} is {orderm[-1]}'

    fig11 = go.Figure()

    for i, y in enumerate(dfig11.flty.unique()):
        fig11.add_traces(go.Scatter(name=str(y),
                                    x=dfig11[dfig11.flty == y]['fltm'],
                                    y=dfig11[dfig11.flty == y][indfig11],
                                    mode='lines+markers',
                                    marker=dict(color=px.colors.qualitative.Bold[i]),
                                    opacity=1))

    fig11.update_xaxes(  # rangeslider_visible=True,
        dtick="M1",
        # tickformat="%b\n", #ticklabelmode='period'
        # tickfont=dict(size=10)
    )
    fig11.update_traces(
        hovertemplate="<b>%{x}</b><br>" + "%s: " % (inddict[indfig11]) + "%{y:.3s}<br>",
        marker_symbol='circle'

    )
    # fig6.update_layout(legend_title_font_size=14)
    fig11.update_layout(
        title='{} Seasonal analysis of {} round route\
                  <br>in Jan2015 - Dec2019</b>'.format(inddict[indfig11], domrfig11),
        #hovermode='x',
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
    # fig1.update_traces(hovertemplate=None)
    # fig1.update_layout(margin=dict(l=5, r=10, t=25, b=20)) <extra></extra>"
    return fig11, Highestm, Shighestm, Lowestm

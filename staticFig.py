import plotly.figure_factory as ff
from data import activedom

fig7 = ff.create_gantt(
    activedom.rename(columns={'domroute': 'Task', 'first_flt': 'Start', 'last_flt': 'Finish'}),
    # width= 900,
    colors= "#AE8F6F",
    height=900
)
fig7.update_xaxes(rangeslider_visible=True)
fig7.update_layout(
    title='Domestic route timeline operation from Jan 2015 to Dec 2019',
    font={"color": "darkslategray"},
    paper_bgcolor="white",
    plot_bgcolor="#f8f5f0",
    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))

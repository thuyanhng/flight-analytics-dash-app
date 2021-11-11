import pandas as pd

import plotly.express as px

# Data preparation:
inddict = {'flt_count': 'Flights', 'prev_total': 'Revenue', 'prev_yq_total': 'YQ revenue',
           'exbag_rev_total': 'Exbag revenue', 'cargow_total': 'Cargo Weight',
           'cargo_rev_total': 'Cargo revenue', 'mail_rev_total': 'Mail revenue', 'pax_total': 'Passengers',
           'avg_loadrate': 'Average load rate', 'avgPaxRev': 'Average revenue per Pax per one-way flight'}
indicator3 = ['pax_total', 'prev_total', 'flt_count']
indicator9 = ['pax_total', 'prev_total', 'flt_count', 'avgPaxRev',
              'avg_loadrate', 'cargo_rev_total', 'mail_rev_total', 'cargow_total', 'exbag_rev_total']


# For OVV:
nwyear_paxrevflt= pd.read_csv('Data/nwyear_paxrevflt.csv')

# country-year-pax-rev-flt

ctryear_paxrevflt= pd.read_csv('Data/ctryear_paxrevflt.csv')

regyear_paxrevflt= pd.read_csv('Data/regyear_paxrevflt.csv')

sankeyall= pd.read_csv('Data/sankeyall.csv')

# For INT:
intranktab= pd.read_csv('Data/intRankingtable.csv')

ctrym_allind= pd.read_csv('Data/ctrym_allind.csv')


intoriayear_paxrevflt= pd.read_csv('Data/intoriayear_paxrevflt.csv')

# For DOM:
sortedpaxroute= pd.read_csv('Data/sortedpaxroute.csv')

domrouteyear_paxrevflt= pd.read_csv('Data/domrouteyear_paxrevflt.csv')

domrouteym_allind= pd.read_csv('Data/domrouteym_allind.csv')

oriayear_paxrevflt= pd.read_csv('Data/oriayear_paxrevflt.csv')

activedom=pd.read_csv('Data/activedom.csv')

# For ACT:


# Make color:
colorseq= px.colors.qualitative.Antique+px.colors.qualitative.Vivid+px.colors.qualitative.Safe+px.colors.qualitative.Bold+px.colors.qualitative.Pastel+px.colors.qualitative.Prism+px.colors.qualitative.Set3
regioncolors= dict(zip(ctryear_paxrevflt.Region.unique(),px.colors.qualitative.Antique[0:4]))
ctrcolors= dict(zip(ctryear_paxrevflt.country_route.unique(), colorseq[0:14]))
domrcolors= dict(zip(sortedpaxroute['city_roundroute'], colorseq[0:43]))



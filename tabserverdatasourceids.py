from ayx import Alteryx
import pandas as pd
import numpy as np
import tableauserverclient as TSC

tableau_auth = TSC.TableauAuth('USERNAME', 'PASSWORD', site='SITE')
server = TSC.Server('https://SERVER-URL')

server.auth.sign_in(tableau_auth)

with server.auth.sign_in(tableau_auth):
    request_options = TSC.RequestOptions(pagesize=1000)
    all_datasources = list(TSC.Pager(server.datasources))
    index = 0
    datasources = {}
    for ds in all_datasources:
        datasources[index] = [ds.name, ds.id]
        index +=1
        print(datasources)
       
df = pd.DataFrame.from_dict(datasources, orient='index')

df.rename({0:'Datasource_Name', 1:'Datasource_ID'}, axis='columns', inplace=True)

Alteryx.write(df, 1)
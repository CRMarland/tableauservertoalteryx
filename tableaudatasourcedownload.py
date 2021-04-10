#Import packages

from ayx import Package
from ayx import Alteryx
import tableauhyperapi as THA
import tableauserverclient as TSC
import pandas as pd
import numpy as np
import zipfile
import re
from os import listdir
from os.path import isfile, join

# Authenticate with your Tableau Server

tableau_auth = TSC.TableauAuth('USERNAME', 'PASSWORD', site='SITE')
server = TSC.Server('https://SERVER-URL')

# Download datasource and save the filepath in data_loc variable

with server.auth.sign_in(tableau_auth):
    data_loc = server.datasources.download('DATASOURCE-ID')

# Use RegEx to extract the filepath minus the filename from the data_loc variable

m = re.match('(.*)\\\\.*$', data_loc)
filepath = m.group(1)

# Unzip the tdsx file (using the data_loc variable) and extract it to the folder
# (using the filepath variable)

with zipfile.ZipFile(data_loc, 'r') as zip_ref:
    zip_ref.extractall(filepath)

# Create a data_path variable that points to the location of the extracted hyper file
# created by the previous step.
# Get the name of the original download and compare that to the files in the 
# unzipped folder - it may have a suffix. 

hyper_location = filepath + '\Data\Extracts'

tdsx_name = re.match(r'.*\\(.*)\.tdsx', data_loc)[1]

hypers_list = os.listdir(hyper_location)

for item in hypers_list:
    tdsx_name_len = len(tdsx_name)
    match_item = item[0:tdsx_name_len]
    if match_item == tdsx_name:
        hyper = item

# Combine the hyper location with the name of the hyper file to create the full path to
# use in an input data tool

final_filepath = hyper_location + '\\' + hyper

# Put the final_filepath variable into a dict so it can be turned into a df and exported
# to Alteryx canvas

dict_to_df = {'data_location': [final_filepath]}

output = pd.DataFrame(data=dict_to_df)

Alteryx.write(output,1)
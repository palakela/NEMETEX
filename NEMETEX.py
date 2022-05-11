#!/usr/bin/env python
# coding: utf-8

# import useful packages
import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description="NEMETEX v.1.0 setting parameters",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m", "--model", type=str, default="CarveMe", help="model used to generate input files. Either CarveMe or gapseq are accepted")
parser.add_argument("-s", "--smetana", type=str, required=True, help="file path for smetana output file")
parser.add_argument("-a", "--coverage", type=str, help="file path for MAGs abundances")
parser.add_argument("-t", "--taxonomy", type=str, help="file path for MAGs taxonomy")
parser.add_argument("-C", "--compound", required=True, type=str, help="compound name OR file path for a list of several compound names")
parser.add_argument("-p", "--prefix", type=str, default="", help="prefix for output folder")

args = vars(parser.parse_args())

# Set up parameters
model = args["model"]
path1 = args["smetana"]
path2 = args["coverage"]
path4 = args["taxonomy"]
compound = args["compound"]
prefix = args["prefix"]


# detect the current working directory and create the output folder
if prefix == "":
    sep = '/'
else:
    sep = '/'+prefix+'_'
    
path = os.getcwd()+sep+'outputs'
    
try:
    os.mkdir(path)
except OSError:
    print("\n<WARNING>: Creation of the directory %s failed. \nMaybe it alredy exists, the files inside will be overwrited." % path)
    
# create error classes to check input files errors
class DuplicatedValues(Exception):
    pass
class NaNValues(Exception):
    pass

# allow to choose between bigg_compounds_conversion_table_CORRECT.txt (for CarveMe models) 
# or gapseq_compounds_conversion_table.txt (for gapseq models)
try:
    if model == 'CarveMe':
        path3 = "bigg_compounds_conversion_table_CORRECT.txt" # already provided with the script
        link3 = "http://bigg.ucsd.edu/universal/metabolites"
    elif model == 'gapseq':
        path3 = "gapseq_compounds_conversion_table.txt" # already provided with the script
        link3 = "https://modelseed.org/biochem/compounds"
except OptionError:
    print("\n<ERROR>Input model not valid, please insert either CarveMe or gapseq.\n")

# import bigg compounds conversion file as Pandas DataFrame (already checked for NA and duplicates)
id_conversion_table = pd.read_csv(path3, delimiter = "\t", index_col='extended name')

# import smetana output as Pandas DataFrame
smetana = pd.read_csv(path1, delimiter = "\t")

# check for NA: if YES raise an error
na_values = smetana.isnull().sum().sum()
if na_values != 0:
    raise NaNvalues("\nThe smetana file has {} missing values. CORRECT IT !!".format(na_values))

# check for duplicates: if YES raise an error
duplicated = smetana.duplicated().sum()
if duplicated != 0:
    raise DuplicatedValues("\nThe smetana file has {} duplicated rows. CORRECT IT !!".format(duplicated))

# remove eventually additional info in compound column
smetana['compound'] = smetana['compound'].agg(lambda x: x.rsplit('_e')[0]+'_e')

# find which compounds are exchanged in the community and how many times
exchanged_compounds = pd.DataFrame(smetana['compound'].value_counts())
exchanged_compounds.columns = ['number of exchanges']

# find the average exchange rate for each compound
exchanged_compounds['smetana_avg'] = smetana.groupby(['compound'])['smetana'].mean()
exchanged_compounds.index.name = 'compound'

exchanged_compounds.sort_index(inplace=True)  #output file sorted in alphabetical order

# create an output file with all retrived information
try:
    exchanged_compounds.to_csv(path+sep+'compounds_exchanged.tsv', sep = '\t')
    print("\n...In the community there are {} exchanges of {} different compounds.\n\nThe file with the list of all compounds exchanged in the community has been generated...".format(smetana.shape[0], exchanged_compounds.shape[0]))
except OSError:
    print("\n<ERROR>: Creation of the compounds_exchanged file failed.")

# create an output file with the number of exchanges for each donor species of each compound
donors_for_compound = pd.DataFrame(smetana.groupby(['compound', 'donor'])[['receiver', 'smetana']].agg({'receiver':'count', 'smetana':'mean'}))
donors_for_compound.rename(columns={'receiver':'gives to','smetana':'average probability of donation'}, inplace=True)

try:
    donors_for_compound.to_csv(path+sep+'donors_for_compound.tsv', sep = '\t')
    print("The file with the list of all donors for each compound has been generated...")
except OSError:
    print("\n<ERROR>: Creation of the donors_for_compound file failed.")

# create an output file with the number of exchanges for each receiver species of each compound
receivers_for_compound = pd.DataFrame(smetana.groupby(['compound', 'receiver'])[['donor', 'smetana']].agg({'donor':'count', 'smetana':'mean'}))
receivers_for_compound.rename(columns={'donor':'receives from','smetana':'average probability to receive'}, inplace=True)

try:
    receivers_for_compound.to_csv(path+sep+'receivers_for_compound.tsv', sep = '\t')
    print("The file with the list of all receivers for each compound has been generated...\n\nSee inside %s folder.\n" % path)
except OSError:
    print("\n<ERROR>: Creation of the receivers_for_compound file failed.")

try:
    # import MAG abundances as Pandas DataFrame
    MAGs_coverage = pd.read_csv(path2, delimiter = "\t", index_col="Bin Id")

    # check for NA
    na_values = MAGs_coverage.isnull().sum().sum()
    if na_values != 0:
        raise NaNvalues("\nThe MAGs coverage file has {} missing values. CORRECT IT !!".format(na_values))

    # check for duplicates
    duplicated = MAGs_coverage.duplicated().sum()
    if duplicated != 0:
        raise DuplicatedValues("\nThe MAGs coverage file has {} duplicated rows. CORRECT IT !!".format(duplicated))

    # remove extension if present
    if '.' in str(MAGs_coverage.index[0]):
        MAGs_coverage.index = MAGs_coverage.index.str.rsplit('.', expand=True).droplevel(1)  

    # select all df rows, but only columns ending with ".sorted: % binned populations"
    node_diameters = pd.DataFrame(MAGs_coverage.loc[:, MAGs_coverage.columns.str.endswith(".sorted: % binned populations")]*100)

except:
    print("\nATTENTION: The MAGs coverage file has not been selected. No abundances info will be add to the graph.")

try:
    # import taxonomy file as Pandas DataFrame
    taxonomy = pd.read_csv(path4, delimiter = "\t", index_col='user_genome')

    # check for NA
    na_values = taxonomy.isnull().sum().sum()
    if na_values != 0:
        raise NaNvalues("\nThe taxonomy file has {} missing values. CORRECT IT !!".format(na_values))

    # check for duplicates (only at index level)
    duplicated = taxonomy.index.duplicated().sum()
    if duplicated != 0:
        raise DuplicatedValues("\nThe taxonomy file has {} duplicated rows. CORRECT IT !!".format(duplicated))

    # remove extension if present
    if '.' in str(taxonomy.index[0]):
        taxonomy.index = taxonomy.index.str.rsplit('.', expand=True).droplevel(1)
        
except:
    print("\nATTENTION: The MAGs taxonomy file has not been selected. No taxonomy info will be add to the graph.")

##########################################################################################    

def compare(x):
    if x['average probability of donation'] > x['average probability to receive']:
        return 'mainly donor'

    elif x['average probability of donation'] < x['average probability to receive']:
        return 'mainly receiver'

    elif x['average probability of donation'] == x['average probability to receive']:
        return 'commensalistic'
    
def network(compound):

    to_replace = {":":"-", "*":"", "?":"", "<":"", ">":"", "|":"", "/":"", "\\":""}

    # if the compound name is provided as extended name, convert it into biggID
    # LINE REMOVED becouse doesn't work: new_compound = "%s%s" % (compound[0].upper(), compound[1:].lower())
    if compound in id_conversion_table.index:
        compound_extended = compound
        compound = id_conversion_table.loc[compound]['biggID']

    # add prefix and suffix to compound name to search for it in smetana output table
    compound_ID = 'M_'+compound+'_e'

    # if the compound is present inside smetana output, create a table with all its exchanges
    if compound_ID in exchanged_compounds.index:
        compound_extended = id_conversion_table.loc[id_conversion_table['biggID'] == compound].index.item()
        for key in to_replace:
            compound_extended = compound_extended.replace(key, to_replace[key])
            
        print(f'\n\nYou are searching for all {compound_extended.upper()} exchanges in the community...')

        subset = smetana[smetana["compound"] == compound_ID]
        print(f'\n...There are {subset.shape[0]} exchange(s) of {compound_extended.upper()} in the community.')

        # create a directory where to store compound outputs
        path = os.getcwd()+sep+'outputs/'+str(compound)
        try:
            os.mkdir(path)
        except OSError:
            print(f"\n<WARNING>: Creation of the directory {path} failed.\nMaybe it already exists, the files inside will be overwrited.")

        # create an output file with all retrived information and exit from the while loop
        try:
            subset.to_csv(path+'/'+str(compound_extended)+'_exchanges.tsv', sep = '\t')
            print(f'\nThe file with all {compound_extended} exchanges in the community has been generated...')
        except OSError:
            print("\n<ERROR>: Creation of the compound file failed")

    # if the compound is not exchanged, print it and ask for a new compound (start another loop)
    else:
        print(f'\nATTENTION: There are not {compound} exchanges in the community, check the name inside the database ('+link3+') or try another compound. Remember, compound names are Case Sensitive.\n')
        return

    # create a list of all species involved in the exchange (set is a datastructure which keeps only one occurrency for each duplicate)
    species = set(pd.concat([subset['receiver'], subset['donor']], axis=0, join='outer'))

    # create a dictionary where key is the species IDs and value is a dictionary containing average abundance and phylum
    species_attributes = {}
    for s in species:
        try:
            diam = node_diameters.loc[s].mean()
        except:
            diam = 0
        try:
            tax = taxonomy.loc[s]['NCBI classification'].split(';')[1].lstrip('p__')
        except:
            tax = 'Unknown'
        species_attributes[s] = {'abundance':diam, 'taxonomy':tax}

    # convert the dictionary in a dataframe and save it in a tsv file
    species_attributes = pd.DataFrame(species_attributes).T  # T method allow us to switch rows and columns (transpose)

    # select only usefull columns and change smetana column name to 'value', to allow recognition as witdth measure by pyvis
    subset2 = subset[['receiver', 'donor', 'smetana']].rename(columns={'smetana':'value'})

    # Creation of a directed graph G with all our exchanges
    G = nx.from_pandas_edgelist(subset2, source='donor', target='receiver', edge_attr='value', create_using=nx.DiGraph())

    # needed to uniform indeces to the graph
    species_attributes = species_attributes.reindex(G.nodes())

    # convert taxonomy values to categorical type (important to allow graph's data management)
    species_attributes['taxonomy'] = pd.Categorical(species_attributes['taxonomy'])
    species_attributes['taxonomy'].cat.codes

    # convert diameter values to numeric type
    species_attributes['abundance'] = pd.to_numeric(species_attributes['abundance'])

    # add features to the nodes
    nx.set_node_attributes(G, species_attributes['abundance'], name='size')
    nx.set_node_attributes(G, species_attributes['taxonomy'], name='group')

    # create graph's visualization
    net = Network('100%', '100%', directed = True, layout = True, heading='Exchanges of '+str(compound_extended))
    net.from_nx(G)

    # add some data to the nodes
    neighbor_map = net.get_adj_list()

    for node in net.nodes:
        node["title"] = "Gives to:<br>" + "<br>".join(neighbor_map[node["id"]]) + '<br><br>Abundance: '+str(node['size']/100)+'%<br><br>Phylum: '+str(node['group'])

    # add exchange rate data to the edges
    for edge in net.edges:
        edge['title'] = 'exchange probability (smetana value): '+str(edge['value'])

    # manage interactive visualization
    net.set_options(""" var options = {
     "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 5
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "dashes": true,
        "smooth": true
      },
      "interaction": {
        "multiselect": true,
        "navigationButtons": true
      },
      "physics": {
        "minVelocity": 0,
        "maxVelocity": 0.5,
        "barnesHut": {
          "gravitationalConstant": -85000,
          "centralGravity": 10,
          "springLength": 250,
          "springConstant": 0,
          "damping": 0,
          "avoidOverlap": 1
        }
      }
    }""")

    try:
        net.show(path+'/'+str(compound_extended)+'_exchanges.html')
        print(f'The HTML file with the network of all {compound_extended} exchanges in the community has been generated...')
    except OSError:
        print("<ERROR>: Creation of the network's HTML file failed")

    # create a final file with all exchanges informations
    result = pd.concat([species_attributes, donors_for_compound.loc[compound_ID], receivers_for_compound.loc[compound_ID]], axis=1, join="outer", sort = False)
    result.sort_values(by=['abundance'], ascending=False, inplace=True)
    result.replace(np.nan,0, inplace=True)
    result['abundance'] = result['abundance']/100
    result['behaviour'] =  result.apply(compare, axis=1)
    result.index.name = 'Species'

    try:
        result.to_csv(path+'/'+str(compound_extended)+'_species_behaviour.tsv', sep = '\t')
        print(f'The file with characteristics of all species involved in {compound_extended} exchanges has been generated.\n\nSee inside {path} folder.\n')
    except OSError:
        print("\n<ERROR>: Creation of the species behaviours file failed")

        
        
try:
    with open(compound) as file:
        compounds = file.readlines()
        compounds = [line.rstrip() for line in compounds]         
    for c in compounds:
        network(c)
            
except:
    network(compound)

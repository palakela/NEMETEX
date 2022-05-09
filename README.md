<p align="center">
  <img src="Logo.png" width="40%">
</p>

<p align='center'>
  Michela Palamin, Elisabetta Offer, and Alice Frisinghelli
</p>  
<p align='center'> 
  Master's Degree in Molecular Biology
</p>
<p align='center'>
  University of Padua
</p>

<p align='center'>
  <i>This code was developed as part of a project carried out during the course of Microbial Metagenomics (Molecular Biology master degree) at the University of Padova. The project was supervised by Prof. Stefano Campanaro and Dr. Arianna Basile.</i>
</p>



Table of contents: 
1) INTRODUCTION
2) REQUIREMENTS
3) INPUT FILES
4) OUTPUT FILES
5) TIPS

______________________________________________________________________________________
## 1) INTRODUCTION

NEMETEX (NEtwork for METabolic EXchanges) is designed for giving graphical visualizations of metabolite exchanges within complex communities. Flux Balance Analysis (FBA) results are not easy to interpret, and certainly not intuitive. NEMETEX aims to provide a simple and useful visualization for managing high-throughput data from metagenomic and FBA analyses.
NEMETEX directly work on SMETANA output files.

______________________________________________________________________________________
## 2) REQUIREMENTS

To run the script it is necessary to have `Python v3.x` installed on your laptop and the following libraries (see also [requirement file](requirements.txt)):

-  `Numpy v1.15.1`
-  `Pandas v0.23.4`
-  `NetworkX v2.1`
-  `PyVis v0.1.9`
-  `os` (part of the Standard Library of `Python 3`)
-  `argparse v2.0.1`

You can install all these dependences from the command line with the following command:

```python
pip3 install numpy pandas networkx pyvis.network os argparse 
```
_______________________________________________________________________________________
## 3) INPUT FILES

NEMETEX needs four different input files to work.

A tabular file necessary to convert compound names, which can either be one of the two already provided with the script or one of your own in the same format as provided ones:

- **[bigg_compounds_conversion_table_CORRECT.txt](bigg_compounds_conversion_table_CORRECT.txt)**: a tabular file allowing the conversion from the CarveMe ID to the extended name of a compound. This file is provided and can be found within the downloaded folder. 
- **[gapseq_compounds_conversion_table.txt](gapseq_compounds_conversion_table.txt)**: tabular file allowing the conversion from the gapseq ID to the extended name of a compound. This file is also provided and can be found within the downloaded folder. 

The remaining three files instead, must be provided by the user. Notice that in [this folder](ToyData) you can find examples of how data in these files must be organised:

- the [output file (tsv format)](ToyData/smetana_output.tsv) generated by `SMETANA v1.0.0`.
- a [tabular file (txt format)](ToyData/MAGs_coverage.txt) which comprises the species (MAGs) abundances of the focus community generated using `checkM v1.0.12`. 
- a [tabular file (txt format)](ToyData/gtdb_ncbi_taxonomy.txt) reporting the MAGs taxonomy generated using `GTDB-Tk v1.3.0` and then converted to the NCBI taxonomy using `gtdb_to_ncbi_majority_vote.py` script (you can find it at this [link](https://github.com/Ecogenomics/GTDBTk/blob/master/scripts/gtdb_to_ncbi_majority_vote.py)).

________________________________________________________________________________________
## 4) OUTPUT FILES

For the entire community NEMETEX generates 3 output files:

-  **[compounds_exchanged.tsv](example_outputs/compounds_exchanged.tsv)**: a file reporting all the compounds exchanged within the community, each reported with the relative number of exchanges and the average probability of exchange (smetana_avg). Notice that this file is sorted out in a descending order according to the number of exchanges.
-  **[donors_for_compound.tsv](example_outputs/donors_for_compound.tsv)**: a file reporting all the donor species for each compound, each reported with the number of receivers and the average probability of donation.
-  **[receivers_for_compound.tsv](example_outputs/receivers_for_compound.tsv)**: a file reporting all receivers for each compound, each reported with the number of donors and the average probability of receiving it.

In [this folder](example_outputs) you can find examples of how data in these output files are organised.

After that, for each compound selected by the user, the script creates a new folder named according to the CarveMe or gapseq ID of the compound. Each folder includes the following files:

-  **compoundName_exchanges.tsv**: a file reporting a subset of the smetana output only relative to that compound.
-  **compoundName_species_behaviour.tsv**: a file reporting the characteristics of all species involved (relative abundance in %, taxonomy, number of receivers with the relative average probability, number of donors with the relative average probability) and the behaviour of the same depending on donor/receiver probability ratio. Notice that the file is sorted out by relative abundances in descenting order.
-  **compoundName_exchanges.html**: a file with the interactive network relative to all exchanges of that compound in the community. Notice that for each node the colour depends on the taxonomy, and the size is proportional to MAGs abundances. Moreover, the thickness of each edge is proportional to its smetana value.

[Here](example_outputs/ac) you can find examples of output files for the Acetate exchanges in a random community.

_________________________________________________________________________________________
## 5) TIPS

### a. Sort output files by taxonomy to refine your analysis

In order to explore completely the community, we suggest the user to group the species present in the supplementary output file by their taxonomy. Indeed, this could provide a more general overview of the community. To do so, you can run the following code inside `NEMETEX` folder where `biggID` and `compoundName` are general references and must be substituted depending on the specific case under analysis. Notice that also `output` folder name must be changed if a prefix has been indicated.

```python
import numpy as np
import pandas as pd

result = pd.read_csv('./outputs/biggID/compoundName_species_behaviour.tsv', delimiter = "\t", index_col='Species')
result.groupby(['taxonomy', 'behaviour']).mean()
```
### b. Update ID/extended_name conversion files

Since the compound names in the smetana output are reported as “bigg_IDs” (or gapseq IDs)and not as extended names, we provide two conversion files created by downloading the conversion file from either [bigg site](http://bigg.ucsd.edu/universal/metabolites) or [gapseq site](https://modelseed.org/biochem/compounds) and cleaning it for both NaN values and duplicates.

In case you would like to update **[bigg_compounds_conversion_table_CORRECT](bigg_compounds_conversion_table_CORRECT.txt)** file, here we report the code which can be used to create this kind of file (notice that internet connection is required):

```python
import requests
import json
import numpy as np
import pandas as pd
import os

# download of the bigg compounds conversion file from the web (Internet connection is required)
response = requests.get('http://bigg.ucsd.edu/api/v2/universal/metabolites')
data = response.text
res = json.loads(data)

# convert it to a Pandas DataFrame
df = pd.DataFrame.from_dict(res['results'])

# check for NA
df.dropna(inplace=True)
# check for duplicates (only at index level) and keep only the first occurency
df.drop_duplicates(inplace=True)

# rename columns to future managing 
df.rename(columns={'name':'extended name','bigg_id':'biggID'}, inplace=True)
id_conversion_table = df.set_index('extended name')

# save as id_conversion_table_CORRECT.txt file
path = os.getcwd()
id_conversion_table.to_csv(path+'/bigg_compounds_conversion_table_CORRECT.txt', sep = '\t')
```

A similar procedure can be followed to update the **[gapseq conversion table](gapseq_compounds_conversion_table.txt)** file, using this code:

```python
import requests
import json
import numpy as np
import pandas as pd
import os

# download of the bigg compounds conversion file from the web (Internet connection is required)
response = requests.get('https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/compounds.json')
data = response.text
res = json.loads(data)

# convert it to a Pandas DataFrame
import pandas as pd

df = pd.DataFrame.from_dict(res)
df = df[['name','id']]

# check for NA
df.dropna(inplace=True)
# check for duplicates (only at index level) and keep only the first occurency
df.drop_duplicates(inplace=True)

# rename columns to future managing 
df.rename(columns={'name':'extended name','id':'biggID'}, inplace=True)
id_conversion_table = df.set_index('extended name')

# save as id_conversion_table_CORRECT.txt file
path = os.getcwd()
id_conversion_table.to_csv(path+'/gapseq_compounds_conversion_table.txt', sep = '\t')
```

# 6) Toy Data usage

To get some hints on how NEMETEX works, we provided you with some *toy data* that you can use. You can find them inside [ToyData](ToyData) folder inside the downloaded directory.

As first try, you can launch the code below from the command line while you are inside the downloaded directory:

```python
python NEMETEX.py -s ToyData/smetana_output.tsv -a ToyData/MAGs_coverage.txt -t ToyData/gtdb_ncbi_taxonomy.txt -C ToyData/compounds.txt -p ToyData
```

You can find the folder containing all output data named as **ToyData_outputs**. Notice that you can also analyse different coumpounds which are exchanged within the example community by changing [compounds](ToyData/compounds.txt) file.

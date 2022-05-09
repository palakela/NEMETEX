# Usage

To launch NEMETEX: open a new terminal, move to the folder you have downloaded, and write the following command line:

```python
python NEMETEX.py [-h] [-m MODEL] -s SMETANA [-a COVERAGE] [-t TAXONOMY] -C COMPOUND [-p PREFIX]
```

## Main arguments

Argument                     | Explanation
:----------------------------| :--------------------------------
`-s/--smetana <smetana.tsv>` | File path for smetana output file
`-C/--compound <compound>`   | Compound name (extended name or ID), or file path for a text file containing a list of several compound names (one per line)

## Options

Argument                       | Explanation
:------------------------------| :--------------------------------
`-m/--model <model>`           | Select the model used to generate input files. `<model>` can either be `CarveMe` or `gapseq`. Default `CarveMe`. 
`-a/--coverage <coverage.txt>` | File path for MAGs abundances. If not provided, final output files will not have abundance information. No different node sizes in the final network will be displayed.
`-t/--taxonomy <coverage.txt>` | File path for MAGs taxonomy. If not provided, final output files will not have taxonomy information. No different colors in the final network will be displayed.
`-p/--prefix <prefix>`         | Prefix for output folder name. Name format `prefix_outputs`. Default name `outputs`
`-h/--help`                    | Print usage information and quit

# Warnings

## a. Output folder creation

The script automatically creates the "output" folder inside the same directory you are working in. If it already exists, the script prints a WARNING statement but it continues to work. Below we report the error which will be shown at screen:

```
<WARNING>: Creation of the directory C:\Users\Michela\Desktop\NEMETEX/ToyData_outputs failed.
Maybe it alredy exists, the files inside will be overwrited.
```
Therefore, we may suggest to rename or remove previous files before continuing to avoid overwriting. Alternatively, you can run NEMETEX providing a different prefix for your output folder using `-p` argument.

## b. Model choice

As model argument, NEMETEX accepts only `CarveMe` or `gapseq`. If other names are provided, NEMETEX raises a NameError and quit. If no argument is provided, NEMETEX analyses you files with the defaul model (CarveMe).

## c. File names

When you provide file names, remember to provide also the extension of them (.txt or .tsv). In case these files are not in the working directory, you need to provide the entire file path name. 

## d. NaN and duplicated values in your files

Remember to check your files for NaN values or duplicates before to start, otherwise the program stops asking you to manually correct them (after the correction, you need to restart the script). 

# Expected output

If everything is correct, the code prints out the number of the total exchanges as follow, where `n` is the total number of exchanges within the community, and `m` is the number of different compounds which are exchanged: 

`...In the community there are n exchanges of m different compounds.`

Meanwhile, it creates three general files describing the entire community:

-  **compounds_exchanged.tsv**
-  **donors_for_compound.tsv**
-  **receivers_for_compound.tsv**

Printing at screen the following lines:

```
The file with the list of all compounds exchanged in the community has been generated...
The file with the list of all donors for each compound has been generated...
The file with the list of all receivers for each compound has been generated...

See inside C:\Users\Michela\Desktop\NEMETEX/ToyData_outputs folder.
```

At this point NEMETEX starts to analyse you files, searching for the compound(s) you have asked for. Notice that you can either use the extended name or the compound ID (see for reference: http://bigg.ucsd.edu/universal/metabolites and https://modelseed.org/biochem/compounds).

In case the compound is not found in the provided smetana file, the script warns you with the message below. If it is the case, we may suggest to check for spelling errors or the correct compound ID. If the error persists, the compound is probably not exchanged in the community. 

```
ATTENTION: There are not miao exchanges in the community, check the name inside the database (http://bigg.ucsd.edu/universal/metabolites) or try another compound. Remember, compound names are Case Sensitive.
```

Alternatively, if the compound is exchanged in the community, you see on screen the number of total exchanges of that compound in the community in the format shown in the example below, and a browser page opens showing the final exchange network.

```
You are searching for all ACETATE exchanges in the community...

...There are 57 exchange(s) of ACETATE in the community.

The file with all Acetate exchanges in the community has been generated...
The HTML file with the network of all Acetate exchanges in the community has been generated...
The file with characteristics of all species involved in Acetate exchanges has been generated.

See inside C:\Users\Michela\Desktop\NEMETEX/ToyData_outputs/ac folder.
```

The network is interactive, hence you can move all the present nodes as you like. Using `Ctrl` (or `Command`) key you can select more than one node and move them together. The color palette is indicative of the phylum level of each MAG, the diameter of each node is proportional to MAG abundance, and the thickness of each edge is proportional to the associated smetana value. Notice that a small info box appears as soon as you position your mouse either on a node, or on a edge.
 
You can also zoom in and zoom out the network. Notice that if the network is too zoomed out, species names are hidden by default. 

Finally, the script creates two compound-specific files: 

-  **compoundName_exchanges.tsv**
-  **compoundName_species_behavior.tsv**

The two files, as well as the network, can be found inside a specific directory named after the compound ID: `/NEMETEX/prefix_outputs/compoundID`

# Example of use

To get some hints on how NEMETEX works, we provided you with some toy data that you can use. You can find them inside [ToyData](ToyData) folder inside the downloaded directory.

As first try, you can run the code below from the command line while you are inside the downloaded directory:

```python
python NEMETEX.py -s ToyData/smetana_output.tsv -a ToyData/MAGs_coverage.txt -t ToyData/gtdb_ncbi_taxonomy.txt -C ToyData/compounds.txt -p ToyData
```

You can find the folder containing all output data generated from this commandline named as **ToyData_outputs**. Notice that you can also analyse different coumpounds which are exchanged within the example community by changing the [compounds](ToyData/compounds.txt) file.

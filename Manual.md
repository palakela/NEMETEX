# Manual

To launch the program, open the terminal, move to the folder you have downloaded, and write the following command line: `Phyton3 NEMETEX.py`.

The script automatically creates the "output" folder inside the same directory you are working in. If it already exists, the script raises an error but it continues to work. Therefore, we may suggest to rename or remove previous files before continuing. 

As first input, you are required to specify the name of the software used to create the model, choosing between **CarveMe** or **gapseq**.

At this point, you are required to give as input the names of the files (including the format) you would like to work on. In case they are not in the working folder, you need to provide the entire file path name. 

If you insert a wrong file name, the code will ask you to re-input the correct name.

Remember to check for NaN values or duplicates before to start, otherwise the program stops asking you to manually correct them (after the correction, you need to restart the script from the beginning). 

If everything is correct, the code prints out the number of the total exchanges as follow, where `n` is the total number of exchanges within the community, and `m` is the number of different compounds which are exchanged: 

`... In the community there are n exchanges of m different compounds`.

Meanwhile, it creates three general files describing the entire community:

-  **compounds_exchanged.tsv**

-  **donors_for_compound.tsv**

-  **receivers_for_compound.tsv**

Now you are required to give as input the name of the compound you want to study. You can either use the extended name or the compound ID (see for reference: http://bigg.ucsd.edu/universal/metabolites and https://modelseed.org/biochem/compounds). 

In case the compound is not found in the provided smetana file, the script warns you. We may suggest to check for spelling errors or the correct compound ID. If the error persists, the compound is probably not exchanged in the community. 

Alternatively, if the compound is exchanged in the community, you see on screen the number of total exchanges of that compound in the community, and a browser page opens showing the final exchange network.

The network is interactive, hence you can move all the present nodes as you like. Using `Ctrl` (or `Command`) key you can select more than one node. The color palette is indicative of the phylum level, the diameter of the node is proportional to MAG abundance, and the thickness of the edges is proportional to the associated smetana value. A small info box appears as soon as you position your mouse either on a node or on a edge.
 
You can also zoom in and zoom out. Notice that if the network is too zoomed out, species names are hidden by default. 

Finally, the script creates two compound-specific files: 

-  **compoundName_exchanges.tsv**

-  **compoundName_species_behavior.tsv**

The two files, as well as the network, can be found inside a specific directory named after the compound ID: `/CODENAME/outputs/compoundID`

As you finish reading all the files, you can either ask for another compound by typing "Y", or stop the program by typing "N".





EXAMPLE OF USE

python NEMETEX.py -s ToyData/smetana_output.tsv -a ToyData/MAGs_coverage.txt -t ToyData/gtdb_ncbi_taxonomy.txt -C ToyData/compounds.txt -p ToyData

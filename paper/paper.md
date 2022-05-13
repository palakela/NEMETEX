---
title: 'NEMETEX: a Python software for the visualisation of the network of metabolic exchanges'
tags:
  - Python
  - microbial interactions
  - flux balance analysis
  - metagenomics

authors:
  - name: Michela Palamin^[First author] 
    affiliation: 1
  - name: Alice Frisinghelli
    affiliation: 1
  - name: Elisabetta Offer
    affiliation: 1
  - name: Guido Zampieri
    orcid: 0000-0002-4518-5913
    affiliation: 1  
  - name: Arianna Basile^[Co-corresponding author]
    orcid: 0000-0003-2461-5221
    affiliation: 2
  - name: Stefano Campanaro^[Co-corresponding author]
    orcid: 0000-0002-9431-1648
    affiliation: 1,3
    
affiliations:
 - name: Department of Biology, University of Padova, Via Ugo Bassi 58/b 35131 Padova, Italy
   index: 1
 - name: The Medical Research Council Toxicology Unit, University of Cambridge, Cambridge, UK
   index: 2
 - name: CRIBI Biotechnology Center, University of Padova, 35131, Padua, Italy
   index: 3
date: 13 May 2022
bibliography: paper.bib


---

# Summary

Motivation: Microorganisms have a pivotal role in ecology and human health and form complex networks where different species can interact and exchange a range of different compounds. Flux balance analysis can offer an insight into the production and the absorption of these metabolic compounds, but frequently results are difficult to visualise and interpret. Additionally, a clear understanding of the roles of microbial species in the community requires thean integration of different information sources, including relative abundance, taxonomy and compounds exchange rate.
Results: To fill-in this gap the command-line tool NEMETEX (NEtwork for METabolic EXchanges) was developed to provide a graphical representation of the metabolites exchanged, joined with interactive visualisation of numerical data. This approach can undoubtedly represent an easy way to investigate high-throughput results obtained from metagenomics and flux balance analysis, providing a more direct interpretation of the data.
Availability and implementation: This program, accessory utilities, and their documentation are freely available at https://github.com/palakela/NEMETEX

\autoref{fig:logo}

# Introduction

Microbial communities are composed of groups of microorganisms sharing the same living space and interacting with each other. In microbiomes, different species can compete for resources and exchange metabolites, two processes representing the main drivers of microbial community assembly [@Ponomarova:2015]. The interplays between microorganisms are extremely variable and can range from competitive, to commensal and mutualistic interactions [@Basile:2020]. A complete understanding of these phenomena is limited by the difficulty in performing direct experimental measurement of carbon or nitrogen fluxes, however, the advancement of metagenomic techniques combined with metabolic Flux Balance Analysis (FBA) [@Orth:2010] allowed the investigation of metabolic fluxes within communities at an unprecedented level of resolution [@Machado:2021;@Diener:2020]. The recent improvement of methods focused on recovery of Metagenome-Assembled Genomes (MAGs) from shotgun sequencing determined a massive recovery of uncharacterized microbial species, most of them having a yet unclarified role [@Hugenholtz:2008;@Forster:2019]. Additionally, recently developed tools such as CarveMe and gapseq [@Machado:2018], [@Zimmermann:2021] allow a fast and easy generation of genome-scale metabolic models, and can provide mechanistic bases for the prediction of metabolites exchange among species. The use of these models in mathematical modelling frameworks can also simulate metabolic interactions [@Diener:2020;@Bauer et al, 2017]. However, the output files obtained from these analyses are of difficult interpretation, and therefore the possibility of obtaining a graphical visualisation of the results can help in understanding the different functional roles of the microbial species. Approaches for the graphical visualisation of metabolites exchanged in complex communities accounting for more than two microbial species, are already existing [@Bauer:2017;@Diener:2020]. However, these software require the import of results from flux balance simulations in a separated environment, thus requesting programming knowledge. Furthermore, these systems are not designed for metagenomic data, and, as a consequence, they don’t include information regarding microbial abundances and taxonomic assignment, which are compulsory for a meaningful biological interpretation of the results. To fill this gap, we have developed NEMETEX (NEtwork for METabolic EXchanges),  a Python script to graphically visualise the metabolites exchanged in a microbiome obtained through FBA simulations, integrating features of the microbial community like taxonomy and species abundance. 

# Methods and implementation
NEMETEX is a tool implemented in Python 3, and developed in order to obtain a visual representation of the potential cross-feedings between community members. The source code is available in the dedicated GitHub repository and for its functioning the libraries Numpy v1.15.1, Pandas v0.23.4, NetworkX v2.1., PyVis v0.1.9, argparse v2.0.1, os are needed.
As depicted in the workflow diagram illustrating the pipeline \autoref{fig:figure1}, the script requires three input files reporting (i) the compounds exchanged, (ii) the species abundance and (iii) the taxonomic assignment for the species. 
i. Metabolites exchange rate is imported from the output file (.tsv format) generated by SMETANA software (v1.0.0) (Species METabolic interaction ANAlysis) [@Zelezniak:2015]. The “receiver” and the “donor” species are identified along with the exchange rate (smetana value) of each compound from the tabular file. 
ii. Relative abundance of each species is imported as a tabular file generated using checkM (v1.0.12) [@Parks:2015]. 
iii. The species taxonomy is defined from GTDB-Tk (v1.3.0) software [@Chaumeil:2019] and converted to the NCBI taxonomy using the script gtdb_to_ncbi_majority_vote.py.
The script provides as output not only the network in html format, but also three global summary files reporting for all compounds the number of exchanges for each compound, the donor and receiver species. A preliminary inspection of these latter files can be helpful in order to select what are the compounds the user would like to investigate more in detail with the graphical representation. 
Finally, the tool requires the compound of interest (extended name, biggID, or ModelSEED ID) as input to visualise how it is exchanged within the community. The image reporting the network is generated together with two files describing the behaviour of the species (donor-receiver) in the exchange of the compound of interest and reporting the exchanges information. It is also possible to provide the tool with a text file with the list of compounds, one per line. In the latter case, NEMETEX will generate the three output files for each compound in separate directories.

# Results
The main output provided by NEMETEX consists of an HTML file reporting an interactive network that allows to visualise in an easy way the metabolic exchanges of the compounds of interest. In the network, the nodes represent the microbial species, with edges showing the directional exchanges between them. The HTML file generated can be used for the dynamic visualisation of the network (Supplementary file I). The graphical representation is tailored to help the user in the identification of the network, and simplify data interpretation. The diameter of each node is proportional to the species relative abundance for an easier identification of dominant species in the community. In the final rendering, the nodes are colored according to the taxonomic assignment at phylum level to facilitate the investigation on specific taxonomic groups. Arrows thickness refers instead to the probability of exchange as calculated by SMETANA [@Zelezniak:2015], and the relative value can be directly displayed by moving the mouse cursor over the edge.  Additional information can be visualised by moving the mouse cursor over the nodes, including for example the taxonomic assignment of the species at phylum level, their relative abundance, and the species receiving the compound under investigation. The user will be further supported in the interpretation of the results thanks to the supplementary output tabular files reporting some basic statistics calculated from SMETANA output. 
The tool was tested with results obtained from a genome-centric metagenomic analysis performed on samples collected from an anaerobic biogas reactor (still unpublished). As an illustrative example of the NEMETEX output format, analysis of the butyrate exchanges within the selected microbial community, is shown in \autoref{fig:figure1}. In this example, there are four main phyla involved, Firmicutes is colored in red, Proteobacteria in blue, Synergistetes in yellow, and Bacteroidetes in green. Five of the reconstructed genomes cannot be assigned at species level by GTDB-Tk, while only Aminobacterium colombiense was clearly assigned to the species level. The network has to be interpreted as follows: three donor species were identified (Clostridiales sp. DTU-UNIPD956, Candidatus Dethiobacteraceae sp. DTU-UNIPD931 and Burkholderiales sp. DTU-UNIPD944), and three receivers (Aminobacterium colombiense DTU-UNIPD933, Petrimonas sp. DTU-UNIPD925 and Clostridiales sp. DTU-UNIPD956). The dominant species represented in the microbial community (Clostridiales sp. DTU-UNIPD956), with a relative abundance  of 0.85%, can be easily identified from the circle diameter, as well as the main exchanges of the compounds which are evidenced by the edges thickness.

# Limitations
NEMETEX has been developed considering the typical structure of the output files obtained from a genome-centric metagenomic experiment; these files include MAGs with known relative abundance calculated from alignment of the shotgun sequences on the reference assembly, and with taxonomy determined using reference genes. However, the tool can be easily adapted to the simulations performed with known species. The tool is strictly linked to the output files describing metabolites exchange and obtained using SMETANA [@Zelezniak:2015], to the relative abundance of species obtained using checkM [@Parks:2015], and to the taxonomic assignment obtained using GTDB-Tk. The tool can certainly be adapted to import output files obtained from other tools such as BAT [@von Meijenfeldt:2019] or coverM (https://github.com/wwood/CoverM), and authors are planning to include these options in future releases of NEMETEX. Additionally, if the desired compound is exchanged by a high number of species, the generated network can become very complex. In this case, the network representation encounters its limit. However, the reported statistics can give an insight on the pivotal donors and receivers. 

# Conclusions
NEMETEX enables a meaningful visualisation of metabolic exchanges within microbial communities and provides statistics of the FBA results. The tool is particularly suited for results obtained from SMETANA simulations. Unlike previously developed approaches, NEMETEX integrates information of metagenomic data composition and taxonomy in the network. This feature will simplify the identification of the most relevant metabolites exchange among species, and will greatly improve the biological interpretation of the results.

# Funding
This work was financially supported by the project “Sviluppo Catalisi dell’Innovazione nelle Biotecnologie” (MIUR ex D.M.738 dd 08/08/19) of the Consorzio Interuniversitario per le Biotecnologie” (CIB), and by the project LIFE20 CCM/GR/001642 - LIFE CO2toCH4 of the European Union LIFE+ program.


# CRediT authorship contribution statement
Michela Palamin: Methodology, Software,  Writing - Original Draft, Writing - Review & Editing. Alice Frisinghelli: Validation, Writing - Original Draft, Writing - Review & Editing. Elisabetta Offer: Validation, Investigation, Data curation, Writing - Review & Editing, Visualization. Guido Zampieri: Writing - Review & Editing. Arianna Basile: Conceptualization, Supervision, Methodology, Software, Visualization, Writing - Original Draft, Writing - Review & Editing. Stefano Campanaro: Conceptualization, Supervision, Project administration, Funding acquisition, Writing - Original Draft, Writing - Review & Editing.


# Figures


![\label{fig:logo}](logo.png)
![(A) NEMETEX workflow. (B) Butyrate exchanges in the microbiome under investigation. Colour and size of each node refer respectively to taxonomic assignment at phylum level and species relative abundance. Arrows reflect directionality of metabolite exchange, whereas thickness indicates exchange probability.\label{fig:figure1}](figure1.png)


# References

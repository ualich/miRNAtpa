# miRNAtpa
**Micro RNA target prediction analysis** (**miRNAtpa**) is a tool for predicting the importance of each miRNA in gene regulation when specific parameters are given. The analysis considers both intermolecular interactions and tissue-specific expression levels of miRNA.

There are 2 parameters that can be customized:
* list of body regions
* list of target genes

> **NOTE**: This tool does not provide fully automated analysis. Manual download of data is required.

## Interaction data
Data about interactions miRNAs have with specific genes and their gene products is obtained from 5 biological databases:

* [DIANA microT](http://diana.imis.athena-innovation.gr/DianaTools/index.php?r=microT_CDS/index)
* [miRDB](http://mirdb.org/)
* [miRmap](https://mirmap.ezlab.org/app/)
* [miRWalk](http://mirwalk.umm.uni-heidelberg.de/)
* [TargetScan](http://www.targetscan.org/)

## Expression data
The expression of miRNA varies by tissue and developmental period of the organism.
Expression data was obtained from 2016 study _Distribution of miRNA expression across human tissues_ by Ludwig et al. (DOI: 10.1093/nar/gkw116).


## Requirements

* Git
* Python 3.6 or later

## Install

```bash
git clone https://github.com/ualich/miRNAtpa.git
cd miRNAtpa
pip3 install .
```

## Usage

1. Prepare file architecture:
   * Select _analysis name_. Use alphanumeric characters.
   * Create _analysis directory_ inside `analyses`, use analysis name.
   * Create a subdirectory `input` inside analysis directory.


2. Create a subdirectory inside `input` for every biological database and download interaction data (see directory `anayses/example/input`):
    * `diana` - download results as CSV file
    * `mirdb` - download results as HTML file (save webpage)
    * `mirmap` - download results as CSV file
    * `mirwalk` - export results as CSV file
    * `targetscan` - download table as TXT file
   

3. Run the command

   ```bash
   python3 mirnatpa/main.py <analysis_name> <regions>
   ```

   Where
   
   * `analyses_name` - alphanumerical name of the analysis
   * `regions` - space separated names of regions used for expression analysis, possible values can be found in the file `expression/regions.txt`


4. Results will be generated inside analysis directory, in subdirectory `results`.

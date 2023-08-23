# multimodal_ndm
This repository contains code to optimise a multimodal connectome for modelling pathology propagation with the network diffusion model ([Raj et al, 2012](https://www.sciencedirect.com/science/article/pii/S0896627312001353)). More information can be found in the corresponding manuscript: "Combining multimodal connectivity information improves modelling of pathology spread in Alzheimer's Disease". 

## Installation Instructions
```bash
# Use conda to install the relevant packages:
conda env create --name multimodal_ndm --file environment.yml
conda activate multimodal_ndm

# pip install the source files
pip install -e .
```

## Connectome Data
We used multimodal brain connectivity data from the [MICA-MICS dataset](https://osf.io/j532r/): [https://doi.org/10.1101/2021.08.04.454795](https://pubmed.ncbi.nlm.nih.gov/36109562/)

Group averaged connectomes, parcellated with the Desikan-Killiany atlas, are stored in `data/connectomes`. The parcels have been reordered to match the order in `data/TauRegionList.csv`. Please cite the MICA-MICS paper if you use these data.

## Pathology Data
In our manuscript, we compare the model predictions with pathology data: tau-PET SUVRs and cortical atrophy derived from structural MRI, from the ADNI and A4 datasets. These data can be obtained upon sending a request that includes the proposed analysis and the named lead investigator, at [http://adni.loni.usc.edu/data-samples/access-data/](http://adni.loni.usc.edu/data-samples/access-data/) and [https://ida.loni.usc.edu/home/projectPage.jsp?project=A4](https://ida.loni.usc.edu/home/projectPage.jsp?project=A4), respectively.  

All the data used in the analysis was parcellated with the Desikan-Killiany atlas. We have included a dummy dataset (`data/dummmy_pathology.csv`) for testing. When using your own pathology data, make sure that the parcels follow the correct order, as given in `data/TauRegionList.csv`.

## Usage Instructions
### unimodal connectomes
To run the network diffusion model with a single connectome as the substrate, you can run `scripts/run_ndm.py`.

```
usage: run_ndm.py [-h] conn_type conn_path thr data_path data_name

positional arguments:
  conn_type   type of connectome
  conn_path   path to the connectome, saved as a comma delimited csv file
  thr         threshold for the connectome - proportion of strongest weights retained [0-1]
  data_path   path to the target data (tau SUVRs, atrophy etc.)
  data_name   name of your target data, eg.tau

optional arguments:
  -h, --help  show this help message and exit
```
For example, to evaluate the performance of the model for modelling your tau data with a connectome from tractography as a substrate, you would run: 

```
python run_ndm.py tractography ../data/connectomes/tractography.csv 0.1 ../data/tau_data.csv tau
```

### multimodal connectome optimisation
For optimising a multi-modal connectome for the modelling of a particular pathology type, use `scripts/run_optimisation.py`:

```
usage: run_optimisation.py [-h] [-n_iter N_ITER] [-n_starts N_STARTS] [-seed SEED] data_name data_path [conn_names ...]

positional arguments:
  data_name           name for the data, eg. tau, atrophy
  data_path           path to the csv where the data is saved
  conn_names          select the connectomes you want to include in the combined connectome, options = {tractography, geodesic,
                      functional, morphological, microstructural}

optional arguments:
  -h, --help          show this help message and exit
  -n_iter N_ITER      number of iterations for the GP minimiser (default=500)
  -n_starts N_STARTS  number of random initialisations for the GP minimiser (default=300)
  -seed SEED          seed region to initialise the network diffusion model (default = Inferiortemporal)
```

Example usage:

```
python run_optimisation.py atrophy ../data/atrophy_data.csv tractography functional morphological -seed Entorhinal
```

There must be a .txt file present in `data` specifying the threshold values to use for each connectome. Examples are already provided with the optimal thresholds for the tau and atrophy datasets used in the paper, as well as for the dummy dataset (ie. `data/dummy_thresholds.txt`). 

Seed regions are bilateral and currently limited to those in the Desikan-Killiany atlas. Region names must be formated as in the first column of `data/TauRegionList.csv`, without the `_L` or `_R` subscript (eg. `Paracentral`, `Fusiform`).

## Citation
Citation (preprint): E. Thompson, A. Schroder, T. He, C. Shand, S. Soskic, N.P. Oxtoby, F. Barkhof, D.C. Alexander, "Combining multimodal connectivity information improves modelling of pathology spread in Alzheimer's Disease", 


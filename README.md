# multimodal_ndm
This repository contains code to optimise a multimodal connectome for model pathology propagation using the network diffusion model ([Raj et al, 2012](https://www.sciencedirect.com/science/article/pii/S0896627312001353)). Code used in the manuscript: "Combining multimodal connectivity information improves modelling of pathology spread in Alzheimer's Disease". 

## Installation instructions
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

## usage instructions
Running the network diffusion model with different connectomes, controlling the threshold value, seed region and ..

Optimising a multi-modal connectome for the modelling of a particular pathology type.

## Citation
Citation (preprint): E. Thompson, A. Schroder, T. He, C. Shand, S. Soskic, N.P. Oxtoby, F. Barkhof, D.C. Alexander, "Combining multimodal connectivity information improves modelling of pathology spread in Alzheimer's Disease", 


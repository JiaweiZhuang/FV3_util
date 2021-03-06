Code for the paper "The importance of vertical resolution in the free troposphere for modeling intercontinental plumes" on Atmospheric Chemistry and Physics (ACP)
--------
[![DOI](https://zenodo.org/badge/95622791.svg)](https://zenodo.org/badge/latestdoi/95622791)

Link to the paper: https://www.atmos-chem-phys.net/18/6039/2018/

Authors
--------
Jiawei Zhuang, Daniel J. Jacob, Sebastian D. Eastham

Technical note for GFDL-FV3 model configuration
--------
See [technical_note.txt](technical_note.txt)

The build scripts assume Harvard's Odyssey cluster and NASA's Pleiades supercomputer.
Might need to be adjusted for your system environment.

Python notebook for data analysis
--------
See the folder [data_analysis/](./data_analysis)

In general, simple line plots (mixing ratio, entropy, profile) can be reproduced by simply running the notebook. Plots on map require TBs of data that cannot be hosted here. They are available upon request, or can be reproduced by rerunning the model.
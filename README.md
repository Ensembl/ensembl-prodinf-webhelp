# ensembl-prodinf-djcore

This repository contains a set of useful core Django functionalities that may be extended in other pass included in current Ensembl Production Services portal - avoiding circular references for the most part.

INSTALL
=======

1. clone the repo
   
    git clone https://github.com/Ensembl/ensembl-prodinf-djcore

2. cd ensembl-prodinf-djcore
   
3. setup.py sdist 
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    setup.py sdist
    pip install sdist/[package_name].tar.gz
    ```
   
    pip install -e https://github.com/Ensembl/ensembl-prodinf-djcore#egg=ensembl-prodinf-djcore


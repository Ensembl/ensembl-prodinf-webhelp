[![Build Status](https://travis-ci.com/Ensembl/ensembl-prodinf-webhelp.svg?token=uixv5pZneCqzQNs8zEJr&branch=main)](https://travis-ci.com/Ensembl/ensembl-prodinf-webhelp)
[![codecov](https://codecov.io/gh/Ensembl/ensembl-prodinf-webhelp/branch/main/graph/badge.svg?token=gPEZbprnc7)](https://codecov.io/gh/Ensembl/ensembl-prodinf-webhelp)

# ensembl-prodinf-webhelp

This repository contains Django admin Portable app to edit Ensembl Web Help content. 

INSTALL
=======

1. clone the repo
   
    git clone https://github.com/Ensembl/ensembl-prodinf-webhelp

2. cd ensembl-prodinf-webhelp
   
3. Install dependencies in you favorite virtual env
   
   ```
   pip install -r requirements.txt
   ```

4. Install and run test app

   ```shell
   ./src/manage.py migrate
   ./src/manage.py runserver
   ```


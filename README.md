# COVID19 and Associated Trends

## Prerequisits
Python >= 3.8 

## Install
### Install libraries
```bash
# For MacOS
brew install openblas
brew install lapack

export DYLD_LIBRARY_PATH=/Users/magicii/git/uthealth/covid19-google-trends/ENV/lib:/usr/local/lib:/usr/lib:/usr/local/opt/openblas/lib
```
### Install VirtualEnv

```bash
pip install virtualenv
virtualenv ./ENV
. ./ENV/bin/activate
```
### Install packages
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py -p
python main.py -f
```

## TODO
- [] Incoporate with Mobility data
- [] Incoporate with Twitter data
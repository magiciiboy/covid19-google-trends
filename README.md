# COVID19 and Associated Trends

## Prerequisits
- Python >= 3.8
- Docker Compose
- VSCode Server

## Start with VirtualEnv
### Initiate environment
```bash
virtualenv ./ENV
. ./ENV/bin/activate
```

### Install packages
```bash
pip install -r requirements.txt
```

## Start with Docker Compose
Library `pmdarima` requires system libraries which are not available on some OS. Therefore, I created a docker image to let contributors run this project with OS independent.
### Run Docker Compose
```bash
docker-compose up
```

### Open VSCode in browser
Open http://localhost:8989/ in your browser to access to VSCode in Docker instance.

## Analytic Commands
### Download new data from Google Trends
```bash
python main.py -d
```

### Plot figures
Only available in Docker image
```bash
python main.py -f
```

## TODO
- [] Incoporate with Mobility data
- [] Incoporate with Twitter data
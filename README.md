# mini-rag-app

## requirements

- Python 3.8 or later

## Install Python using MiniConda

1) Download & Install MiniConda
2) Create new environment using following command:

```bash
   $ conda create -n mini-rag-app python=3.8
```

3) Activate the environment using following command:

```bash
   $ conda activate mini-rag-app
```
## Installation

## Install required packages  
```bash
   $ pip install -r requirements.txt
```

## Run Project using uvicorn
```bash
   $ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
## Setup environments variables       
```bash
   $ cp .env.example .env 
```
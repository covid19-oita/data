#
# Makefile for manual update data
#
NAME=update_data
SHELL := /bin/bash

PYTHON_VERSION=3.8.3-alpine

PATIENTS_DATA_URL=http://data.bodik.jp/dataset/f632f467-716c-46aa-8838-0d535f98b291/resource/3714d264-70f3-4518-a57a-8391e0851d7d/download/440001oitacovid19patients.csv
DATA_SUMMARY_URL=http://data.bodik.jp/dataset/f632f467-716c-46aa-8838-0d535f98b291/resource/96440e66-3061-43d6-adf3-ef1f24211d3a/download/440001oitacovid19datasummary.csv
FINANCIAL_NUMBER_URL=http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/a56764ef-baba-4972-8877-e773c24d27ca/download/440001oitacovid19finnumber.csv
FINANCIAL_AMOUNT_URL=http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/9c609301-4800-4f06-a400-62ba5eb489ba/download/440001oitacovid19finamount.csv
FINANCIAL_TYPE_URL=http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/3be72fdc-d8e7-4042-bbcd-e05e8dc6bae2/download/440001oitacovid19fintype.csv
EMPLOYMENT_SUBSIDY_URL=http://data.bodik.jp/dataset/a099a7d0-8393-4982-89c3-bee49ddfcecd/resource/226c523f-178d-4180-8a1c-16e492757378/download/440001oitaemploymentsubsidy.csv

all: get_data start exec stop rmi

get_data:
	curl -sS -o "./csv/440001oitacovid19patients.csv" $(PATIENTS_DATA_URL)
	curl -sS -o "./csv/440001oitacovid19datasummary.csv" $(DATA_SUMMARY_URL)
	curl -sS -o "./csv/440001oitacovid19finnumber.csv" $(FINANCIAL_NUMBER_URL)
	curl -sS -o "./csv/440001oitacovid19finamount.csv" $(FINANCIAL_AMOUNT_URL)
	curl -sS -o "./csv/440001oitacovid19fintype.csv" $(FINANCIAL_TYPE_URL)
	curl -sS -o "./csv/440001oitaemploymentsubsidy.csv" $(EMPLOYMENT_SUBSIDY_URL)

start:
	docker run -it --rm -d -v `pwd`:/app --name update_data python:$(PYTHON_VERSION)

exec:
	docker exec -it update_data /usr/local/bin/pip install feedparser
	docker exec -it update_data /usr/local/bin/python /app/tool/convert/main.py

stop:
	docker stop update_data

rmi:
	docker rmi -f python:$(PYTHON_VERSION)
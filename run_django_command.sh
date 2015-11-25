#!/bin/bash
FILE_NAME=$(date +"%d_%m_%Y")
python manage.py print_models 2> ${FILE_NAME}.dat
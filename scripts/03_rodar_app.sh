#!/usr/bin/env bash
set -e

export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_NAME=dimdim_564928
export DB_USER=root
export DB_PASSWORD=senha_564928

python3 app.py

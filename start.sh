#!/bin/bash
echo "Ativando ambiente virtual..."
source venv/Scripts/activate

echo "Subindo a API..."
uvicorn main:app --reload
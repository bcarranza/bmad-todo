#!/bin/bash

# TODO App Setup Script
# This script sets up the development environment

set -e

echo "🚀 TODO App - Development Setup"
echo "================================"

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements-dev.txt

# Initialize database
echo "💾 Initializing database..."
alembic upgrade head

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "The app will be available at:"
echo "  Frontend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""


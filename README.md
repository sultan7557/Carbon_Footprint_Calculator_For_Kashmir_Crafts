# Carbon Footprint Calculator for Kashmiri Crafts

A web application that calculates the carbon footprint of Kashmiri craft products based on materials, processing, transportation, and other factors.

## Features
- Multi-category carbon footprint calculation
- Dynamic form that updates based on craft selection
- Geographic distance calculation
- Sustainability recommendations
- PostgreSQL database for data storage

## Setup
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Unix/macOS) or `venv\Scriptsctivate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure PostgreSQL and update .env file
6. Run with: `uvicorn app.main:app --reload`


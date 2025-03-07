import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
ENCODERS_PATH = os.getenv("ENCODERS_PATH")

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add src to pythonpath
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

# Load Environment
load_dotenv(current_dir.parent / '.env')

from cli import app

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

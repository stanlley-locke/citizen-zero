import sys
import os
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))
# Add admin_cli src to path too, to reuse api_client if needed, or we just copy it.
# Ideally we should have a shared lib, but for now we'll duplicate or import relative.
sys.path.append(str(current_dir.parent.parent / 'admin_cli' / 'src'))

load_dotenv(current_dir.parent / '.env')

from cli import app

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

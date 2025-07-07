import sys

from src.api import app

if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)

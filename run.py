import sys
import traceback
from datetime import datetime
import os
import uvicorn

from app.config import debug

# ✅ Define your error folder path here
ERROR_FOLDER = r"C:/Users/WOLFGANG/Blaq_Github/ai-market-tracker/error_logs"   # Change this

# Make sure the folder exists
os.makedirs(ERROR_FOLDER, exist_ok=True)

def handle_exception(exc_type, exc_value, exc_traceback):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"error_{timestamp}.txt"
    
    # ✅ Build full file path using the variable
    full_path = os.path.join(ERROR_FOLDER, filename)

    with open(full_path, "w") as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

    print(f"Error saved to: {full_path}")

sys.excepthook = handle_exception

# -----------------------------------------------------------------------------
# Run Server
# -----------------------------------------------------------------------------

# print(sys.path)

if __name__ == "__main__":
        uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=debug,
    )
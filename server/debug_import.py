import sys
import traceback

try:
    import main
    print("SUCCESS: logic imported successfully")
except Exception:
    traceback.print_exc()

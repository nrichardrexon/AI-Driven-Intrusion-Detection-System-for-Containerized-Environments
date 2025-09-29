# setup_env.py
"""
Environment Setup Script
- Installs dependencies from requirements.txt
- Prepares folder structure for ML-IDS project
"""

import os
import subprocess

# Required folders
folders = [
    "src",
    "data",
    "notebooks",
    "tests"
]

# Create folders if missing
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Created folder: {folder}")
    else:
        print(f"✅ Folder already exists: {folder}")

# Check requirements.txt
req_file = "requirements.txt"
if not os.path.exists(req_file):
    print("⚠️ requirements.txt not found. Creating default one...")
    with open(req_file, "w") as f:
        f.write(
            "pandas\n"
            "numpy\n"
            "scikit-learn\n"
            "torch\n"
            "fastapi\n"
            "uvicorn\n"
            "prometheus-client\n"
            "python-json-logger\n"
            "pytest\n"
        )

# Install dependencies
print("\n📦 Installing dependencies...")
subprocess.check_call(["pip", "install", "-r", req_file])

print("\n✅ Environment setup complete!")

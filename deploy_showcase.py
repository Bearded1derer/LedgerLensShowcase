import os
import shutil
import subprocess
import sys

# Configuration
REPO_URL = "https://github.com/Bearded1derer/LedgerLensShowcase.git"
ASSETS_DIR = "assets"

# Map original filenames to clean destination filenames
IMAGE_MAPPING = {
    "Screenshot 2026-01-12 151310.png": "step1_ingestion.png",
    "Screenshot 2026-01-12 151343.png": "step2_audit.png",
    "Screenshot 2026-01-12 151412.png": "step3_cleanup.png"
}

def run_command(command):
    """Runs a shell command and prints output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"✅ Success: {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {command}")
        print(e.stderr)
        return None

def organize_images():
    """Creates assets folder and moves/renames images."""
    print("--- 📂 Organizing Images ---")
    
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        print(f"Created directory: {ASSETS_DIR}")

    for original, new_name in IMAGE_MAPPING.items():
        if os.path.exists(original):
            destination = os.path.join(ASSETS_DIR, new_name)
            shutil.move(original, destination)
            print(f"Moved: '{original}' -> '{destination}'")
        else:
            # Check if it already exists in destination (re-run scenario)
            destination = os.path.join(ASSETS_DIR, new_name)
            if os.path.exists(destination):
                print(f"Skipping: '{new_name}' already exists in assets.")
            else:
                print(f"⚠️ Warning: Could not find '{original}' in current directory.")

def git_operations():
    """Initializes git and pushes to remote."""
    print("\n--- 🚀 Starting Git Operations ---")

    # 1. Initialize Git if not present
    if not os.path.exists(".git"):
        run_command("git init")
    
    # 2. Add Remote (safely)
    existing_remotes = run_command("git remote -v")
    if existing_remotes and "origin" not in existing_remotes:
        run_command(f"git remote add origin {REPO_URL}")
    elif not existing_remotes:
         run_command(f"git remote add origin {REPO_URL}")
    else:
        print("Remote 'origin' already exists.")

    # 3. Rename branch to main (standard practice)
    run_command("git branch -M main")

    # 4. Add all files
    run_command("git add .")

    # 5. Commit
    run_command('git commit -m "Deploy LedgerLens Showcase: Auto-organized assets"')

    # 6. Push
    print("\nAttempting to push to GitHub...")
    push_result = run_command("git push -u origin main")
    
    if push_result is not None:
        print("\n✨ SUCCESS! Your showcase is live on GitHub.")
        print(f"Repository: {REPO_URL}")
        print("To view your site live, go to Repo Settings -> Pages -> Source: 'Deploy from a branch' (main)")

if __name__ == "__main__":
    print("LedgerLens Showcase Deploy Tool")
    print("-------------------------------")
    
    # Check if git is installed
    if shutil.which("git") is None:
        print("❌ Error: Git is not installed or not in your PATH.")
        sys.exit(1)

    organize_images()
    git_operations()

import subprocess
import time
import webbrowser
import sys

def run(cmd, cwd=None):
    return subprocess.Popen(cmd, cwd=cwd, shell=True)

if __name__ == "__main__":
    print("🚀 Starting SpaceScope...")

    # Start backend
    print("▶ Starting backend...")
    backend = run("docker compose up -d backend celery_worker celery_beat")

    time.sleep(4)

    # Start frontend
    print("▶ Starting frontend...")
    frontend = run("docker compose up -d frontend")

    time.sleep(5)

    # Open browser tabs
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:5173")
    webbrowser.open("http://localhost:8000/docs")

    print("✅ SpaceScope is running!")
    print("Frontend → http://localhost:5173")
    print("Backend Docs → http://localhost:8000/docs")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        subprocess.run("docker compose down", shell=True)
        sys.exit(0)

import subprocess

def run_dvc():
    subprocess.run(["dvc", "init", "--no-scm"], check=True)
    subprocess.run(["dvc", "remote", "add", "-d", "gcsremote", "gcs:// aniflix-dataset-bucket"], check=True)
    subprocess.run(["dvc", "pull"], check=True)

def run_streamlit():
    subprocess.run([
        "streamlit", "run", "main.py",
        "--server.port", "8080",
        "--server.headless", "true"
    ], check=True)

if __name__ == "__main__":
    run_dvc()
    run_streamlit()

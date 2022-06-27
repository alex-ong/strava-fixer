from strava_offline import cli
import subprocess

def main():
    cmd = "pipenv run python -m strava_offline sqlite"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()
    cmd = "pipenv run python -m strava_offline gpx"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()



if __name__ == "__main__":
    main()    
    
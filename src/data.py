from pathlib import Path
import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

def download_seasons(start_year=2005, end_year=2026):
    for y in range(start_year, end_year + 1):
        code = f"{str(y)[2:]}{str(y + 1)[2:]}"   # 2005 -> "0506"
        url = f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
        out = RAW / f"E0_{code}.csv"
        if out.exists():
            continue
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        out.write_bytes(r.content)
        print("downloaded", out.name)

if __name__ == "__main__":
    download_seasons()

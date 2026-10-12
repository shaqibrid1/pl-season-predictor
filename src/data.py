from pathlib import Path
import requests
import pandas as pd

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
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

def load_matches() -> pd.DataFrame:
    frames = []
    for f in sorted(RAW.glob("E0_*.csv")):
        df = pd.read_csv(f, encoding="latin-1")
        df["season"] = f.stem.split("_")[1]
        frames.append(df[["season", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]])
    matches = pd.concat(frames, ignore_index=True)
    matches["Date"] = pd.to_datetime(matches["Date"], dayfirst=True)
    return matches.dropna(subset=["FTHG", "FTAG"]).reset_index(drop=True)
if __name__ == "__main__":
    download_seasons()

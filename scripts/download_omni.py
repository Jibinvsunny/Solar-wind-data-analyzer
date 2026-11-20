"""Download OMNI solar wind data files from NASA SPDF.

Downloads, for each year in the range:
  - OMNI2 hourly data:   omni2_YYYY.dat      (low_res_omni)
  - OMNI 5-minute data:  omni_5minYYYY.asc   (high_res_omni, includes SYM-H)
  - optionally OMNI 1-minute data: omni_minYYYY.asc (large: ~100 MB per year)

Files that are already downloaded are skipped, so you can stop and re-run safely.

Usage (from the folder that contains this script):
    python download_omni.py --start 1995 --end 2025 --out data/raw
    python download_omni.py --start 2015 --end 2015 --out data/raw --one-minute
"""

import argparse
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://spdf.gsfc.nasa.gov/pub/data/omni"
SOURCES = {
    "hourly": (f"{BASE}/low_res_omni", "omni2_{year}.dat"),
    "5min": (f"{BASE}/high_res_omni", "omni_5min{year}.asc"),
    "1min": (f"{BASE}/high_res_omni", "omni_min{year}.asc"),
}
FORMAT_NOTES = [
    (f"{BASE}/low_res_omni", "omni2.text"),
    (f"{BASE}/high_res_omni", "hroformat.txt"),
]


def download(url: str, target: Path, retries: int = 3) -> str:
    if target.exists() and target.stat().st_size > 0:
        return "already have"
    tmp = target.with_suffix(target.suffix + ".part")
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as response, open(tmp, "wb") as out:
                while chunk := response.read(1 << 20):
                    out.write(chunk)
            tmp.replace(target)
            return f"downloaded ({target.stat().st_size / 1e6:.1f} MB)"
        except urllib.error.HTTPError as err:
            tmp.unlink(missing_ok=True)
            if err.code == 404:
                return "not on the server (year may not exist yet)"
            if attempt == retries:
                return f"failed: HTTP {err.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
            tmp.unlink(missing_ok=True)
            if attempt == retries:
                return f"failed: {err}"
        time.sleep(5 * attempt)
    return "failed"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Download OMNI data from NASA SPDF.")
    parser.add_argument("--start", type=int, default=1995, help="First year (default 1995)")
    parser.add_argument("--end", type=int, default=2025, help="Last year (default 2025)")
    parser.add_argument("--out", default="data/raw", help="Folder to save files in")
    parser.add_argument("--one-minute", action="store_true", help="Also get 1-minute files (large)")
    parser.add_argument("--no-5min", action="store_true", help="Skip 5-minute files")
    args = parser.parse_args(argv)

    out = Path(args.out)
    kinds = ["hourly"] + ([] if args.no_5min else ["5min"]) + (["1min"] if args.one_minute else [])

    for folder, name in FORMAT_NOTES:
        (out / "format_notes").mkdir(parents=True, exist_ok=True)
        status = download(f"{folder}/{name}", out / "format_notes" / name)
        print(f"{name:<22} {status}")

    failed = 0
    for kind in kinds:
        folder, pattern = SOURCES[kind]
        (out / kind).mkdir(parents=True, exist_ok=True)
        for year in range(args.start, args.end + 1):
            name = pattern.format(year=year)
            status = download(f"{folder}/{name}", out / kind / name)
            failed += status.startswith("failed")
            print(f"{name:<22} {status}")

    print(f"\nDone. Files are in: {out.resolve()}")
    if failed:
        print(f"{failed} file(s) failed. Run the same command again to retry them.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

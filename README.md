# Solar Wind Data Analyzer

A Python pipeline that turns raw solar wind data into a clean, quality-checked dataset ready for statistical and machine-learning analysis.

> **Status:** early development (v0.1 in progress). The pipeline steps below are being built in this order.

## What it does

Give it a raw solar wind file (starting with NASA OMNI; ACE, WIND and DSCOVR later) and it will:

1. **Read** the file into a time-indexed table with clear column names and units.
2. **Replace fill values** (e.g. `9999.99`, `999.9`) with proper missing values.
3. **Flag bad data**: values outside physical limits and isolated spikes.
4. **Find gaps**, fill only short ones, and keep long ones marked as missing.
5. **Resample** to a common cadence (1 min, 5 min or 1 hour).
6. **Add derived parameters**: dynamic pressure, solar-wind electric field (Ey = -V·Bz), IMF clock angle, plasma beta, Alfvén Mach number and the Newell coupling function.
7. **Save** a cleaned file (CSV or Parquet) and a short quality report (how much data survived each step).

## Planned usage

```bash
swda clean data/raw/omni2_2015.dat --cadence 1h --out data/processed/omni2_2015_clean.csv
```

```python
from swda import pipeline

clean, report = pipeline.run("data/raw/omni2_2015.dat", cadence="1h")
print(report)
```

## Project layout

```
src/swda/        the package (reading, cleaning, quality checks, derived parameters)
tests/           automated tests
examples/        notebooks showing the pipeline on real storms
data/raw/        your downloaded data (not uploaded to GitHub)
data/processed/  cleaned output (not uploaded to GitHub)
docs/            notes on data formats and methods
```

## Data sources

- OMNI hourly and 1-min data: NASA Space Physics Data Facility, <https://omniweb.gsfc.nasa.gov/>

Please acknowledge the OMNI data providers when you use their data in publications.

## Author

**Jibin V. Sunny**, space weather and heliophysics researcher (MSc, IIT Indore). Research on corotating interaction regions, interplanetary sheaths and their geomagnetic effects.

## License

MIT, see [LICENSE](LICENSE).

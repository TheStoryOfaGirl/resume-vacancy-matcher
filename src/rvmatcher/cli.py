import asyncio
import json
from pathlib import Path
import pandas as pd

from .pipeline import run_all, summary

async def main():
    cases = json.loads(Path("data/test_cases.json").read_text(encoding="utf-8"))
    results = await run_all(cases)
    print(results.to_string(index=False))
    print("\n--- summary ---")
    print(summary(results).to_string())

if __name__ == "__main__":
    asyncio.run(main())
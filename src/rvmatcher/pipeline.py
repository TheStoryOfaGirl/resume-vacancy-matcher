import asyncio
import pandas as pd
from IPython.display import display

from .workflows.one_shot import workflow_one_shot
from .workflows.sequential import workflow_sequential
from .tracing import RunResult

RUNNERS = {
    "one_shot": workflow_one_shot,
    "sequential": workflow_sequential,
}

async def run_case(case: dict, workflows: list[str] | None = None) -> list[dict]:
    workflows = workflows or list(RUNNERS)
    rows = []
    for name in workflows:
        run: RunResult = await RUNNERS[name](case["resume"], case["vacancy"])
        rows.append({
            "case": case["id"], "workflow": name,
            "success": int(run.success),
            "verdict_ok": int(run.success and run.report.verdict == case["verdict_true"]),
            "wall_s": round(run.wall_time_s, 3),
            "calls": run.api_calls,
            "tokens": run.tokens,
            "error": run.error,
        })
    return rows

async def run_all(cases: list[dict]) -> pd.DataFrame:
    all_rows = []
    for case in cases:
        rows = await run_case(case)
        all_rows.extend(rows)
        print(f"{case['id']}: done", flush=True)
    return pd.DataFrame(all_rows)

def summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("workflow", sort=False)
        .agg(
            cases=("case", "size"),
            success_rate=("success", "mean"),
            verdict_accuracy=("verdict_ok", "mean"),
            mean_wall_s=("wall_s", "mean"),
            mean_calls=("calls", "mean"),
            mean_tokens=("tokens", "mean"),
        )
        .round(3)
    )
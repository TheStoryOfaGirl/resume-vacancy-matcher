import argparse
import asyncio
import json
from pathlib import Path
import pandas as pd

from .pipeline import run_all, summary
from .workflows.sequential import workflow_sequential


def _header(title: str) -> None:
    print(f" {title}")


async def run_hw2_success():
    _header("ДЗ 2 | Успешное выполнение workflow")
    cases = json.loads(Path("data/test_cases.json").read_text(encoding="utf-8"))
    case = cases[5]
    run = await workflow_sequential(case["resume"], case["vacancy"])
    print(f"success={run.success}, verdict={run.report.verdict if run.report else None}")
    for s in run.trace:
        print(f"    {s.stage}: success={s.success}, tokens={s.prompt_tokens}/{s.completion_tokens}")


async def run_hw2_invalid():
    _header("ДЗ 2 | Обработка некорректного результата")
    run = await workflow_sequential("Иван Петров", "")   # пустая вакансия
    print(f"success={run.success}")
    print(f"error={str(run.error)[:200]}")
    print(f"stages в trace: {[s.stage for s in run.trace]}")


async def run_hw2_retry():
    _header("ДЗ 2 | Исчерпание retry")
    run = await workflow_sequential("Иван Петров", "")
    attempts = [s for s in run.trace if s.stage == "extract_vacancy"]
    print(f"попыток extract_vacancy = {len(attempts)} (ожидается 3)")
    print(f"все неуспешны: {all(not s.success for s in attempts)}")
    print(f"финальная ошибка: {str(run.error)[:200]}")


async def run_hw1_all():
    _header("ДЗ 1 | Полный прогон one_shot vs sequential")
    cases = json.loads(Path("data/test_cases.json").read_text(encoding="utf-8"))
    results = await run_all(cases)
    print(results.to_string(index=False))
    print(summary(results).to_string())


# Сценарии CLI
SCENARIOS = {
    "hw1": run_hw1_all,
    "hw2-success": run_hw2_success,
    "hw2-invalid": run_hw2_invalid,
    "hw2-retry": run_hw2_retry,
}

async def main():
    parser = argparse.ArgumentParser(
        description="Resume–Vacancy Matcher CLI",
        epilog="Доступные сценарии: " + ", ".join(SCENARIOS.keys())
    )
    parser.add_argument(
        "scenario",
        nargs="?",
        choices=list(SCENARIOS.keys()),
        default="hw1",
        help="Какой сценарий запустить (по умолчанию: hw1)"
    )
    args = parser.parse_args()

    await SCENARIOS[args.scenario]()


if __name__ == "__main__":
    asyncio.run(main())
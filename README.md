# FoodFlow

Екосистема доставки їжі для мережі ресторанів Gusto (навчальний проєкт, ЛР №7).

## Запуск тестів

    PYTHONPATH=src python -m unittest discover -s tests -v

## Метрики якості

    # складність (локальний аналог radon; у CI працює справжній radon)
    python tools/cc_local.py src > reports/complexity.json
    # матриця Hotspots (складність x churn за 90 днів)
    python tools/hotspots.py --complexity reports/complexity.json --out-dir reports

CI/CD: `.github/workflows/quality.yml` (GitHub Actions, контейнер python:3.12-slim) —
тести, `radon cc -s -j`, Churn Rate з git log, матриця Hotspots, артефакт `quality-reports`.

## Примітка про Git-історію

Історія комітів згенерована скриптом (варіант 2 «Штучне наповнення історії»
з методички ЛР №7), щоб мати 90-денне вікно для аналізу Churn Rate. Вікно 90 днів зафіксовано: 2026-08-11 — 2026-11-09
(змінна `CHURN_SINCE` у workflow; для живого режиму використайте `"90 days ago"`).

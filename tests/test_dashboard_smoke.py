"""End-to-end smoke tests: run the pipeline on a tiny dataset, then render the dashboard."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from dashboard_data import MODULES


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard.py"


def _write_csv(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


@pytest.fixture
def pipeline_output_dir(tmp_path: Path) -> Path:
    """Run `python -m src.main` on a dataset with a shortage, an overage and an unmapped SKU."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_csv(data_dir / "order_history.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso,year
        IU Health,tomato,400,22,2025
        Bloomington Coop,Tomatoes,200,22,2025
        IU Health,sweet_corn,300,22,2025
        Bloomington Coop,kale bunch,150,23,2025
        Bloomington Coop,mystery greens,50,23,2025
    """)
    _write_csv(data_dir / "grower_capacity.csv", """\
        grower,crop_canonical,estimated_lbs,week_iso,year
        Hilltop Farm,tomato,450,22,2025
        River Bend,sweet_corn,500,22,2025
        Hilltop Farm,kale,60,23,2025
    """)
    _write_csv(data_dir / "sku_lookup.csv", """\
        crop_raw,crop_canonical
        tomato,tomato
        Tomatoes,tomato
        sweet_corn,sweet_corn
        kale bunch,kale
    """)
    output_dir = tmp_path / "output"
    subprocess.run(
        [sys.executable, "-m", "src.main", "--data-dir", str(data_dir), "--output-dir", str(output_dir)],
        cwd=ROOT,
        check=True,
    )
    return output_dir


def _open_dashboard(output_dir: Path) -> AppTest:
    app = AppTest.from_file(str(DASHBOARD), default_timeout=60)
    app.run()
    output_input = next(widget for widget in app.sidebar.text_input if widget.label == "Output directory")
    output_input.set_value(str(output_dir)).run()
    return app


def test_dashboard_explains_missing_outputs(tmp_path: Path) -> None:
    app = _open_dashboard(tmp_path / "no-outputs-yet")

    assert not app.exception
    assert any("required output files are missing" in error.value for error in app.error)


def test_dashboard_renders_every_module_from_pipeline_outputs(pipeline_output_dir: Path) -> None:
    app = _open_dashboard(pipeline_output_dir)

    for module in MODULES:
        app.sidebar.radio(key="module_nav").set_value(module).run()
        assert not app.exception, f"{module}: {[exc.value for exc in app.exception]}"
        assert not app.error, f"{module}: {[error.value for error in app.error]}"

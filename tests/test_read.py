from datetime import date
from typing import Iterable

import pytest
from pyspark.sql import SparkSession

from shardate.read import Reader
from shardate.dates import all_dates_between
from shardate.utils import date_col


@pytest.fixture(scope="session")
def spark():
    """Create a SparkSession for testing."""
    return SparkSession.builder.getOrCreate()


@pytest.fixture(scope="session")
def start_date() -> date:
    return date(2025, 12, 31)


@pytest.fixture(scope="session")
def end_date() -> date:
    return date(2026, 1, 3)


@pytest.fixture(scope="session")
def target_date() -> date:
    return date(2026, 1, 1)


@pytest.fixture(scope="session")
def target_dates() -> list[date]:
    return [date(2025, 12, 31), date(2026, 1, 1), date(2026, 1, 2)]


@pytest.fixture(scope="session")
def path(spark, start_date, end_date, tmp_path_factory):
    """Create sample YMD-partitioned parquet data for testing."""
    df = spark.createDataFrame(
        [
            {
                "id": index,
                "value": f"data_{index}",
                "y": dt.strftime("%Y"),
                "m": dt.strftime("%m"),
                "d": dt.strftime("%d"),
            }
            for index, dt in enumerate(all_dates_between(start_date, end_date))
        ]
    )
    path = tmp_path_factory.mktemp("test_data")
    df.write.parquet(str(path), partitionBy=["y", "m", "d"], mode="overwrite")
    return path


def test_read_by_date(path: str, target_date: date):
    df = Reader(path).read_by_date(target_date)
    dates = [row["date"] for row in sorted(df.select(date_col()).distinct().collect())]
    assert len(dates) == 1
    assert dates[0] == target_date


def test_read_between(path: str, start_date: date, end_date: date):
    df = Reader(path).read_between(start_date, end_date)
    dates = [row["date"] for row in sorted(df.select(date_col()).distinct().collect())]
    assert dates == list(all_dates_between(start_date, end_date))


def test_read_by_dates(path: str, target_dates: Iterable[date]):
    df = Reader(path).read_by_dates(target_dates)
    dates = [row["date"] for row in sorted(df.select(date_col()).distinct().collect())]
    assert dates == sorted(target_dates)

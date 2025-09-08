"""Shardate: Fast reader for YMD-partitioned Parquet files."""

from shardate.read import read_between, read_by_date, read_by_dates

__version__ = "2025.9.8"
__all__ = ["read_between", "read_by_date", "read_by_dates"]

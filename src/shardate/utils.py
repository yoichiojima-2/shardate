from pyspark.sql import functions as F


def date_col() -> F.col:
    return F.to_date(F.concat_ws("-", F.col("y"), F.col("m"), F.col("d"))).alias("date")

import polars as pl
import numpy as np

def engineer_features(df: pl.DataFrame) -> pl.DataFrame:
    """
    Engineers feature & creates the target variable using Polars expressions.
    :param df: Polars data frame
    :return: polars data frame
    """

    base_occupancy = 0.20

    # Create boolean/integer flags
    df_engineered = df.with_columns(
        pl.col("day_of_week").is_in([5, 6]).cast(pl.Int8).alias("is_weekend"),
        (pl.col("time_of_day") >= 18).cast(pl.Int8).alias("is_peak_hours")
    )

    noise_values = np.random.normal(loc=0.0, scale=0.05, size=len(df))
    noise_series = pl.Series(name="noise", values=noise_values)

    # Create the target variable using the engineered features.
    df_engineered = df_engineered.with_columns(
        (
            base_occupancy +
            (pl.col("is_weekend") * 0.30) +
            (pl.col("is_peak_hours") * 0.20) +
            (pl.col("movie_popularity_score") / 10 * 0.25) -
            (pl.col("days_since_release") / 90 * 0.15) +
            noise_series
    ).clip(lower_bound=0.05, upper_bound=1.0).alias("occupancy_percentage")
    )

    return df_engineered
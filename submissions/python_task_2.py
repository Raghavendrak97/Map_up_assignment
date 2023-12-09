import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = df.pivot(index='start_location', columns='end_location', values='distance')
    distance_matrix = distance_matrix.fillna(0)
    distance_matrix += distance_matrix.T
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    distance_matrix = df.reset_index()
    unrolled_df = pd.melt(distance_matrix, id_vars='start_location', var_name='end_location', value_name='distance')
    unrolled_df.columns = ['id_start', 'id_end', 'distance']
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return dunrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold_range = 0.1 * reference_avg_distance
    filtered_ids = df.groupby('id_start')['distance'].mean().between(reference_avg_distance - threshold_range,
                                                                    reference_avg_distance + threshold_range).index.tolist()
    result_df = pd.DataFrame({'id_start': filtered_ids})

    return result_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.1, 'car': 0.3, 'rv': 0.5, 'bus': 0.7, 'truck': 1.0}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient
    return df

from datetime import datetime, time
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time
    df['start_day'] = pd.to_datetime(df['start_time']).dt.dayofweek.map(day_mapping)
    df['end_day'] = pd.to_datetime(df['end_time']).dt.dayofweek.map(day_mapping)
    time_ranges = [
        ((time(0, 0, 0), time(10, 0, 0)), 0.8),
        ((time(10, 0, 0), time(18, 0, 0)), 1.2),
        ((time(18, 0, 0), time(23, 59, 59)), 0.8)
    ]
    for start_time_range, discount_factor in time_ranges:
        mask = (df['start_time'] >= start_time_range[0]) & (df['end_time'] <= start_time_range[1])
        df.loc[mask, 'vehicle_type'] *= discount_factor
    weekend_mask = (df['start_day'].isin(['Saturday', 'Sunday'])) & (df['end_day'].isin(['Saturday', 'Sunday']))
    df.loc[weekend_mask, 'vehicle_type'] *= 0.7
    return df

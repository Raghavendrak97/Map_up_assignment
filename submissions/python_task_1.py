import pandas as pd

df = pd.read_csv('dataset-1.csv')
def generate_car_matrix(df)->pd.DataFrame:

    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(len(car_matrix))]*2] = 0
    return car_matrix


def get_type_count(df)->dict:

    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], include_lowest=True)
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))
    return sorted_type_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    sorted_bus_indexes = sorted(bus_indexes)
    return sorted_bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    sorted_selected_routes = sorted(selected_routes)
    return sorted_selected_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return mmodified_matrix


df = pd.read_csv('dataset-2.csv')
def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    start_datetime = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    end_datetime = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    duration_minutes = (end_datetime - start_datetime).dt.total_seconds() / 60
    completeness_check = (duration_minutes >= 24 * 60) & (start_datetime.dt.dayofweek == 0) & (end_datetime.dt.dayofweek == 6)
    result_series = completeness_check.groupby([df['id'], df['id_2']]).all()

    return result_series

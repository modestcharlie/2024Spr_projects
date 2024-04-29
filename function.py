import pandas as pd


def sort_correlations(df, column='Correlation', top_n=5):
    """
    Calculate absolute correlation values, sort them, and return the top N correlations.

    Args:
    df (pd.DataFrame): DataFrame containing correlation data.
    column (str): Name of the column containing correlation values.
    top_n (int): Number of top correlations to return.

    Returns:
    pd.DataFrame: DataFrame of top N absolute correlations sorted descending.

    Example:
    >>> test_data = {'Year': [2000, 2001, 2002], 'Correlation': [0.1, -0.2, 0.3]}
    >>> test_df = pd.DataFrame(test_data)
    >>> sort_correlations(test_df, 'Correlation', 2)
       Year  Correlation  Abs_Correlation
    2  2002          0.3              0.3
    1  2001         -0.2              0.2
    """
    df['Abs_Correlation'] = df[column].abs()
    return df.sort_values(by='Abs_Correlation', ascending=False).head(top_n)


import matplotlib.pyplot as plt


def plot_correlations(df, x_col, y_col, title):
    """
    Plot correlation coefficients over time.

    Args:
    df (pd.DataFrame): DataFrame containing the data to plot.
    x_col (str): Column name for x-axis (years).
    y_col (str): Column name for y-axis (correlation values).
    title (str): Title of the plot.
    angle (int): Rotation angle for x-axis labels.

    Returns:
    None: Displays a matplotlib plot.

    Example:
    >>> test_data = {'Year': [2000, 2001, 2002], 'Correlation': [0.1, -0.2, 0.3]}
    >>> test_df = pd.DataFrame(test_data)
    >>> plot_correlations(test_df, 'Year', 'Correlation', 'Sample Correlation Plot', 0)  # doctest: +SKIP
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker='o')
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    plt.show()


def create_correlation_df(correlation_dict, year_col, corr_col):
    """
    Create a DataFrame from a dictionary with correlation data.

    Args:
    correlation_dict (dict): Dictionary with years as keys and correlation values as values.
    year_col (str): Name for the 'Year' column.
    corr_col (str): Name for the 'Correlation' column.

    Returns:
    pd.DataFrame: DataFrame created from the dictionary.

    Example:
    >>> test_dict = {'2000': 0.05, '2001': -0.03}
    >>> create_correlation_df(test_dict, 'Year', 'Correlation')
       Year  Correlation
    0  2000         0.05
    1  2001        -0.03
    """
    df = pd.DataFrame(list(correlation_dict.items()), columns=[year_col, corr_col])
    return df


def parse_state_county(df, location_col):
    """
    Parses a DataFrame to separate state and county names based on the presence of 'County' in the location string.

    Args:
    df (pd.DataFrame): DataFrame containing location data.
    location_col (str): Column name in df where the county or state names are stored.

    Returns:
    pd.DataFrame: DataFrame with new 'State' and 'County' columns.

    Example:
    >>> test_data = {'county_or_state_name': ['Texas', 'Travis County, TX', 'Williamson County, TX']}
    >>> test_df = pd.DataFrame(test_data)
    >>> parse_state_county(test_df, 'county_or_state_name')
        county_or_state_name  State                 County
    1      Travis County, TX  Texas      Travis County, TX
    2  Williamson County, TX  Texas  Williamson County, TX
    """
    df['State'] = None
    df['County'] = None
    current_state = ''

    for index, row in df.iterrows():
        location = row[location_col]
        if 'County' not in location:
            current_state = location  # Update current state
        else:
            df.loc[index, 'State'] = current_state
            df.loc[index, 'County'] = location

    return df[df['County'].notnull()]


def get_decade(year):
    """
    Returns the decade for a given year as a string label.

    Args:
    year (int): The year for which the decade needs to be determined.

    Returns:
    str: A string representing the decade.

    Examples:
    >>> get_decade(1975)
    '1970'
    >>> get_decade(1985)
    '1980'
    >>> get_decade(1995)
    '1990'
    >>> get_decade(2005)
    '2000'
    >>> get_decade(2010)
    '2008-12'
    >>> get_decade(2018)
    '2017-21'
    """
    if 1970 <= year < 1980:
        return '1970'
    elif 1980 <= year < 1990:
        return '1980'
    elif 1990 <= year <= 2000:
        return '1990'
    elif 2000 <= year < 2008:
        return '2000'
    elif 2008 <= year < 2012:
        return '2008-12'
    elif 2017 <= year < 2021:
        return '2017-21'


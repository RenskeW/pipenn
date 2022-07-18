import pandas as pd

PIPENN_COLS = ['class', 'AA', 'name', 'number', 'rel_surf_acc', 'abs_surf_acc', 'z', 'prob_helix', 'prob_sheet',
               'prob_coil']


def load_netsurfp_output(path: str = 'netsurfp_output.txt') -> pd.DataFrame:
    """Loads the data in the correct format.
    TODO Check if Reza wanted these column names

    :rtype: DataFrame
    :param path: str - Path to NetsurfP output
    :return: DataFrame - NetsurfP output in DataFrame format
    """
    df = pd.read_fwf(path, comment='#', header=None, names=PIPENN_COLS, infer_nrows=10000)
    return df


def get_length(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate and append sequence lengths so the NetsurfP output.

    :param df: DataFrame - NetsurfP output in DataFrame format
    :return: DataFrame - NetsurfP output in DataFrame format with sequence lengths
    """

    max_lengths = df.groupby('name')['number'].max()
    max_lengths.name = 'length'
    df.merge(max_lengths, left_on='name', right_on='name')

    return df


if __name__ == '__main__':
    # TODO add argparser to specify netsurfP output path
    df = load_netsurfp_output('netsurfp_output.txt')
    df = get_length(df)

"""
This script converts NetSurfP1 output to PIPENN format
"""
__author__ = 'Arthur Goetzee'

import pandas as pd
import argparse

PIPENN_COLS = ['class', 'AA', 'name', 'number', 'rel_surf_acc', 'abs_surf_acc', 'z', 'prob_helix', 'prob_sheet',
               'prob_coil']

parser = argparse.ArgumentParser(description='Convert netsurfP output and generate features for PIPENN')
parser.add_argument('-f', metavar='F', type=str, action='store', help='NetsurfP output to be converted')


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


# TODO add funtion that obtains uniprotID


if __name__ == '__main__':
    args = parser.parse_args()
    df = load_netsurfp_output(args.f)
    df = get_length(df)

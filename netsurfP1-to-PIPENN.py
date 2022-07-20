"""
This script converts NetSurfP1.1 output to PIPENN format
"""
__author__ = 'Arthur Goetzee'

import pandas as pd
import requests
import argparse  # Part of std library
import json  # Part of std library
import time

PIPENN_COLS = ['class', 'AA', 'name', 'number', 'rel_surf_acc', 'abs_surf_acc', 'z', 'prob_helix', 'prob_sheet',
               'prob_coil']

parser = argparse.ArgumentParser(description='Convert NetSurfP1.1 output and generate features for PIPENN')
parser.add_argument('-f', metavar='F', type=str, action='store', help='NetSurfP1.1 output to be converted',
                    default='netsurfp_output.txt')
parser.add_argument('-o', metavar='O', type=str, action='store', help='Output file in csv format',
                    default='PIPENN_intermediate_input.csv')


def load_netsurfp_output(path: str) -> pd.DataFrame:
    """Loads the data in the correct format.
    TODO Check if Reza wanted these column names

    :rtype: DataFrame
    :param path: str - Path to NetSurfP1.1 output
    :return: DataFrame - NetSurfP1.1 output in DataFrame format
    """
    df = pd.read_fwf(path, comment='#', header=None, names=PIPENN_COLS, infer_nrows=10000)
    return df


def get_length(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate and append sequence lengths so the NetSurfP1.1 output.

    :param df: DataFrame - NetSurfP1.1 output in DataFrame format
    :return: DataFrame - NetSurfP1.1 output in DataFrame format with sequence lengths
    """

    max_lengths = df.groupby('name')['number'].max()
    max_lengths.name = 'length'
    df = df.merge(max_lengths, left_on='name', right_on='name')

    return df


def get_uniprot_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Obtains the UniProtIDs for each of PDB ID's in the data.
    In case of multiple results, the last result is used.
    In case of no results, FAILURE is used.
    Job results are queried max 5 times, with 15 seconds of waiting time in between. Upon timeout, UniprotID column will
    be populated with 'FAILURE' value.

    :param df: DataFrame - NetSurfP1.1 output in DataFrame format
    :return: Original DataFrame appended with UniprotIDs
    """

    raw_pdb_ids = df['name'].unique().tolist()
    pdb_ids = {id[0:4]: id for id in raw_pdb_ids}  # Remove trailing characters, need this later for mapping back
    str_pdb_ids = ','.join(pdb_ids)

    data = {
        'ids': str_pdb_ids,
        'from': "PDB",
        'to': "UniProtKB"
    }

    # POST request
    job_req = requests.post('https://rest.uniprot.org/idmapping/run', data=data)
    jobid = json.loads(job_req.text)['jobId']

    # GET request to get results
    # TODO wait for request to be finished
    job_res = requests.get(f'https://rest.uniprot.org/idmapping/results/{jobid}')

    tries = 0
    while job_res.status_code != 200:  # In case job is not yet ready.
        time.sleep(15)
        job_res = requests.get(f'https://rest.uniprot.org/idmapping/results/{jobid}')
        tries += 1

        if tries > 4:
            print('ERROR: Request timed out. Could not get UniprotIDs!')
            failed_dict = {id: 'FAILED' for id in raw_pdb_ids}
            mapping_df = pd.DataFrame.from_dict(data=failed_dict, orient='index', columns=['uniprotID'])
            df = df.merge(mapping_df, left_on='name', right_index=True)
            return df


    results = json.loads(job_res.text)

    mapping_dict = {}
    for result in results['results']:
        mapping_dict[pdb_ids[result['from']]] = result['to']

    # In case of failure
    for failed in results['failedIds']:
        mapping_dict[pdb_ids[failed]] = 'FAILED'

    mapping_df = pd.DataFrame.from_dict(data=mapping_dict, orient='index', columns=['uniprotID'])
    df = df.merge(mapping_df, left_on='name', right_index=True)
    return df


if __name__ == '__main__':
    args = parser.parse_args()

    df = load_netsurfp_output(args.f)
    df = get_length(df)
    df = get_uniprot_ids(df)

    if not args.o.endswith('.csv'):
        args.o += '.csv'

    df.to_csv(args.o, index=False)

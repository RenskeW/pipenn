import pandas as pd
import numpy as np
import io

print(pd.read_csv('netsurf_example_output.txt', comment='#').head())
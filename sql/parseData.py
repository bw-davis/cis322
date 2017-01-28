import pandas as pd
import numpy as np
import sys 

first_arg = sys.argv[1]
df = pd.read_csv(first_arg)


print(df['asset tag'])
print(df['compartments'])
print(df['intake date'][0])




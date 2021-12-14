import pandas as pd
import numpy as np

data = np.arange(2, 10, dtype=np.float16)
df = pd.DataFrame(data=data, columns=['fp16'])
# Code without the fix
# print(df.dtypes)
# df.to_parquet('./fp16.parquet')

# Code with the fix
float16_cols = list(df.select_dtypes(include=['float16']).columns)
new_types = dict((col,'float') for col in float16_cols)
df = df.astype(new_types)
print(df.dtypes)
df.to_parquet('./fp16.parquet')

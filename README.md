# Test Parquet float16 Support in Pandas

## Background

As I am on leave I was trying to see if I can contribute to some open source projects so while checking out the 
issue tracker of Pandas, I found this open issue. This issue got me chasing into exploring what may be the root
cause of this issue and can this be fixed at some level in Pandas itself. While the fix part is still pending
I found the possible cause and a possible work around to the issue.

## Overview

In this example I am trying to test the Pandas support for Parquet also test the bug reported in
https://github.com/pandas-dev/pandas/issues/44846

## Issue

BUG: Parquet format does not support saving float16 columns

### Reproducible Example

```python
import pandas as pd
import numpy as np

data = np.arange(2, 10, dtype=np.float16)
df = pd.DataFrame(data=data, columns=['fp16'])
df.to_parquet('./fp16.parquet')
```

### Issue Description

Pandas does not validate presence of float16 columns in DataFrame as parquet format does not support saving float16 values.

Sample exception

```
Traceback (most recent call last):
  File "test_parquet_float16.py", line 6, in <module>
    df.to_parquet('./fp16.parquet')
  File "/home/priyab/.conda/envs/airflow/lib/python3.8/site-packages/pandas/util/_decorators.py", line 207, in wrapper
    return func(*args, **kwargs)
  File "/home/priyab/.conda/envs/airflow/lib/python3.8/site-packages/pandas/core/frame.py", line 2677, in to_parquet
    return to_parquet(
  File "/home/priyab/.conda/envs/airflow/lib/python3.8/site-packages/pandas/io/parquet.py", line 416, in to_parquet
    impl.write(
  File "/home/priyab/.conda/envs/airflow/lib/python3.8/site-packages/pandas/io/parquet.py", line 194, in write
    self.api.parquet.write_table(
  File "/home/priyab/.conda/envs/airflow/lib/python3.8/site-packages/pyarrow/parquet.py", line 1782, in write_table
    with ParquetWriter(
  File "/home/priyab/.conda/envs/airflow/lib/python3.8/site-packages/pyarrow/parquet.py", line 614, in __init__
    self.writer = _parquet.ParquetWriter(
  File "pyarrow/_parquet.pyx", line 1385, in pyarrow._parquet.ParquetWriter.__cinit__
  File "pyarrow/error.pxi", line 105, in pyarrow.lib.check_status
pyarrow.lib.ArrowNotImplementedError: Unhandled type for Arrow to Parquet schema conversion: halffloat
```

## Reason

It seems there is already a ticket open in PyArrow & Parquet project to support halffloat or float16, as shown by the below issues

https://github.com/apache/arrow/issues/2691
https://issues.apache.org/jira/browse/ARROW-7242
https://issues.apache.org/jira/browse/PARQUET-1647

But from what I can see is that in the Parquet issue, no response has been taken to address this issue. And in return bubble up to PyArrow & Pandas

## Workaround

For now the workaround seems to change the dtype of any float16 data type to float32.

Code Example

```
float16_cols = list(df.select_dtypes(include=['float16']).columns)
new_type = dict((col,'float') for col in float16_cols)
df = df.astype(new_types)
```

## Motivation

Its more often than not I use pandas to solve a quick Data Analysis problem and I know its not perfect but in many cases it gets the thing done. And this particular issue will also be faced in cases where someone infers the data while reading it and its inferred as float16. The workaround is suitable in only those conditions where you don't need to write float16 to a parquet file.

## Conclusion

The only reason I have did not look at fixing the issue in parquet or in pyarrow implementation is the complexity around touching the base implementation that will take to adding support for a new data type. Also as a work around exists I would rather live with it at a api consumption layer for now.
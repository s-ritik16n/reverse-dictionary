import pandas as pd
from connect_db import get_engine
from print_error import print_error

engine, meta = get_engine()

df = pd.read_sql("definitions", engine)
df.to_csv("db/definitions.csv", sep=":", columns = ["word", "definition"], header = False, index=False, mode = "w")


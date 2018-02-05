import pandas as pd

df = pd.DataFrame([[1,2],[2,3]], columns = ["one","two"], index=None)

print(1 == df["one"])
print(2 == df["one"])
for el in df["one"]:
	print(el)

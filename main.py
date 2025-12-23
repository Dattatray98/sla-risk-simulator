import pandas as pd  #type: ignore 

data = pd.read_csv('data/Insurance_claims_event_log.csv')

pdata = pd.DataFrame(data)


datarow = pdata.head(100)
print(datarow)

datarow.to_csv("data/sample_data.csv", index=False)
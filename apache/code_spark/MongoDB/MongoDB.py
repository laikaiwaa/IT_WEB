import pandas as pd
import matplotlib.pyplot as plt
import csv
import csv
from pymongo import MongoClient
conn=MongoClient('192.168.3.7',27017)
db=conn.health_20180305
u=db.user
m=u.find()

#import json
#f=open('di.json', 'w')
#w='\n'
#for each in m:
#    json.dump(each,f)
 #   f.write(w)
#f.close()
#for each in m:
#    print(each)

n=pd.DataFrame(list(m))


n.to_csv('D://project//MongoDB//t.csv',sep=',', encoding = "utf-8-sig",index=False)



o=n['userType']
p=o.dropna()
print(o.isna().count())
print(p.count())
plt.hist(p)
plt.show()

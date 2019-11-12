import pandas as pd
import xml.etree.ElementTree as et
from random import randint

xtree = et.parse("/Users/rachananarayanacharya/Downloads/Posts.xml")
xroot = xtree.getroot()

df_cols = ["Id", "PostTypeId","Body", "Title"]
rows = []

for node in xroot:
    #print(node.attrib.get("Title"))
    id = node.attrib.get("Id")
    pid = node.attrib.get("PostTypeId")
    body = node.attrib.get("Body")
    title = node.attrib.get("Title")
    if not title:
        title = " "

    rows.append({"Id": id, "PostTypeId": pid,
                 "Body": body, "Title": title})

#print(rows)

posts = pd.DataFrame(rows, columns = df_cols)
posts = posts[posts["PostTypeId"] == "1"]

posts["Body"]=posts["Title"]+posts["Body"]
#print(posts["Body"].head(5))
#posts["Title"].fillna(value=" ", inplace=True)
#print(posts["Id"].head(5))


xtree = et.parse("/Users/rachananarayanacharya/Downloads/PostLinks.xml")
xroot = xtree.getroot()

df_cols = ["PostId", "RelatedPostId"]
rows = []

for node in xroot:
    id = node.attrib.get("PostId")
    rid = node.attrib.get("RelatedPostId")

    rows.append({"PostId": id, "RelatedPostId": rid})

postLinks = pd.DataFrame(rows, columns = df_cols)
merged_inner=pd.merge(left=posts,right=postLinks, left_on='Id', right_on='PostId')

combined_df=pd.merge(left=merged_inner,right=posts, left_on='RelatedPostId', right_on='Id')#body_x body_y


combined_df.drop(['PostTypeId_y', 'PostTypeId_x','Id_y', 'Id_x','Title_x', 'Title_y'], axis=1, inplace=True)
combined_df.rename(columns={"PostId":"qid1", "Body_x": "question1", "RelatedPostId":"qid2", "Body_y": "question2"}, inplace=True)
combined_df.index.names = ['id']

combined_df["is_duplicate"]=1

#print("hii ",combined_df.shape)
#print("hii-1 ",combined_df.head())
# print("hii-1 ",combined_df[1])

pairs_set=set()
for idx, row in combined_df.iterrows():
    #print("hey", row)
    # print("hey1 ", row['qid1'])

    q1=row['qid1']
    q2=row['qid2']
    qpair=""

    if q1<q2:
        qpair=str(q1)+" "+str(q2)
    else:
        qpair=str(q2)+" "+str(q1)
    pairs_set.add(qpair)
    #print(qpair)
cur_size, cur_cols=combined_df.shape
print("initial rows:", cur_size)
for index in range(0, cur_size):
    qpair=""
    while(True):
        id1=combined_df.iloc[randint(0, cur_size-1)].loc["qid1"]#["qid1"]
        id2=combined_df.iloc[randint(0, cur_size-1)].loc["qid2"]
        qpair=str(id1)+" "+str(id2)
        if(not qpair in pairs_set and (not id1==id2)):
            break
    #print(qpair)

    post1=posts.loc[posts['Id'] == id1]
    #print(post1["Body"].item())
    #raise SystemExit
    body1=post1["Body"].item()

    post2=posts.loc[posts['Id'] == id2]
    body2=post2["Body"].item()
    df_entry={"qid1":id1, "question1": body1,"qid2":id2, "question2": body2, "is_duplicate":0}
    combined_df=combined_df.append(df_entry, ignore_index=True)
print("Current size",combined_df.shape)
with open('stack_exchange.csv', 'a') as f:
    combined_df.to_csv(f)
#combined_df.to_csv('stack_exchange.csv')
    #print(post1)
    #body1=post1["Body"]

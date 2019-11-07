import pandas as pd
import xml.etree.ElementTree as et

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
merged_inner_1=pd.merge(left=posts,right=postLinks, left_on='Id', right_on='PostId')

merged_inner_2=pd.merge(left=merged_inner_1,right=posts, left_on='RelatedPostId', right_on='Id')#body_x body_y


merged_inner_2.drop(['PostTypeId_y', 'PostTypeId_x','Id_y', 'Id_x','Title_x', 'Title_y'], axis=1, inplace=True)
for column in merged_inner_2.columns:
    print(merged_inner_2[column].head(5))
#merged_inner_2.drop(['PostTypeId_y', 'PostTypeId_x','Id_y', ' Id_x','Title_x', 'Title_y', ], axis=1)
#merged_inner_2.drop(['B', 'C'], axis=1)


# coding: utf-8

# In[1]:

# Importing the libraries

import pandas as pd
import numpy as np
import re


# ## Data cleaning and Item_Price conversion in float

# In[2]:

# function that will remove the dollar sign from the item_price and convert it in float
def remov(x):
    L = list(x)
    del L[0]
    S = ''.join(L)
    return float(S)


# In[3]:

# Reading the dataset
df = pd.read_csv("chipotle.csv")

p = []

# Converting item_price column into float
for i in df["item_price"]:
    p.append(remov(i))

# Adding the floated item_price to the dataframe
df2 = df
df2["Item_price"] = p
del df2['item_price']
df2.head()


# ## Average quantities and average total price

# In[4]:

# Average quantity and price for all the orders
m = []
id = []
price = []
for i in range(1, 1835):
    id.append(i)
    m.append(df[df2["order_id"] == i]["quantity"].mean())
    price.append(df[df2["order_id"] == i]["Item_price"].mean())
data = {"order_id":id, "mean_quantity":m, "mean_item_price":price}
S = pd.DataFrame(data)
S.head()


# ## Item ordered with the largest total quantity and largest total price

# In[5]:

# creating a list of the item names
Ln = df2["item_name"].unique() 

Ql = []
Pl = []

for i in Ln:
    Ql.append(sum(df2["quantity"][df2["item_name"] == i]))
    Pl.append(sum(df2["Item_price"][df2["item_name"] == i]))

data = {"Largest_total_quantity":Ql, "Largest_total_price":Pl, "item_name":Ln}
LargTot = pd.DataFrame(data)

pmax = LargTot[LargTot["Largest_total_price"] == LargTot["Largest_total_price"].max()]["item_name"]
qmax = LargTot[LargTot["Largest_total_quantity"] == LargTot["Largest_total_quantity"].max()]["item_name"]

print("The item ordered with the largest total quantity is:\t{0}\n\n".format(qmax))
print("The item ordered with the largest total price is:\t{0}".format(pmax))


# ## Find the three top most popular choices that were added to an item

# In[6]:

# List of the Items
L = df2["item_name"].unique()

#List of their occurences in the dataframe.
occur = []
for i in L:
    n = 0
    for j in df2["item_name"]:
        if i == j:
            n += 1
    occur.append(n)
D = dict(zip(L, occur))

M = []
k = []
i = 0
while i != 3:
    M.append(max(D.values()))
    k.append(list(D.keys())[list(D.values()).index(M[i])])
    D.pop(k[i], None)
    i += 1
data = {"Items":k, "Number of orders": M}
Top = pd.DataFrame(data) 
Top


# ## Let us group the item into three types:

# ## Defining the necessary functions

# In[7]:

# Function that looks for the words Burrito and Bowls in the Item name
def B2(x):
    atRegex = re.compile(r'Burrito|Bowl')
    mo = atRegex.search(x)
    if atRegex.search(x) == None:
        return False
    else:
        return True
    
# Function that looks for the words Tacos and Salad in the Item name
def TS(x):
    atRegex = re.compile(r'Tacos|Salad')
    mo = atRegex.search(x)
    if atRegex.search(x) == None:
        return False
    else:
        return True

# Function that looks for the words Sides and Drinks in the Item name
def SD(x):
    atRegex = re.compile(r'Side|Drink')
    mo = atRegex.search(x)
    if atRegex.search(x) == None:
        return False
    else:
        return True


# ## Grouping

# In[8]:

B = df2["item_name"].unique()

# Group Burrito and Bowls
BB = []
for i in B:
    if B2(i) == True:
        BB.append(i)
BB

data = {"Burrito and Bowls": BB}
Grp1 = pd.DataFrame(data)
print(Grp1)

# Group Tacos and Salad
TaSa = []
for i in B:
    if TS(i) == True:
        TaSa.append(i)
TaSa

data = {"Tacos and Salad": TaSa}
Grp2 = pd.DataFrame(data)
print("\n\n",Grp2)

# Group Sides and Drinks
SiDr = []
for i in B:
    if SD(i) == True:
        SiDr.append(i)
SiDr
data = {"Sides and Drinks": SiDr}
Grp3 = pd.DataFrame(data)
print("\n\n", Grp3)


# ## Proportion of orders that include Tacos and Salad types

# In[9]:

n = 0
for i in Grp2["Tacos and Salad"]:
    for j in df2["item_name"]:
        if i == j:
            n += 1
prop = n/len(df2["item_name"])

print("The proportion of orders that include Tacos and Salad types is: \t{0}".format(prop))


# ## Proportion of orders that include Sides and Drinks types

# In[10]:

n = 0
for i in Grp3["Sides and Drinks"]:
    for j in df2["item_name"]:
        if i == j:
            n += 1
prop = n/len(df2["item_name"])

print("The proportion of orders that include Sides and Drinks types is: \t{0}".format(prop))


# In[ ]:



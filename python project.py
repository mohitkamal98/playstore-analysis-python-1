#!/usr/bin/env python
# coding: utf-8

# <b> PLAYSTORE ANALYSIS PROJECT -1
#     

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplot', 'inline')


# In[3]:


data = pd.read_csv(r"C:\Users\mohit\Downloads\Python Assignment 2_BI\playstore_analysis.csv")


# In[4]:


data.head()


# <b> Q1: Data clean up - Missing value treatment

# <b>a. Drop records where rating is missing since rating is our target/study variable

# In[5]:


data.dropna(subset =['Rating'],inplace = True)


# <b>b. Check the null values for the Android Ver column. 

# <b>i. Are all 3 records having the same problem?

# In[6]:


data.loc[data['Android Ver'].isnull()] 


# <b>ii. Drop the 3rd record i.e. record for “Life Made WIFI …
# 

# In[7]:


data.drop([10472], inplace = True)


# In[8]:


data.loc[data['Android Ver'].isnull()]


# <b>iii. Replace remaining missing values with the mode
# 

# In[9]:


data['Android Ver'].fillna(data['Android Ver'].mode()[0], inplace = True)


# <b> c. Current ver – replace with most common value

# In[10]:


data['Current Ver'].fillna(data['Current Ver'].mode()[0],inplace = True)


# <b> Q2: Data clean up- correcting the data types

# <b>a. Which all variables need to be brought to numeric types?

# no,all variable does not need to brought to numeric types but Reviews and install need to brought to numeric types.

# <b>b. Price variable – remove $ sign and convert to float

# In[11]:


Price = []
for i in data['Price']:
    if i[0]=='$':
        Price.append(i[1:])
    else:
        Price.append(i)
    


# In[12]:


data.drop(labels=data[data['Price']=='Everyone'].index, inplace =True)
data['Price']=Price
data['Price']=data['Price'].astype(float)


# <b>c. Installs – remove ‘,’ and ‘+’ sign, convert to integer

# In[13]:


install= []
for j in data['Installs']:
    install.append(j.replace(',','').replace('+','').strip())
    
data['Installs']=install
data['Installs']=data['Installs'].astype(int)


# <b>d. Convert all other identified columns to numeric

# In[14]:


data['Reviews']=data['Reviews'].astype('int')


# <b>Q3. Sanity checks – check for the following and handle accordingly

# <b>a. Avg. rating should be between 1 and 5, as only these values are allowed on the play 
# store

# <b>i. Are there any such records? Drop if so.
# 
# 
# 

# In[15]:


data.loc[data.Rating < 1] & data.loc[data.Rating > 5]


# there are no such record having rating less than 1 or greater than 5.

# <b>b. Reviews should not be more than installs as only those who installed can review the 
# app.

# <b>i. Are there any such records? Drop if so

# In[16]:


data.loc[data['Reviews'] > data['Installs']]


# yes,there are 7 records where Review is greater than Installs.

# In[17]:


temp = data[data['Reviews']> data['Installs']].index
data.drop(labels = temp, inplace = True)


# In[18]:


data.loc[data['Reviews'] > data['Installs']]


# <b> Q4. Identify and handle outliers -

# <b>a. Price column

# <b>i. Make suitable plot to identify outliers in price

# In[19]:


plt.boxplot(data['Price'])
plt.show()


# <b>ii. Do you expect apps on the play store to cost $200? Check out these cases

# yes i expect apps on play store to cost $200.

# In[20]:


data.loc[data['Price'] > 200]


# <b>iii. After dropping the useless records, make the suitable plot again to identify 
# outlier

# In[21]:


plt.boxplot(data['Price'])
plt.show()


# <b>iv. Limit data to records with price < $30

# In[22]:


lt_30 = data[data['Price'] > 30].index
data.drop(labels = lt_30, inplace = True)


# In[23]:


count = data.loc[data['Price'] > 30].index
count.value_counts().sum()


# <b>b. Reviews column

# <b>i. Make suitable plot

# In[24]:


sns.distplot(data['Reviews'])
plt.show()


# <b>ii. Limit data to apps with < 1 Million reviews

# In[25]:


lt_1m = data[data['Reviews'] > 1000000 ].index
data.drop(labels = lt_1m, inplace=True)
print(lt_1m.value_counts().sum(),'cols dropped')


# <b>c. Installs

# <b>i. What is the 95th percentile of the installs?

# In[26]:


percentile = data.Installs.quantile(0.95)
print(percentile,"is 95th percentile of Installs")


# <b>ii. Drop records having a value more than the 95th percentile

# In[27]:


for i in range(0,101,1):
    print('the {} percentile of Installs is {}'.format(i,np.percentile(data['Installs'],i)))


# In[28]:


temp1 = data[data["Installs"] > percentile].index
data.drop(labels = temp1, inplace = True)
print(temp1.value_counts().sum())


# <B>Data analysis to answer business questions

# <b>Q5. What is the distribution of ratings like? (use Seaborn) More skewed towards higher/lower 
# values

# <b>a. How do you explain this?

# In[29]:


sns.distplot(data['Rating'])
plt.show()
print('The skewness of this distribution is', data['Rating'].skew())
print(' data that is skewed to the left hence more skew toward lower data values.')


# <b>b. What is the implication of this on your analysis?

# In[30]:


data['Rating'].mode(), data['Rating'].median(), data['Rating'].mean()


# mode >= meadian > mean, mean is less than median and distribution of Rating is negative skewed therefore distribution of rating is more skewed towards lower value.

# <b>6. What are the top Content Rating values?

# <b>a. Are there any values with very few records?

# In[31]:


data['Content Rating'].value_counts()


# Adults only 18+ and Unrated are values with very few records.

# <b>b. If yes, drop those as they won’t help in the analysis

# In[32]:


#replacing unwanted value with NaN
cr =[]
for k in data['Content Rating']:
    cr.append(k.replace('Adults only 18+', 'NaN').replace('Unrated', 'NaN'))
data['Content Rating']=cr


# In[33]:


# dropping the NaN Value
temp2 = data[data['Content Rating'] =='NaN'].index
data.drop(labels=temp2, inplace = True)
print('droped cols',temp2)


# In[34]:


data['Content Rating'].value_counts()


# <b>Q7. Effect of size on rating

# <b>a. Make a joinplot to understand the effect of size on rating

# In[35]:


sns.jointplot(y = 'Size', x = 'Rating', data=data, kind='hex')
plt.show()


# <b>b. Do you see any patterns?

# In[36]:


Yes, patterns can be observed between size and Rating that is their is correlation between Size and Rating


# <b>c. How do you explain the pattern?

# increasing Rating, size of app also increases. we can concluede that positive correlation between size and Rating.

# <b>Q8. Effect of price on rating

# <b> Make a joinplot(with regression line)

# In[37]:


sns.jointplot(x='Price', y='Rating', data= data, kind ='reg')
plt.show()


# <b>b. What pattern do you see?

# increasing the price. Rating remains constant greater than 4. thus it can be concluded that their is very weak Positive correlation between Rating and Price.

# <b>c. How do you explain the pattern?

# since on increasing the Price. Rating remains almost constant greater than 4. Thus it can be concluded that their is very weak positive correleation between Rating and Price.

# In[38]:


data.corr()


# <b>d. Replot the data, this time with only records with price > 0

# In[39]:


data1=data.loc[data.Price>0]
sns.jointplot(x='Price', y='Rating', data = data1, kind='reg')
plt.show()


# <b>e. Does the pattern change?

# yes, On increasing the record with Price > 0, the overall pattern changed a slight is their is very weekly Negative Correletion 
# between Price and Rating

# In[40]:


data1.corr()


# <b>f. What is your overall inference on the effect of price on the rating

# Generally increasing the Price, does not have significant effect on higher Rating for higher Price. Rating is high
# and almost constant is greater than 4

# <b>Q9. Look at all the numeric interactions together –

# <b>a. Make a pairplort with the colulmns - 'Reviews', 'Size', 'Rating', 'Price'

# In[41]:


sns.pairplot(data, vars=['Reviews', 'Size', 'Rating', 'Price'], kind = 'reg')
plt.show()


# <b>Q10. Rating vs. content rating

# <b>a. Make a bar plot displaying the rating for each content rating
# 

# In[42]:


data.groupby(['Content Rating'])['Rating'].count().plot.bar(color="blue")
plt.show()


# <b>b. Which metric would you use? Mean? Median? Some other quantile?

# In[43]:


plt.boxplot(data['Rating'])
plt.show()


# <b>c. Choose the right metric and plot

# In[44]:


data.groupby(['Content Rating'])['Rating'].median().plot.barh(color="blue")
plt.show()


# <b> Q11. Content rating vs. size vs. rating – 3 variables at a time

# <b>a. Create 5 buckets (20% records in each) based on Size

# In[45]:


bins = [0, 20000, 40000, 60000, 80000,100000]
data['Bucket Size'] = pd.cut(data['Size'], bins, labels = ['0-20k','20k-40k','40k-60k','60k-80k','80k-100k'])
pd.pivot_table(data, values='Rating', index= 'Bucket Size',columns ='Content Rating')


# <b>b. By Content Rating vs. Size buckets, get the rating (20th percentile) for each 
# combination

# In[47]:


temp3=pd.pivot_table(data, values ='Rating', index = 'Bucket Size', columns='Content Rating', aggfunc= lambda x:np.quantile(x,0.2))
temp3


# <b>c. Make a heatmap of this

# <b>i. Annotated

# In[52]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(temp3, annot= True, ax= ax)
plt.show()


# <b>ii. Greens color map

# In[54]:


f,ax = plt.subplots(figsize = (5,5))
sns.heatmap(temp3, annot= True, cmap='Greens', ax= ax)
plt.show()


# <b>d. What’s your inference? Are lighter apps preferred in all categories? Heavier? Some?

# In my inference, its not true that lighter app are preferred in all categories. Bcz app with size 40k-60k and 80k-100k have got highest rating in all categories. so we conclude that heavier apps are preferred in all categories.

# In[ ]:





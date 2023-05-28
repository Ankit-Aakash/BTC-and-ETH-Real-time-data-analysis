#!/usr/bin/env python
# coding: utf-8

# In[155]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#import datetime as dt
#from datetime import datetime, timedelta


# In[157]:


df = pd.read_csv("data.csv") #import data from csv file
# Convert the 'date' column to datetime type
df['Time'] = pd.to_datetime(df['Time'])


# In[184]:


# Get the current date
current_date = datetime.now().date()

# Calculate the date 30 days ago
start_date = current_date - timedelta(days=30)


# In[185]:


df['Date'] = df['Time'].apply(lambda x: x.date())


# In[183]:


df = df[df['Date']> start_date]
df.info()


# In[166]:


# Extract the data for the month of May
may_data = df[df['Time'].dt.month == 5]

# Extract the data for BTC
btc_data = may_data[may_data['Symbol'] == 'BTC']

# Extract the data for ETH
eth_data = may_data[may_data['Symbol'] == 'ETH']


# In[167]:


#For BTC
print('Mean BTC:',btc_data['Close'].mean())
print('Min BTC:',btc_data['Close'].min())
print('Max BTC:',btc_data['Close'].max())
print('Standard Dev BTC:',btc_data['Close'].std())


# In[168]:


#For ETH
print('Mean ETH:',eth_data['Close'].mean())
print('Min ETH:',eth_data['Close'].min())
print('Max ETH:',eth_data['Close'].max())
print('Standard Dev ETH:',eth_data['Close'].std())


# In[169]:


# Using describe function
print(eth_data.describe())


# In[170]:


# Using describe function
print(btc_data.describe())


# In[171]:


print(btc_data.corrwith(eth_data, method='spearman'))


# In[172]:


print('Using Box Plot for outlier detection')
print('The dots in the box plots correspond to extreme outlier values.') 

sns.boxplot(data=btc_data,x=btc_data["Close"])
plt.title("Boxplot of Closing Price of BTC")


# In[173]:


sns.boxplot(data=eth_data,x=eth_data["Close"])
plt.title("Boxplot of Closing Price of ETH")


# In[174]:


print('Using Line Graph for finding any trend in closing price of ')

#Graph size
plt.figure(figsize=(15, 8))

# Plotting the line graph
plt.plot(btc_data['Time'], btc_data['Close'],linewidth=2)

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Close')
plt.title('Price Trend')

# Displaying the graph
plt.show()


# In[175]:


#Using Line Graph for finding any trend in closing price

#Graph size
plt.figure(figsize=(15, 8))

# Plotting the line graph
plt.plot(eth_data['Time'], eth_data['Close'],linewidth=2)



# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Close')
plt.title('Price Trend')

# Displaying the graph
plt.show()


# In[176]:


#Using Line Graph for finding any trend in volume

#Graph size
plt.figure(figsize=(15, 8))

# Plotting the line graph
plt.plot(btc_data['Time'], btc_data['Volume'],linewidth=2)



# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Volume')
plt.title('Volume Trend')

# Displaying the graph
plt.show()


# In[149]:


#Using Line Graph for finding any trend in volume

#Graph size
plt.figure(figsize=(15, 8))

# Plotting the line graph
plt.plot(eth_data['Time'], eth_data['Volume'],linewidth=2)



# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Volume')
plt.title('Volume Trend')

# Displaying the graph
plt.show()


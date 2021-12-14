#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


# In[2]:


mouse_data = pd.read_csv('Mouse_metadata.csv')
mouse_data.head()


# In[3]:


study_results = pd.read_csv('Study_results.csv')
study_results.head()


# In[4]:


#combine the data
mouse_data_full = pd.merge(mouse_data,study_results,how="left",on='Mouse ID')
mouse_data_full.head()


# In[5]:


mouse_data_full["Mouse ID"].value_counts()


# In[6]:


duplicate_mouse_ids = mouse_data_full.loc[mouse_data_full.duplicated(subset=['Mouse ID', 'Timepoint']),'Mouse ID'].unique()


# In[7]:


print(duplicate_mouse_ids)


# In[8]:


duplicate_mouse = mouse_data_full.loc[mouse_data_full["Mouse ID"]=="g989",:]
duplicate_mouse.head(20)


# In[9]:


mouse_data_full = mouse_data_full.drop(mouse_data_full.index[908])


# In[10]:


mouse_data_full = mouse_data_full.rename(columns={"Tumor Volume (mm3)":"Tumor Volume",
                                         "Weight (g)":"Weight"})
mouse_data_full.head()


# In[11]:


mouse_data_full["Mouse ID"].value_counts()


# In[12]:


grouped_data = mouse_data_full.groupby(['Drug Regimen'])


# In[13]:


print(grouped_data)


# In[14]:


mean = grouped_data["Tumor Volume"].mean()


# In[15]:


median = grouped_data["Tumor Volume"].median()


# In[16]:


sem = grouped_data["Tumor Volume"].sem()


# In[17]:


std = grouped_data["Tumor Volume"].std()


# In[18]:


var = grouped_data["Tumor Volume"].var()


# In[19]:


regimen_summary = pd.DataFrame(grouped_data["Drug Regimen"].count())
regimen_summary["Median"] = median
regimen_summary["Mean"] = mean   
regimen_summary["SEM"] = sem
regimen_summary["Standard Deviation"] = std
regimen_summary["Variance"] = var
regimen_summary


# In[20]:


mouse_data_full.groupby(['Drug Regimen']).agg({'Tumor Volume':['mean','median','sem','std','var']})


# In[21]:


grouped_data = mouse_data_full.groupby(['Drug Regimen'])
print(grouped_data)


# In[22]:


time_points = grouped_data['Timepoint'].sum()


# In[23]:


time_point_chart = time_points.plot(kind="bar", title="Timepoints by Drug Regimen")
time_point_chart.set_ylabel("Timepoints")


# In[24]:


mice_grouped = mouse_data_full.groupby(['Sex'])
print(mice_grouped)


# In[25]:


mice_grouped["Mouse ID"].count()


# In[26]:


mouse_summary = pd.DataFrame(mice_grouped["Sex"].count())
mouse_summary


# In[27]:


mouse_pie = mouse_summary.plot(kind="pie",y='Sex',title=("Distribution of mice"))
plt.axis("equal")
                              


# In[28]:


max_timepoint = mouse_data_full.groupby(["Mouse ID"])['Timepoint'].max()
print(max_timepoint)


# In[29]:


mouse_data_timepoint = pd.merge(mouse_data_full,max_timepoint,on='Mouse ID')
mouse_data_timepoint.head()


# In[30]:


capomulin_regimen = mouse_data_timepoint.loc[mouse_data_timepoint["Drug Regimen"]=="Capomulin",:]
capomulin_regimen.head()


# In[31]:


total_volume = capomulin_regimen.groupby(["Mouse ID"])['Tumor Volume'].sum()
print(total_volume)


# In[32]:


ramicane_regimen = mouse_data_timepoint.loc[mouse_data_timepoint["Drug Regimen"]=="Ramicane",:]
ramicane_regimen.head()


# In[33]:


total_volume = ramicane_regimen.groupby(["Mouse ID"])['Tumor Volume'].sum()
print(total_volume)


# In[35]:


infubinol_regimen = mouse_data_timepoint.loc[mouse_data_timepoint["Drug Regimen"]=="Infubinol",:]
infubinol_regimen.head()


# In[36]:


total_volume = infubinol_regimen.groupby(["Mouse ID"])['Tumor Volume'].sum()
print(total_volume)


# In[37]:


ceftamin_regimen = mouse_data_timepoint.loc[mouse_data_timepoint["Drug Regimen"]=="Ceftamin",:]
ceftamin_regimen.head()


# In[38]:


total_volume = ceftamin_regimen.groupby(["Mouse ID"])['Tumor Volume'].sum()
print(total_volume)


# In[39]:


specific_regimen = mouse_data_full.loc[mouse_data_full["Drug Regimen"]=="Capomulin",:]
specific_regimen.head()


# In[44]:


specific_regimen.groupby(['Timepoint']).agg(total_volume=('Tumor Volume', 'median')).plot(figsize=(10, 5), title= "Tumor Volume")


# In[45]:


specific_regimen.plot(kind="scatter", x="Tumor Volume", y="Weight", grid=True, figsize=(8,8),
              title="Tumor Volume Vs. Weight")
plt.show()


# In[46]:


x_values = specific_regimen['Tumor Volume']
y_values = specific_regimen['Weight']
(slope, intercept, rvalue, pvalue, stderr) = stats.linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(0,20),fontsize=15,color="red")
plt.xlabel('Tumor Volume')
plt.ylabel('Weight')
print(f"The r-squared is: {rvalue**2}")
plt.show()


# In[ ]:





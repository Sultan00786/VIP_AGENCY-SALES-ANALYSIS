#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


from pathlib import Path


# In[3]:


def get_df_name(file_path):
    if str(file_path.suffix) == '.csv' :
        return str(file_path.stem)
    else :
        file_name = str(file_path.stem).replace(' ','_').split('_')
        name_start_index = 2
        name_end_index = len(file_name)-1
        df_name = '_'.join(file_name[name_start_index:name_end_index]).lower()
        return df_name
        


# In[4]:


def getFilesInfo(dir_path):
    files = []
    dir_path = Path(dir_path)
    for file_path in dir_path.iterdir():
        files.append({
            "file_path":str(file_path),
            "file_extension": str(file_path.suffix),
            "df_name": get_df_name(file_path)
        })
    return files


# In[5]:


# temp = pd.read_excel(r"assets\\LeverEDGE_10C077_Pending Bill_2026091701435443544354.xlsx")
# temp.head(15)
import warnings
from types import SimpleNamespace

def load_files(file_info):
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

    dfs = {}
    for item in file_info:
        name = item['df_name']
        path = item['file_path']
        if(item['file_extension'] == '.csv'):
            dfs[name] = pd.read_csv(path)
        else:
            dfs[name] = pd.read_excel(path)
    dfs = SimpleNamespace(**dfs)
    return dfs


# In[6]:


def clean_heading_titles(dfs):
    for name, df in dfs.__dict__.items():
        dfs.__dict__[name] = df[~(pd.isna(df.iloc[:,0]))]


# In[7]:


from IPython.display import display, HTML

display(HTML("""
<style>
.dataframe-container {
    overflow-x: auto !important;
}
</style>
"""))


# In[8]:


def fixs_cols_name(dfs):
    for name, df in dfs.__dict__.items():
        col_names = list(df.iloc[0,:])
        dfs.__dict__[name] = df.iloc[1:,:]
        dfs.__dict__[name].columns = col_names


# In[23]:


def save_dfs_files(dfs):
    for name, df in dfs.__dict__.items():
        df.to_csv(f'output\\{name}.csv', index=False)







# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

def initialise_df(schools):
    """
    this function takes our dataframes as arguments and applies a variety of columns to a new dataframe    
    """

    df = pd.DataFrame()
    df['id'] = schools['ACARA School ID']
    df['state'] = schools['State']
    #df['postcode'] = schools['Postcode']
    df['sector'] = schools['School Sector']
    df['grades'] = schools['School Type']
    df['geolocation'] = schools['Geolocation']
    df['icsea'] = schools['ICSEA']
    df['staff'] = schools['Full Time Equivalent Teaching Staff']
    df['numStudents'] = schools['Total Enrolments']
    df['staff_per_student'] = df['staff']/df['numStudents']
    df['indigenous_percent'] = schools['Indigenous Enrolments']
    df['non_english_home_percent'] = schools['Language Background Other Than English']
    #df['girls_percent'] = schools['Girls Enrolments']/schools['Total Enrolments']*100
    df['boys_percent']= schools['Boys Enrolments']/schools['Total Enrolments']*100
    df.set_index("id", inplace=True)

    return df


def get_funding(df, funding2016):
#funding2016.head()
    funding2016.set_index('ACARA School ID', inplace=True)
    df['Aus_funding'] = funding2016['Income: Australian Government Recurrent Funding']
    df['state_funding'] = funding2016['Income: State/Territory Government Recurrent Funding']
    df['parent_funding'] = funding2016['Income: Fees, Charges and Parental Contributions']
    df['other_funding'] = funding2016['Income: Other Private Sources']
    df['gross_funding'] = funding2016['Total Gross Income']
    df['gross_per_student'] = funding2016['Total Gross Income Per Student']
    df['net_per_student'] = funding2016['Total Net Recurrent Income Per Student']
    
    return df

def get_results(df, naplan2017):
    """
    this function retreives the year9 numeracy results for each school & removes 
    those schools who don't have year9
    """

    #drop rows that don't have year9 numeracy
    naplan2017 = naplan2017[naplan2017['Domain'] == 'Numeracy']
    naplan2017 = naplan2017[naplan2017['Student Grade Level'] == 'Year 9']
    naplan2017.set_index('ACARA School ID', inplace=True)

    #join df with the average Yr9 numeracy scores
    df = pd.concat([df, naplan2017['Average NAPLAN Score']], axis=1)
    
    #shorten name on naplan results
    df=df.rename(columns = {'Average NAPLAN Score':'naplan'})

    #drop schools without Yr9 i.e. where results are NaN
    df=df.dropna()

    return df


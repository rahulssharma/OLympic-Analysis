import preprocess
import numpy as np
# df1=preprocess.preprocessor(df,region_df)
def medal_tally(df):
    medal_Tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_Tally = medal_Tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()

    medal_Tally['Total'] = medal_Tally['Gold'] + medal_Tally['Silver'] + medal_Tally['Bronze']

    medal_Tally['Gold']=medal_Tally['Gold'].astype('int')
    medal_Tally['Silver']=medal_Tally['Silver'].astype('int')
    medal_Tally['Bronze']=medal_Tally['Bronze'].astype('int')
    medal_Tally['Total']=medal_Tally['Total'].astype('int')
    return medal_Tally
def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x = x.rename(columns={'index': 'Name', 'Name_x': 'Medal'})
    return x
def country_year_list(df1):
    Years = df1['Year'].unique().tolist()
    Years.sort()
    Years.insert(0,'Overall')
    Country=np.unique(df1['region']. dropna().values).tolist()
    Country.sort()
    Country.insert(0,'Overall')
    return Years,Country

def fetch_medal_tally(df1,year,country):
    medal_df=df1.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x

def data_over_time(df,col):
    nations_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_overtime.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_overtime


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = (new_df.pivot_table(index="Sport", columns='Year', values='Medal', aggfunc="count").fillna(0))
    return pt

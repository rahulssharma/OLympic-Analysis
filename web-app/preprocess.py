import pandas as pd



def preprocessor(df,region_df):
    # global df,region_df
    df=df[df['Season']=='Summer']
    df=df.merge(region_df,on="NOC",how="left")
    df.drop_duplicates(inplace=True)
    df1 = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df1
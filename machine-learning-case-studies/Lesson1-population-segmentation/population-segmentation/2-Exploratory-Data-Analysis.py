""""
clean it up, 
explore it, 
and pre-process it
""""


# print out stats about data [x, y]
print(counties_df.shape)

#print total size of array x * y
print(counties_df.size)

#print # of dimansions on the data
print(counties_df.ndim)

#print features names
print(counties_df.columns)

# drop any incomplete rows of data, and create a new df
clean_counties_df = None
features = counties_df.columns

#print total size of array x * y
print(counties_df.shape)

#remove all rows contain missing values
clean_counties_df = counties_df.dropna()

#print total size of array x * y
print(clean_counties_df.shape)

# Add new column State-County
clean_counties_df['State-County'] = clean_counties_df[['State', 'County']].apply(lambda x: '-'.join(x), axis=1)

# index data by 'State-County'
clean_counties_df.set_index(clean_counties_df['State-County'])

# drop the old State and County columns, and the CensusId column
# clean df should be modified or created anew
clean_counties_df = clean_counties_df.drop(["State", "County", "CensusId", "State-County"], axis=1)

# features
features_list = clean_counties_df.columns.values
print('Features: \n', features_list)


counties_scaled = None

# read values
x = clean_counties_df.values #returns a numpy array

#use min max normalization
min_max_scaler = preprocessing.MinMaxScaler()

#apply normalization on the data
x_scaled = min_max_scaler.fit_transform(x)

#convert data to dataframe
counties_scaled = pd.DataFrame(x_scaled)

#rename features
new = pd.DataFrame(data=counties_scaled, columns=clean_counties_df.columns)

#insert data to the data
counties_scaled = pd.DataFrame(data=counties_scaled.values, columns=clean_counties_df.columns)
# create a list of features that you want to compare or examine
my_list = features_list
n_bins = 40 # define n_bins

# histogram creation code is similar to above
# we will found that the values is in different ranges so we need
# to normalize it
for column_name in my_list:
    ax=plt.subplots(figsize=(6,3))
    # get data by column_name and display a histogram
    ax = plt.hist(clean_counties_df[column_name], bins=n_bins, range=[clean_counties_df[column_name].min(), clean_counties_df[column_name].max()])
    title="Histogram of " + column_name
    plt.title(title, fontsize=12)
    plt.show()
    

    
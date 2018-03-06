import pandas, folium, json

data = pandas.read_read_csv('mammoth_data.cvs') # dataframe from cvsfile

# Need to aggregate all fossils for one State. Some records have more than one
# mammoth discovered. The abd column has the number of fossils found at the Site

# Create a quantity column with a copy of the abd column
quantities = data['abd']
# If there is no data, assume that the record is for one mammoth
quantities = quantities.fillna(value = 1)

# Add the new column to the dataframe
data['quantity'] = quantities

# Group by state, and sum the columns. We only need the sum of the quantity column.
# groupby returns a Groupby object. reset_index() returns that object into a dataframe
state_data_groups = data.groupby(by=['state']).sum().reset_index()

# Add missing states to dataframe. About 15 states have no mammoths.
# Choropeth will error if states are missing (Extra regions, countries, or states will be ignored)
# Need to add a row with a zero value for missing states.
state_abbr = json.load(open('us_states_abbr.json'))
state_list = list(states_abbr.key())

# Create a data frame from state names, with zero for each quantity
all_states_zeros = pandas.dataframe({ 'state' : state_list, 'quantity' : 0})

# append the zero dataframe to the end of state_data_groups
all_state_data = state_data_groups.append(all_states_zeros)

# Drop second of duplicate value for the 'state' series,
# which will remove the zero version for states that were already in the dataframe
all_state_data = all_state_data.drop_duplicates('state', Keep='first')

# Neat! Repace with dictionary of { orig: replace } ; which are in the form { 'Minnesota' : 'MN'}
state_data_groups = all_state_data.replace(states_abbr)

print (state_data_groups)

# And create the Choropleth map
us_states_filen= r'us_states.json' # Path to geo-jason file

choromap = folium.Map(location=[40, -120], zoom_start=3)

choromap.Choropleth(
    geo_path=us_states_file,  # Reads theis file
    data =state_data_groups,
    columns = ['state', 'quantity'],
    key_on = 'id',
    fill_color = 'BuPu', fill_capacity = 0.6, line_opacity = 0.4,
    threshold_scale = [0, 5, 10, 15, 20, 90],
    legend_name = "mammoth finds per state"
)

choromap.save('mammoth_choropleth.html')

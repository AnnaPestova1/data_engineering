import pandas as pd

'''Data cleaning'''

# export data from csv files
df_world_series_results = pd.read_csv('../dirty_data/world_series_results.csv', skipinitialspace=True)

df_world_series_pitchers_results = pd.read_csv('../dirty_data/world_series_pitchers_results.csv', skipinitialspace=True)

df_world_series_pitchers_biography = pd.read_csv('../dirty_data/world_series_pitchers_biography.csv', skipinitialspace=True)

# creating copies
clean_df_world_series_results = df_world_series_results.copy()
clean_df_world_series_pitchers_results = df_world_series_pitchers_results.copy()
clean_df_world_series_pitchers_biography = df_world_series_pitchers_biography.copy()

# drop rows with missing data and drop duplicates
clean_df_world_series_results = clean_df_world_series_results.dropna(ignore_index=True)
clean_df_world_series_results['World Series'] = clean_df_world_series_results['World Series'].str.replace(r'\D', '', regex=True).astype(int)

clean_df_world_series_results.rename(columns={'World Series': 'year'}, inplace=True, errors='raise')

clean_df_world_series_pitchers_results = clean_df_world_series_pitchers_results.dropna().reset_index()
clean_df_world_series_pitchers_results['World Series'] = clean_df_world_series_pitchers_results['World Series'].str.replace(r'\D', '', regex=True).astype(int)

clean_df_world_series_pitchers_results.rename(columns={'World Series': 'year'}, inplace=True, errors='raise')



# remove columns when no games yet
no_series_yet_index = clean_df_world_series_results[ clean_df_world_series_results['National League'] == 'To Be Determined' ].index
clean_df_world_series_results.drop(no_series_yet_index , inplace=True)
clean_df_world_series_results['NL Wins'] = clean_df_world_series_results['NL Wins'].astype(int)
clean_df_world_series_results['AL Wins'] = clean_df_world_series_results['AL Wins'].astype(int)

no_games_yet = clean_df_world_series_pitchers_results[ clean_df_world_series_pitchers_results['Team 1 wins'] == '-' ].index
clean_df_world_series_pitchers_results.drop(no_games_yet , inplace=True)

clean_df_world_series_pitchers_results['Team 1 wins'] = clean_df_world_series_pitchers_results['Team 1 wins'].astype(int)
clean_df_world_series_pitchers_results['Team 2 wins'] = clean_df_world_series_pitchers_results['Team 2 wins'].astype(int)

clean_df_world_series_pitchers_results= clean_df_world_series_pitchers_results.replace(to_replace=r'^\W+', value='', regex=True).replace(to_replace=r'\W+$', value='', regex=True).replace(to_replace=r'\'', value='', regex=True).replace(to_replace=r'[\[\]]', value='', regex=True)

for col in ['Team 1 Pitchers', 'Team 2 Pitchers', 'Team 1 Pitchers Links', 'Team 2 Pitchers Links']:
    clean_df_world_series_pitchers_results[col] = clean_df_world_series_pitchers_results[col].map(lambda x: x.split('\\n') if '\\n' in x else x.split(', '))
    if col == 'Team 1 Pitchers' or col == 'Team 2 Pitchers':
        clean_df_world_series_pitchers_results[col] = clean_df_world_series_pitchers_results[col].map(lambda x: [s.lower().title() for s in x] )

clean_df_world_series_pitchers_results[['Team 1', 'Team 2']] = clean_df_world_series_pitchers_results[['Team 1', 'Team 2']].replace(to_replace=r' \d+ [a-zA-Z ]+', value='', regex=True)

# print(len(clean_df_world_series_results), len(clean_df_world_series_pitchers_results)) result is 120
def clean_teams_name():
    for i in range(len(clean_df_world_series_results)):
        if clean_df_world_series_results['year'][i] == clean_df_world_series_pitchers_results['year'][i]:
            if 'Pitching Statistics' in clean_df_world_series_pitchers_results['Team 1'][i]:
                clean_df_world_series_pitchers_results.loc[i, 'Team 1'] = clean_df_world_series_results['American League'][i] if clean_df_world_series_pitchers_results['Team 1 wins'][i] == clean_df_world_series_results['AL Wins'][i] else clean_df_world_series_results['National League'][i]
            if 'Pitching Statistics' in clean_df_world_series_pitchers_results['Team 2'][i]:
                clean_df_world_series_pitchers_results.loc[i, 'Team 2'] = clean_df_world_series_results['National League'][i] if clean_df_world_series_pitchers_results['Team 2 wins'][i] == clean_df_world_series_results['NL Wins'][i] else clean_df_world_series_results['American League'][i]

clean_teams_name()

# manual resolution columns for pitcher name and their links
def auto_manual_resolution(x, col1, col2):
    result = []
    if len(x[col1]) == len(x[col2]):
        for i in range(len(x[col1])):
            result.append({'pitcher_name': x[col1][i], 'link': x[col2][i]})
    else:
        print(f"row for {x['year']} in columns {col1, col2} requires manual resolution")
    return result

    

clean_df_world_series_pitchers_results['t1 players and links'] = clean_df_world_series_pitchers_results.apply(lambda x: auto_manual_resolution(x, 'Team 1 Pitchers', 'Team 1 Pitchers Links'), axis=1)
clean_df_world_series_pitchers_results['t2 players and links'] = clean_df_world_series_pitchers_results.apply(lambda x: auto_manual_resolution(x, 'Team 2 Pitchers', 'Team 2 Pitchers Links'), axis=1)

'''
i have the follow message
row for 1969 in columns ('Team 2 Pitchers', 'Team 2 Pitchers Links') requires manual resolution
so I will resolve the issue manually
'''
index_for_manual_resolution = clean_df_world_series_pitchers_results[clean_df_world_series_pitchers_results['year'] == 1969].index
# print(index_for_manual_resolution)

# remove truncation in terminal
pd.set_option('display.max_colwidth', None)
# uncomment to see the data
# print(clean_df_world_series_pitchers_results.loc[index_for_manual_resolution, 'Team 2 Pitchers'])
# print(clean_df_world_series_pitchers_results.loc[index_for_manual_resolution, 'Team 2 Pitchers Links'])
'''
data I received.

[Mike Cuellar, Dick Hall, Dave Leonhard, Dave Mcnally, Jim Palmer, Pete Richert, Eddie Watt]
Name: Team 2 Pitchers, dtype: object
[https://www.baseball-almanac.com/players/player.php?p=cuellmi01, https://www.baseball-almanac.com/players/player.php?p=halldi01, https://www.baseball-almanac.com/players/player.php?p=leonhda01, https://www.baseball-almanac.com/players/player.php?p=leonhda01, https://www.baseball-almanac.com/players/player.php?p=mcnalda01, https://www.baseball-almanac.com/players/player.php?p=palmeji01, https://www.baseball-almanac.com/players/player.php?p=palmeji01, https://www.baseball-almanac.com/players/player.php?p=richepe01, https://www.baseball-almanac.com/players/player.php?p=watted01]
Name: Team 2 Pitchers Links, dtype: object

2 links: https://www.baseball-almanac.com/players/player.php?p=palmeji01 and https://www.baseball-almanac.com/players/player.php?p=leonhda01 are duplicated
I will remove extra link manually and than run the code again
'''

clean_df_world_series_pitchers_results.at[index_for_manual_resolution[0], 'Team 2 Pitchers Links'] =  ['https://www.baseball-almanac.com/players/player.php?p=cuellmi01', 'https://www.baseball-almanac.com/players/player.php?p=halldi01', 'https://www.baseball-almanac.com/players/player.php?p=leonhda01', 'https://www.baseball-almanac.com/players/player.php?p=mcnalda01', 'https://www.baseball-almanac.com/players/player.php?p=palmeji01', 'https://www.baseball-almanac.com/players/player.php?p=richepe01', 'https://www.baseball-almanac.com/players/player.php?p=watted01']
clean_df_world_series_pitchers_results.at[index_for_manual_resolution[0], 't2 players and links'] = auto_manual_resolution(clean_df_world_series_pitchers_results.loc[index_for_manual_resolution[0]], 'Team 2 Pitchers', 'Team 2 Pitchers Links')

print('Issue resolved on lines 77-103')
# return truncation
pd.reset_option('display.max_colwidth')


# clean pitchers data
us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "D.C."
]

# if we run next line of code we will se that no null data, we just need clean data
# print('\nis null in data\n', clean_df_world_series_pitchers_biography.isnull().any())

clean_df_world_series_pitchers_biography['Born-on'] = clean_df_world_series_pitchers_biography['Born-on'].replace(to_replace=r'[^\d\-\/]', value='', regex=True)
clean_df_world_series_pitchers_biography['Born-on'] = pd.to_datetime(clean_df_world_series_pitchers_biography['Born-on'], format='%m-%d-%Y', errors='coerce')

clean_df_world_series_pitchers_biography['Full name'] = clean_df_world_series_pitchers_biography['Full name'].map(lambda x: x.lower().title() )

clean_df_world_series_pitchers_biography['Born in'] = clean_df_world_series_pitchers_biography['Born in'].apply(lambda x: x.split(', ')[-1]).apply(lambda x: 'USA' if x in us_states else x).apply(lambda x: 'Germany' if x == 'West Germany' else x)

clean_df_world_series_pitchers_biography['was_in_college'] = clean_df_world_series_pitchers_biography.apply(lambda x: False if x['College'] == 'None Attended' else True, axis = 1 )

clean_df_world_series_results.rename(columns={'National League': 'nl', 'American League' : 'al', 'Links': 'games_links', 'AL Wins': 'al score', 'NL Wins': 'nl score' }, inplace=True, errors='raise')
clean_df_world_series_pitchers_results.rename(columns={'Team 1' : 't1', 'Team 2': 't2', 'Team 1 Pitchers': 't1 pitchers', 'Team 2 Pitchers': 't2 pitchers', 'Team 1 Pitchers Links': 't1 pitchers links', 'Team 2 Pitchers Links': 't2 pitchers links', 'Team 1 wins': 't1 score', 'Team 2 wins': 't2 score', 'Links': 'links'}, inplace=True, errors='raise')
clean_df_world_series_pitchers_biography.rename(columns={'Full name': 'name', 'Born in' : 'birthplace', 'Links': 'link', 'Born-on': 'birthdate', 'College': 'college' }, inplace=True, errors='raise')



# create new data for dashboard about world series games

world_series_data = pd.merge(clean_df_world_series_results, clean_df_world_series_pitchers_results, on='year', how='inner')

world_series_data['al pitchers'] = world_series_data.apply(lambda x: x['t1 pitchers'] if x['al'] == x['t1'] and x['al score'] == x['t1 score'] else x['t2 pitchers'], axis=1)
world_series_data['nl pitchers'] = world_series_data.apply(lambda x: x['t1 pitchers'] if x['nl'] == x['t1'] and x['nl score'] == x['t1 score'] else x['t2 pitchers'], axis=1)
world_series_data['al pitchers links'] = world_series_data.apply(lambda x: x['t1 pitchers links'] if x['al'] == x['t1'] and x['al score'] == x['t1 score'] else x['t2 pitchers links'], axis=1)
world_series_data['nl pitchers links'] = world_series_data.apply(lambda x: x['t1 pitchers links'] if x['nl'] == x['t1'] and x['nl score'] == x['t1 score'] else x['t2 pitchers links'], axis=1)
world_series_data['al pitchers and links'] = world_series_data.apply(lambda x: x['t1 players and links'] if x['al'] == x['t1'] and x['al score'] == x['t1 score'] else x['t2 players and links'], axis=1)
world_series_data['nl pitchers and links'] = world_series_data.apply(lambda x: x['t1 players and links'] if x['nl'] == x['t1'] and x['nl score'] == x['t1 score'] else x['t2 players and links'], axis=1)

world_series_data.drop(['t1', 't2', 't1 score', 't2 score', 't1 pitchers', 't2 pitchers', 't1 pitchers links', 't2 pitchers links', 'links', 'index', 't1 players and links', 't2 players and links'], axis=1, inplace=True) 


world_series_data_nl = world_series_data[['year','nl', 'nl score', 'nl pitchers and links' ]]
world_series_data_al = world_series_data[['year','al', 'al score', 'al pitchers and links' ]]

# create separate dataFrames with data by league and players
world_series_data_nl = world_series_data_nl.explode("nl pitchers and links", ignore_index=True)
world_series_data_nl['name'] = world_series_data_nl['nl pitchers and links'].apply(lambda x: x['pitcher_name'])
world_series_data_nl['link'] = world_series_data_nl['nl pitchers and links'].apply(lambda x: x['link'])

world_series_data_al = world_series_data_al.explode("al pitchers and links", ignore_index=True)
world_series_data_al['name'] = world_series_data_al['al pitchers and links'].apply(lambda x: x['pitcher_name'])
world_series_data_al['link'] = world_series_data_al['al pitchers and links'].apply(lambda x: x['link'])
world_series_data_nl.drop('nl pitchers and links', axis=1, inplace=True) 
world_series_data_al.drop('al pitchers and links', axis=1, inplace=True) 
nl = pd.merge(world_series_data_nl, clean_df_world_series_pitchers_biography, how="left", on=["link"])
al = pd.merge(world_series_data_al, clean_df_world_series_pitchers_biography, how="left", on=["link"])


try:
    ws_results = pd.DataFrame(world_series_data)
    nl_results = pd.DataFrame(nl)
    al_results = pd.DataFrame(al)
    ws_pitchers_biography = pd.DataFrame(clean_df_world_series_pitchers_biography)
    
    ws_results.to_csv('../cleaned dataframes/world_series_data.csv', index=False)
    print('clean_df_world_series_results.csv created')
    nl_results.to_csv('../cleaned dataframes/nl_results.csv', index=False)
    print('nl_results.csv created')
    al_results.to_csv('../cleaned dataframes/al_results.csv', index=False)
    print('al_results.csv created')
    ws_pitchers_biography.to_csv('../cleaned dataframes/clean_df_world_series_pitchers_biography.csv', index=False)
    print('clean_df_world_series_pitchers_biography.csv created')

except Exception as err:
    print(f"Error during creating world_series_results.csv file occur {err}")
pd.set_option('display.max_colwidth', None)

# print(nl.info())
# print(al.info())
# manually check data 
# unique_al = world_series_data_al['al'].unique()
# unique_nl = world_series_data_nl['nl'].unique()
# print(unique_al)
# print(unique_nl)

# ['Boston Americans' 'Philadelphia Athletics' 'Chicago White Sox'
#  'Detroit Tigers' 'Boston Red Sox' 'Cleveland Indians' 'New York Yankees'
#  'Washington Senators' 'St. Louis Browns' 'Minnesota Twins'
#  'Baltimore Orioles' 'Oakland Athletics' 'Kansas City Royals'
#  'Milwaukee Brewers' 'Toronto Blue Jays' 'Anaheim Angels' 'Tampa Bay Rays'
#  'Texas Rangers' 'Houston Astros']
# ['Pittsburgh Pirates' 'New York Giants' 'Chicago Cubs' 'Boston Braves'
#  'Philadelphia Phillies' 'Brooklyn Robins' 'Cincinnati Reds'
#  'St. Louis Cardinals' 'Brooklyn Dodgers' 'Milwaukee Braves'
#  'Los Angeles Dodgers' 'San Francisco Giants' 'New York Mets'
#  'San Diego Padres' 'Atlanta Braves' 'Florida Marlins'
#  'Arizona Diamondbacks' 'Houston Astros' 'Colorado Rockies'
#  'Washington Nationals']
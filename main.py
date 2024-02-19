
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from nba_api.stats.endpoints import leagueleaders
import pandas as pd
import matplotlib.pyplot as plt

player_dict = players.get_players()

# Use ternary operator or write function 
# Names are case sensitive
bron = [player for player in player_dict if player['full_name'] == 'LeBron James'][0]
bron_id = bron['id']

# find team Ids
from nba_api.stats.static import teams 
teams = teams.get_teams()
GSW = [x for x in teams if x['full_name'] == 'Golden State Warriors'][0]
GSW_id = GSW['id']

try:
    # Pull data for the top 500 scorers
    top_500 = leagueleaders.LeagueLeaders(
        season='2023-24',
        season_type_all_star='Regular Season',
        stat_category_abbreviation='PTS'
    ).get_data_frames()[0][:500]

    # Correct column names for grouping
    avg_stats_columns = ['MIN', 'FGM', 'FGA', 'FTM', 'FTA', 'PTS', 'FG3M', 'FG3A']
    top_500_avg = top_500.groupby(['PLAYER', 'PLAYER_ID'])[avg_stats_columns].mean()

    # Inspect the first few rows of the averaged stats
    print(top_500_avg.head())

except Exception as e:
    print(f"An error occurred: {e}")


df_for_plotting = top_500_avg.reset_index()

'''
# Create a scatter plot with colors based on 'PTS'
fig = plt.scatter(
    df_for_plotting, 
    x='PTS', 
    y='FG3M', 
    hover_name='PLAYER', 
    color='PTS',  # This line makes the color of the points depend on the 'PTS' values
    #color_continuous_scale=plt.colors.sequential.Viridis  # Optional: choose a color scale
)
fig.show()
'''
print(top_500_avg)

top_10 = top_500_avg.sort_values(by='PTS', ascending=False).head(10)
print(top_10)

plt.scatter(top_500_avg['PTS'], top_500_avg['FG3M'], c=top_500_avg['PTS'], cmap='viridis')
plt.xlabel('Points')
plt.ylabel('Three Pointers Made per Game')  

for index, row in top_500_avg.iterrows():
    if row['PTS'] > 1300:
        plt.annotate(index[0], (row['PTS'], row['FG3M']))

plt.show()
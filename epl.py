import pandas as pd
import streamlit as st
import time

# Read data for the 2021-2022 season
df = pd.read_csv('eplmatches.csv')
season_df = df[df['Season_End_Year'] == 2022]

# Get list of teams
teams = season_df['Home'].unique()
teams.sort()

# Create initial standings table
standings = pd.DataFrame({
    'Team': teams,
    'MP': 0,
    'W': 0,
    'D': 0,
    'L': 0,
    'GF': 0,
    'GA': 0,
    'GD': 0,
    'Pts': 0
})

standings = standings.set_index('Team')

# Create Streamlit app
st.title('Premier League Standings')
st.subheader('2021-2022 Season')

# creating a single-element container
placeholder = st.empty()

with placeholder.container():
    # Display initial standings table
    st.dataframe(standings)

# Visualization parameters
start_date = season_df['Date'].min()
end_date = season_df['Date'].max()


# Visualization loop
for date in pd.date_range(start=start_date, end=end_date):
    with placeholder.container():
        # convert to string with format "YYYY-MM-DD"
        date_str = date.strftime('%Y-%m-%d')

        # Get matches for current date
        matches = season_df[season_df['Date'] == date_str]

        # Update standings table
        for index, match in matches.iterrows():
            home_team = match['Home']
            away_team = match['Away']
            home_goals = match['HomeGoals']
            away_goals = match['AwayGoals']

            # Update home team stats
            standings.loc[home_team, 'MP'] += 1
            standings.loc[home_team, 'GF'] += home_goals
            standings.loc[home_team, 'GA'] += away_goals
            standings.loc[home_team, 'GD'] = standings.loc[home_team, 'GF'] - standings.loc[home_team, 'GA']
            if home_goals > away_goals:
                standings.loc[home_team, 'W'] += 1
                standings.loc[home_team, 'Pts'] += 3
            elif home_goals == away_goals:
                standings.loc[home_team, 'D'] += 1
                standings.loc[home_team, 'Pts'] += 1
            else:
                standings.loc[home_team, 'L'] += 1

            # Update away team stats
            standings.loc[away_team, 'MP'] += 1
            standings.loc[away_team, 'GF'] += away_goals
            standings.loc[away_team, 'GA'] += home_goals
            standings.loc[away_team, 'GD'] = standings.loc[away_team, 'GF'] - standings.loc[away_team, 'GA']
            if away_goals > home_goals:
                standings.loc[away_team, 'W'] += 1
                standings.loc[away_team, 'Pts'] += 3
            elif away_goals == home_goals:
                standings.loc[away_team, 'D'] += 1
                standings.loc[away_team, 'Pts'] += 1
            else:
                standings.loc[away_team, 'L'] += 1

        # Sort standings table and display
        standings = standings.sort_values(by=['Pts', 'GD', 'GF'], ascending=[False, False, False])

        # Add 'Pos' column
        standings = standings.reset_index()
        standings.index += 1
        
        st.write('##', date.strftime('%A, %B %d, %Y'))
        st.dataframe(standings)
        standings = standings.set_index('Team')
        time.sleep(1)


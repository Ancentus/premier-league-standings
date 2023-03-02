import pandas as pd
import streamlit as st
import time
import plotly.express as px

# Read data for the all seasons
df = pd.read_csv('eplmatches.csv')

# Get list of seasons
seasons = df['Season_End_Year'].unique()
seasons.sort()

# Let the user select the season
selected_season = st.sidebar.selectbox('Select season end year', seasons)

# Filter the data for the selected season
season_df = df[df['Season_End_Year'] == selected_season]

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
        
        # Display date and standings table in columns
        col1, col2 = st.columns([1, 6])

        # Display date in first column
        col1.write(date.strftime('%A, %B %d, %Y'))

        # Display standings table in second column
        ht = (20 + 1) * 35 + 3

        # sort by index for correct displaying in bar chart
        standings = standings.sort_index(ascending=True)

        # define team colors
        teams_colors = {
            "Arsenal": "#EF0107",
            "Aston Villa": "#95BFE5",
            "Brentford": "#FEE12B",
            "Brighton": "#0057B8",
            "Burnley": "#6C1D45",
            "Chelsea": "#034694",
            "Crystal Palace": "#1B458F",
            "Everton": "#003399",
            "Leeds United": "#FFCD00",
            "Leicester City": "#0053A0",
            "Liverpool": "#C8102E",
            "Manchester City": "#6CABDD",
            "Manchester Utd": "#DA291C",
            "Newcastle Utd": "#241F20",
            "Norwich City": "#00A14E",
            "Southampton": "#D71920",
            "Tottenham": "#132257",
            "Watford": "#FBEE23",
            "West Ham United": "#7A263A",
            "Wolves": "#FDB913",
            "Wolvess": "#FDB913"
        }


        # Create bar chart
        fig = px.bar(standings, x='Pts', y='Team', orientation='h', height=ht, range_x=[0,100], color='Team', color_discrete_map=teams_colors)

        # Set chart title and axis labels
        fig.update_layout(title=date.strftime('%A, %B %d, %Y'), xaxis_title="Points", yaxis_title="Team")

        # Display chart in second column
        col2.plotly_chart(fig)
        standings = standings.set_index('Team')
        time.sleep(1)


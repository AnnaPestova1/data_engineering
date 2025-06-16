import sqlite3
import pandas as pd


try:
    # read csv files
    world_series_data = pd.read_csv('../cleaned dataframes/world_series_data.csv', skipinitialspace=True)
    nl_results = pd.read_csv('../cleaned dataframes/nl_results.csv', skipinitialspace=True)
    al_results = pd.read_csv('../cleaned dataframes/al_results.csv', skipinitialspace=True)
    ws_pitchers_biography = pd.read_csv('../cleaned dataframes/clean_df_world_series_pitchers_biography.csv', skipinitialspace=True)
    unique_teams_name = pd.read_csv('../cleaned dataframes/unique_teams_name.csv', skipinitialspace=True)

    # Connect to a new SQLite database
    with  sqlite3.connect("../db/world_series.db") as conn:  
        conn.execute("PRAGMA foreign_keys = 1") 
        cursor = conn.cursor()
        # Create tables
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS WorldSeriesResults (
            year YEAR  NOT NULL UNIQUE PRIMARY KEY,
            nl_team TEXT NOT NULL,
            nl_score INTEGER NOT NULL,
            al_team TEXT NOT NULL,
            al_score INTEGER NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PitchersData (
            link TEXT NOT NULL UNIQUE PRIMARY KEY,
            pitcher_name TEXT NOT NULL,
            birthplace TEXT NOT NULL,
            birthdate DATE NOT NULL,
            college TEXT,
            was_in_college BOOL NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teams (
            team_name TEXT NOT NULL UNIQUE PRIMARY KEY
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS League (
            league_name TEXT NOT NULL UNIQUE PRIMARY KEY
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS NationalLeagueData (
            year YEAR  NOT NULL,
            team_name TEXT NOT NULL,
            team_score INTEGER NOT NULL,
            league_name TEXT NOT NULL,
            pitcher_name TEXT NOT NULL,
            link TEXT NOT NULL,
            FOREIGN KEY (year) REFERENCES WorldSeriesResults (year),
            FOREIGN KEY (team_name) REFERENCES Teams (team_name),
            FOREIGN KEY (league_name) REFERENCES League (league_name),
            FOREIGN KEY (link) REFERENCES PitchersData (link)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS AmericanLeagueData (
            year YEAR  NOT NULL,
            team_name TEXT NOT NULL,
            team_score INTEGER NOT NULL,
            league_name TEXT NOT NULL,
            pitcher_name TEXT NOT NULL,
            link TEXT NOT NULL,
            FOREIGN KEY (year) REFERENCES WorldSeriesResults (year),
            FOREIGN KEY (team_name) REFERENCES Teams (team_name),
            FOREIGN KEY (league_name) REFERENCES League (league_name),
            FOREIGN KEY (link) REFERENCES PitchersData (link)
        )
        """)

        print("Tables created successfully.")

        league_data = ['National League', 'American League']
        try:
            for league in league_data:
                cursor.execute("INSERT INTO League (league_name) VALUES (?)", (league, ))
            print('League table data created')
        except Exception as e:
            print("Exception:", e)

        try:
            for _, row in world_series_data.iterrows():
                cursor.execute('''INSERT INTO 
                WorldSeriesResults (year, nl_team, nl_score, al_team, al_score) VALUES (?,?,?,?,?)
                ''', (row['year'], row['nl team'], row['nl score'], row['al team'], row['al score']))
            print('WorldSeriesResults table data created')
        except Exception as e:
            print("Exception:", e)
        
        try:
            for _, row in ws_pitchers_biography.iterrows():
                cursor.execute('''INSERT INTO 
                PitchersData (pitcher_name, birthplace, birthdate, college, link, was_in_college) VALUES (?,?,?,?,?,?)
                ''', (row['name'], row['birthplace'], row['birthdate'], row['college'],row['link'], row['was_in_college']))
            print('PitchersData table data created')
        except Exception as e:
            print("Exception:", e)

        try:
            for _, row in  unique_teams_name.iterrows():
                cursor.execute('''INSERT INTO 
                Teams (team_name) VALUES (?)
                ''', (row['team_name'], ))
            print('Teams table data created')
        except Exception as e:
            print("Exception:", e)

        try:
            for _, row in nl_results.iterrows():
                cursor.execute('''INSERT INTO 
                NationalLeagueData (year, team_name, team_score, league_name, pitcher_name, link) VALUES (?,?,?,?,?,?)
                ''', (row['year'], row['nl team'], row['nl score'], 'National League', row['name'], row['link']))    
            print('NationalLeagueData table data created')
        except Exception as e:
            print("Exception:", e)

        try:
            for _, row in al_results.iterrows():
                cursor.execute('''INSERT INTO 
                AmericanLeagueData (year, team_name, team_score, league_name, pitcher_name, link) VALUES (?,?,?,?,?,?)
                ''', (row['year'], row['al team'], row['al score'], 'American League', row['name'], row['link']))
            print('AmericanLeagueData table data created')
        except Exception as e:
            print("Exception:", e)

        conn.commit()

except sqlite3.IntegrityError as e:
    print("Error inserting row:", row)
    print("Exception:", e)



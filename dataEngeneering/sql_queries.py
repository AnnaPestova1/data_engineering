import sqlite3   
import sys

def exit():
    print('See you later!')
    sys.exit()

def main():
    try:
        with  sqlite3.connect("../db/world_series.db") as conn:  
            conn.execute("PRAGMA foreign_keys = 1") 
            cursor = conn.cursor()

            print('Lets query some data!')
            print('''ATTENTION: 
                  You will be exit from app if you will type something not in the choice options''')
            def query_more(func):
                print('''
                      
                      
                      Do you want to continue query World series results?
                        y - yes
                        n - return to main menu
                        to exit type something else''')
                query = input('Choice: ').strip()
                if query == 'y':
                    func()
                elif query == 'n':
                    initial_query()
                else:
                    exit()
            def initial_query():

                    print('What you want to query?')
                    print('Choice options:')

                    print('1 Word Series results by year')
                    print('2 Word Series results by teams')
                    print('3 Receive a list of the pitchers from a team')
                    print('4 To exit')

                    choice = input('Your choice: ').strip()
                    if int(choice) == 1:
                        ws_by_years()
                    if int(choice) == 2:
                        ws_by_teams()
                    if int(choice) == 3:
                        pitchers_by_team()
                    else:
                        exit()

            def ws_by_years():
                try:
                    print('Type the year from 1903 to 2025')
                    year = input('Your choice: ').strip()
                    if int(year) >= 1903 and int(year) <= 2025:
                        cursor.execute('SELECT * FROM WorldSeriesResults WHERE year = ?', (int(year), ))
                        result = cursor.fetchall()
                        if result:
                            for row in result:
                                print(f"World series result for {year} year")
                                print(f"From National League played {row[1]} with the score {row[2]} from American League played {row[3]} with score {row[4]}")
                                query_more(ws_by_years)
                        else:
                            print(f'Where was no World Series games in {year} year')
                            query_more(ws_by_years)
                    else:
                        exit()
                except Exception as e:
                    print("Exception:", e)
                    exit()
                    
            def ws_by_teams():
                try:
                    cursor.execute('SELECT * FROM Teams')
                    teams_list = cursor.fetchall()
                    removed_tuples = list(map(lambda x: ''.join(x), teams_list))
                    print("Choose the team from the following list:")
                    print(removed_tuples)
                    team = input('Your choice: ').strip()
                    if team in removed_tuples:
                        cursor.execute('''SELECT t.team_name, w.year, w.nl_team, w.nl_score, w.al_team, w.al_score
                                       FROM Teams t 
                                       JOIN WorldSeriesResults w 
                                       ON t.team_name = w.nl_team OR t.team_name = w.al_team 
                                       WHERE t.team_name = ?
                                       ''', (team, ))
                        results = cursor.fetchall()
                        if results:
                            print(f"The team {team} have played in those World Series")
                            for row in results:
                                print(f"In {row[1]} year National League played {row[2]} with the score {row[3]} from American League played {row[4]} with score {row[5]}")
                                query_more(ws_by_teams)
                        else:
                            print(f'Something went wrong with the query for team {team}')
                            query_more(ws_by_teams)
                    else:
                        exit()
                
                except Exception as e:
                    print("Exception:", e)
                    exit()
                    
            def pitchers_by_team():
                try:
                    cursor.execute('SELECT * FROM Teams')
                    teams_list = cursor.fetchall()
                    removed_tuples = list(map(lambda x: ''.join(x), teams_list))
                    print("Choose the team from the following list:")
                    print(removed_tuples)
                    team = input('Your choice: ').strip()
                    if team in removed_tuples:
                        cursor.execute('''SELECT pitcher_name
                                    FROM NationalLeagueData
                                    WHERE team_name = ?
                                    UNION
                                    SELECT pitcher_name
                                    FROM AmericanLeagueData
                                    WHERE team_name = ?
                                    ''', (team, team))
                        results = cursor.fetchall()
                        removed_tuples_players = list(map(lambda x: ''.join(x), results))
                        print(f"For team {team} in World Series in different years played these pitchers: {", ".join(removed_tuples_players)}.")
                        query_more(pitchers_by_team)
                    else:
                        exit()
                
                except Exception as e:
                    print("Exception:", e)
                    exit()    
                
            while True:
                try:
                    initial_query()

                except Exception as e:
                    print("Exception:", e)
                    exit()
    except KeyboardInterrupt: 
        exit()
    except Exception as e:
        print("Exception:", e)

    finally:
        conn.close()

# if __name__ == "__main__":
main()

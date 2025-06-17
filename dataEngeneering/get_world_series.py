from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep

games_result = []
games_players_result = []
WS_players = []

# links will be saved in utils folder to allow run scrapping separately, if needed
games_links = []
pitchers_links = []


# # scrap data about world series finale by year
# try:
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     wait = WebDriverWait(driver, 10)
#     driver.get('https://www.baseball-almanac.com/ws/wsmenu.shtml')
#     sleep(3)

#     result_table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='boxed'][1]")))
#     # print('result_table', result_table)

#     table_rows = result_table.find_elements(By.CSS_SELECTOR, 'tr')
#     # print('table_rows', table_rows)

#     # need len(table_rows)-2) in range, because last 2 rows - columns name and table footer 
#     for i in range(len(table_rows)-2):
#         # skip header
#         if i == 0:
#             continue

#         row_data = table_rows[i].find_elements(By.CSS_SELECTOR, 'td')

#         if i == 1:
#             col_1 = row_data[0].text
#             col_2 = row_data[1].text
#             col_3 = row_data[2].text
#             col_4 = row_data[3].text
#             col_5 = row_data[4].text
#             continue

#         w_series = row_data[0].text.split('\n')[0]
#         # print(w_series)
#         nl_team = row_data[1].text.split('\n')[0]
#         # print(nl_team)
#         nl_win= row_data[2].text
#         # print(nl_win, type(nl_win))
#         al_team = row_data[3].text.split('\n')[0]
#         # print(al_team)
#         al_win= row_data[4].text
#         # print(al_win, type(al_win))

#                 # add link if anchor element exists, else - skip
#         try:
#             url = row_data[0].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
#             games_links.append(url)
#         except:
#             url = None

#         # append dictionary with the world series for specific year to results
#         # change headers to make unique for saving in object
#         games_result.append({col_1: w_series, col_2: nl_team, f"NL {col_3}": nl_win, col_4: al_team, f"AL {col_5}": al_win, 'Links': url })


# except Exception as e:
#     print(f"An exception occurred: {type(e).__name__} {e}")
# finally:
#     driver.quit()

# print('results', len(games_result))

# # save data about games in the csv file
# try:
#     ws_results = pd.DataFrame(games_result)
#     # print(ws_results)
#     # created new copy the file to save to not lose the original data
#     ws_results.to_csv('../dirty_data/world_series_results_copy.csv', index=False)
#     print('world_series_results.csv created')

# except Exception as err:
#     print(f"Error during creating world_series_results.csv file occur {err}")

# # saving urls into utils csv file
# try:
#     ws_games_links = pd.DataFrame(games_links, columns = ['url'])
#     # print(ws_results)
#     # created new copy the file to save to not lose the original data
#     ws_games_links.to_csv('../utils/ws_games_links_copy.csv', index=False)
#     print('ws_games_links.csv created')

# except Exception as err:
#     print(f"Error during creating ws_games_links.csv file occur {err}")



# try:
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     wait = WebDriverWait(driver, 10)
#     # uncomment this line if running the whole file and creating data from scratch
#     # links = games_links

#     # uncomment this line if want to run only these scrapping data
#     # links_from_csv = pd.read_csv('../utils/ws_games_links.csv', skipinitialspace=True)
#     # links = links_from_csv['url'].tolist()

#     # uncomment this for testing and debugging purposes
#     links = ['https://www.baseball-almanac.com/ws/yr1990ws.shtml']
#     # links = ['https://www.baseball-almanac.com/ws/yr2002ws.shtml']
#     # links = ['https://www.baseball-almanac.com/ws/yr1903ws.shtml', 'https://www.baseball-almanac.com/ws/yr1907ws.shtml', 'https://www.baseball-almanac.com/ws/yr1915ws.shtml', 'https://www.baseball-almanac.com/ws/yr1905ws.shtml', 'https://www.baseball-almanac.com/ws/yr1990ws.shtml']
#     # print(links)

#     for link in links:
#         # print(link)
#         driver.get(link)
#         sleep(3)
        
#         tables = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='boxed']")))

#         result_table = tables[-1]
#         # print('result_table', result_table)
#         table_rows = result_table.find_elements(By.CSS_SELECTOR, 'tr')
#         # print('table_rows', table_rows, len(table_rows))
#         initial_data = {
#             'world_series': '',
#             'first_header': '',
#             'first_team_totals': 0,
#             'first_team': [],
#             'first_team_urls': [],   
#             'second_header': '',
#             'second_team': [],
#             'second_team_urls': [], 
#             'second_team_totals': 0,
#         }
#         for row in table_rows:
#             row_data = row.find_elements(By.CSS_SELECTOR, 'td')
#             data = row_data[0]
#             class_name = data.get_attribute("class")
#             # print(class_name)
#             if class_name == 'banner':
#                 if data.text == 'Totals':
#                     if initial_data['second_header'] == '':
#                         initial_data['first_team_totals']= row_data[1].text
#                         # print('initial_data totals 1', initial_data)
#                     else:
#                         initial_data['second_team_totals'] = row_data[1].text
#                         # print('initial_data totals 2', initial_data)
#                 else:
#                     continue
#             if class_name == 'header':
#                 if data.text == 'Totals':
#                     if initial_data['second_header'] == '':
#                         initial_data['first_team_totals']= row_data[1].text
#                         # print('initial_data totals in header', initial_data)
#                     else:
#                         initial_data['second_team_totals'] = row_data[1].text
#                         # print('initial_data totals in header', initial_data)
#                 else:
#                     # print('headers', class_name, initial_data['first_header'],initial_data['second_header'])
#                     if initial_data['first_header'] == '':
#                         initial_data['world_series'] = data.find_elements(By.CSS_SELECTOR, 'h2')[0].text
#                         if initial_data['world_series'] == '1907 World Series':
#                             initial_data['first_header'] = data.find_elements(By.CSS_SELECTOR, 'p')[1].text
#                         else:
#                             initial_data['first_header'] = data.find_elements(By.CSS_SELECTOR, 'p')[0].text
#                     else:
#                         initial_data['second_header'] = data.find_elements(By.CSS_SELECTOR, 'p')[0].text
#                         # print('initial_data 2', initial_data)
#             if class_name == 'datacolBlue':
#                 # print('data.text', data.text)
#                 if data.text == 'Totals':
#                     if initial_data['second_header'] == '':
#                         initial_data['first_team_totals']= row_data[1].text
#                         # print('initial_data totals 3', initial_data)
#                     else:
#                         initial_data['second_team_totals'] = row_data[1].text
#                         # print('initial_data totals 4', initial_data)
#                 else:
#                     pitcher_name = data.text
#                     urls = data.find_elements(By.CSS_SELECTOR, 'a')
#                     team_links = [] 
#                     for url in urls:
#                         single_url = url.get_attribute('href')
#                         pitchers_links.append(single_url)
#                         team_links.append(single_url)
#                         # print('team_links 3', team_links) 

#                     # print('pitcher_name', pitcher_name)
#                     if initial_data['second_header'] == '':
#                         # print('team_links 7', team_links)
#                         initial_data['first_team_urls'].append(team_links) 
#                         initial_data['first_team'].append(pitcher_name)
#                         # print("3",pitcher_name, pitchers_links)
#                         # print("3", pitcher_name, pitchers_links, initial_data)
#                     else:
#                         # print('team_links 7', team_links)
#                         initial_data['second_team_urls'].append(team_links) 
#                         initial_data['second_team'].append(pitcher_name)
#                         # print("4", pitcher_name, pitchers_links)
#                         # print("4", pitcher_name, pitchers_links, initial_data)

#             if class_name == 'datacolBox':
#                 if data.text == 'Totals':
#                     if initial_data['second_header'] == '':
#                         initial_data['first_team_totals']= row_data[1].text
#                         # print('initial_data totals 3', initial_data)
#                     else:
#                         initial_data['second_team_totals'] = row_data[1].text
#                         # print('initial_data totals 4', initial_data)
#                 else:
#                     pitcher_name = data.text
#                     # print('pitcher_name', pitcher_name)
#                     urls = data.find_elements(By.CSS_SELECTOR, 'a')
#                     team_links = []
#                     # print('len(urls)', len(urls))
#                     for url in urls:
#                         single_url = url.get_attribute('href')
#                         pitchers_links.append(single_url)
#                         team_links.append(single_url) 
#                         # print('team_links 4', team_links) 
#                     if initial_data['second_header'] == '':    
#                         initial_data['first_team'].append(pitcher_name)
#                         # print('team_links 5', team_links) 
#                         initial_data['first_team_urls'].append(team_links)
#                         # print("5", pitcher_name, pitchers_links, initial_data)
#                     else:
#                         initial_data['second_team'].append(pitcher_name)
#                         # print('team_links 6', team_links)
#                         initial_data['second_team_urls'].append(team_links)
#                         # print("6", pitcher_name, pitchers_links, initial_data)   
#         # print('initial_data', initial_data)
#         games_players_result.append({'World Series': initial_data['world_series'], 'Team 1': initial_data['first_header'], 'Team 1 Pitchers': initial_data['first_team'], 'Team 1 Pitchers Links': initial_data['first_team_urls'], 'Team 1 wins': initial_data['first_team_totals'], 'Team 2': initial_data['second_header'], 'Team 2 Pitchers': initial_data['second_team'], 'Team 2 Pitchers Links': initial_data['second_team_urls'], 'Team 2 wins': initial_data['second_team_totals'], 'Links': link })
#         # print('games_players_result', games_players_result)

# except Exception as e:
#     print(f"An exception occurred: {type(e).__name__} {e}")
# finally:
#     driver.quit()

# # save data into csv file
# try:
#     ws_players_results = pd.DataFrame(games_players_result)
#     # print(ws_results)
#     # created new copy the file to save to not lose the original data
#     ws_players_results.to_csv('../dirty_data/world_series_pitchers_results_copy.csv', index=False)
#     # print('world_series_pitchers_results.csv created')

# except Exception as err:
#     print(f"Error during creating world_series_pitchers_results_copy.csv file occur {err}")

# # saving urls into utils csv file
# try:
#     ws_pitchers_links = pd.DataFrame(pitchers_links, columns = ['url'])
#     # print(ws_results)
#     # created new copy the file to save to not lose the original data
#     ws_pitchers_links.to_csv('../utils/ws_pitchers_links_copy.csv', index=False)
#     print('ws_pitchers_links.csv created')

# except Exception as err:
#     print(f"Error during creating ws_pitchers_links.csv file occur {err}")

# #scrapping pitchers biographies

# try:
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     wait = WebDriverWait(driver, 10)

#     # # uncomment this line if running the whole file and creating data from scratch
#     # links = pitchers_links

#     # # uncomment this line if want to run only these scrapping data
#     links_from_csv = pd.read_csv('../utils/ws_pitchers_links.csv', skipinitialspace=True)
#     links = links_from_csv['url'].unique().tolist()
#     print(len(links_from_csv), len(links))

# #   # uncomment this for testing and debugging purposes
#     # links = ['https://www.baseball-almanac.com/players/player.php?p=janseke01', 'https://www.baseball-almanac.com/players/player.php?p=astacez01', 'https://www.baseball-almanac.com/players/player.php?p=mcginjo01']
#     # print(links)

#     for link in links:
#         print('link', link)
#         driver.get(link)
#         sleep(3)
        
#         result_table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='boxed'][1]")))

#         table_rows = result_table.find_elements(By.CSS_SELECTOR, 'tr')
#         initial_data = {
#             'full_name': '',
#             'born_on': '',
#             'born_in': '',
#             'college': ''
#         }
#         for row in table_rows:
#             row_data = row.find_elements(By.CSS_SELECTOR, 'td')
#             data = row_data[0]
#             class_name = data.get_attribute("class")
#             if class_name == 'header':
#                 # print("1")
#                 initial_data['full_name'] = data.find_elements(By.CSS_SELECTOR, 'h2')[0].text
#                 # print("1", initial_data)
#             if class_name == 'biocolpad' and data.text == 'Born On:':
#                 # print("2")
#                 initial_data['born_on'] = row_data[1].text
#                 # print("2", initial_data)
#             if class_name == 'biocolpad' and 'Born In:' in data.text:
#                 # print("3")
#                 born = row_data[1].text
#                 # print(born)
#                 initial_data['born_in'] = born
#             if class_name == 'biocolpad' and data.text == 'College:':
#                 # print("4")
#                 initial_data['college'] = row_data[1].text
#         print('initial_data', initial_data)
#         WS_players.append({'Full name': initial_data['full_name'], 'Born in': initial_data['born_in'], 'Born-on': initial_data['born_on'], 'College': initial_data['college'], 'Links': link })

# except Exception as e:
#     print(f"An exception occurred: {type(e).__name__} {e}")
# finally:
#     driver.quit()


# try:
#     ws_players_biography = pd.DataFrame(WS_players)
#     # created new copy the file to save to not lose the original data
#     ws_players_biography.to_csv('../dirty_data/world_series_pitchers_biography_copy.csv', index=False)
#     print('world_series_pitchers_biography.csv created')

# except Exception as err:
#     print(f"Error during creating world_series_pitchers_biography.csv file occur {err}")



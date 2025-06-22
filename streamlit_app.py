import streamlit as st  
import pandas as pd   
import altair as alt
import ast
import numpy as np

try: 
    ws_results=pd.read_csv('cleaned dataframes/world_series_data.csv')
    nl_results=pd.read_csv('cleaned dataframes/nl_results.csv')
    al_results=pd.read_csv('cleaned dataframes/al_results.csv')
    ws_pitchers_biography=pd.read_csv('cleaned dataframes/clean_df_world_series_pitchers_biography.csv')
    unique_teams_name=pd.read_csv('cleaned dataframes/unique_teams_name.csv')


    # data for search
    teams = unique_teams_name['team_name'].sort_values()
    years = ws_results['year']
    leagues = ['National League', 'American League']
    colleges = ws_pitchers_biography['college'].unique().tolist()
    countries = ws_pitchers_biography['birthplace'].unique().tolist()
    pitchers_name = ws_pitchers_biography['name'].unique().tolist()

    st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state="auto", menu_items=None)
    
    st.sidebar.header('Choose search params')
    league_index = None

    min_year, max_year = int(years.min()), int(years.max())
    selected_team = st.sidebar.selectbox('Select Team', teams, placeholder="Select team", index=None) 

    min_year, max_year = st.sidebar.select_slider('Select Year', options=years, value = (min_year, max_year)) 
    on= st.sidebar.toggle("drop leagues")
    if on:
        selected_league = st.sidebar.radio('Select League', leagues, index=league_index)
    else:
        selected_league = None

    selected_college = st.sidebar.selectbox('Select College', colleges, placeholder="Select college", index=None) 
    selected_country = st.sidebar.selectbox('Select Country', countries, placeholder="Select country", index=None) 

    game_table = ws_results[['year', 'nl team', 'nl score', 'nl pitchers', 'al team', 'al score', 'al pitchers']]
    game_table= game_table.rename(columns={'nl team': 'National League team', 'nl score': 'National League score', 'nl pitchers': 'National League pitchers', 'al team': 'American League team', 'al score': 'American League score', 'al pitchers': 'American League pitchers'}, errors='raise')
    game_table['National League pitchers'] = game_table['National League pitchers'].apply(lambda x: ', '.join(ast.literal_eval(x)))
    game_table['American League pitchers'] = game_table['American League pitchers'].apply(lambda x: ', '.join(ast.literal_eval(x)))
    reorganized_game_table = game_table.iloc[:, [0, 3, 1, 2, 5, 4, 6]]
    if min_year >1903 & max_year<2024:  
        reorganized_game_table = reorganized_game_table[(reorganized_game_table['year'] >= min_year) & (reorganized_game_table['year'] <= max_year)]
    if selected_league!= None:
        if selected_league == 'National League':
            reorganized_game_table = reorganized_game_table.drop(columns=['American League team', 'American League score', 'American League pitchers'])
        else:
            reorganized_game_table = reorganized_game_table.drop(columns=['National League team', 'National League score', 'National League pitchers'])


    if selected_team!= None:
        if selected_league =='American League':
            reorganized_game_table = reorganized_game_table[(reorganized_game_table['American League team'] == selected_team)]
        elif selected_league == 'National League':
            reorganized_game_table = reorganized_game_table[(reorganized_game_table['National League team'] == selected_team)]
        else:
            reorganized_game_table = reorganized_game_table[(reorganized_game_table['American League team'] == selected_team) | (reorganized_game_table['National League team'] == selected_team)]
    st.title('Some Facts About the World Series')


    st.header('World Series games')
    st.dataframe(reorganized_game_table, hide_index=True)

    
    total_pitchers_number = len(ws_pitchers_biography)
    in_college = ws_pitchers_biography['college'].value_counts().get('None Attended', 0)
    no_college = total_pitchers_number - in_college
    college_attendance = pd.DataFrame({'attendance': ['attended', 'non attended'], 'count':[in_college, no_college]})
    pd.set_option('display.max_colwidth', None)
    college_birthplace_displaying_data = al_results.merge(nl_results, how = 'outer')
    college_birthplace_displaying_data['birthdate'] = pd.to_datetime(college_birthplace_displaying_data['birthdate'], format='%Y-%m-%d', errors='coerce')


    filtered_college_data = ws_pitchers_biography[['name', 'college']]

    filtered_college_data = filtered_college_data[(ws_pitchers_biography['college'] == selected_college)]

    college_by_year = college_birthplace_displaying_data[['year', 'was_in_college']]
    # non_attended_college_by_year = college_birthplace_displaying_data[['year', 'was_in_college']]

    attended_college_by_year = college_by_year.groupby('year')['was_in_college'].apply(lambda x: (x == True).sum()).reset_index().rename(columns={'was_in_college': 'attended'}, errors='raise')
    non_attended_college_by_year = college_by_year.groupby('year')['was_in_college'].apply(lambda x: (x == False).sum()).reset_index().rename(columns={'was_in_college': 'non attended'}, errors='raise')
    line_chart_college_attendance_by_year = attended_college_by_year.merge(non_attended_college_by_year, how = 'outer')
    line_chart_college_attendance_by_year['year'] = pd.to_datetime(line_chart_college_attendance_by_year['year'], format='%Y', errors='coerce')

    college_by_team = college_birthplace_displaying_data[['nl team', 'al team', 'was_in_college']]

    college_by_team = college_by_team.rename(columns={'nl team': 'team'}, errors='raise')

    college_by_team['team'] = college_by_team['team'].fillna(college_by_team['al team'])
    college_by_team = college_by_team.drop(columns=['al team'])
    # non_attended_college_by_team = college_birthplace_displaying_data[['year', 'was_in_college']]

    attended_college_by_team = college_by_team.groupby('team')['was_in_college'].apply(lambda x: (x == True).sum()).reset_index().rename(columns={'was_in_college': 'attended'}, errors='raise')
    non_attended_college_by_team = college_by_team.groupby('team')['was_in_college'].apply(lambda x: (x == False).sum()).reset_index().rename(columns={'was_in_college': 'non attended'}, errors='raise')

    line_chart_college_attendance_by_team = attended_college_by_team.merge(non_attended_college_by_team, how = 'outer')

    st.header('Explore Pitchers Data By Name')

    @st.dialog('Did you know?')

    def pitcher_name(name):
        filtered_college_birthplace_displaying_data = college_birthplace_displaying_data[(college_birthplace_displaying_data['name'] == name)].reset_index()
        collected_data = {}
        list_of_teams=[]
        for i in range(len(filtered_college_birthplace_displaying_data)):
            year = int(filtered_college_birthplace_displaying_data['year'][i])
            team = filtered_college_birthplace_displaying_data['nl team'][i] if pd.notna(filtered_college_birthplace_displaying_data['nl team'][i]) else filtered_college_birthplace_displaying_data['al team'][i]
            was_in_college = filtered_college_birthplace_displaying_data['was_in_college'][i]
            college = filtered_college_birthplace_displaying_data['college'][i]
            if team not in collected_data.keys():
                collected_data[team] = [year]
                list_of_teams.append(team)
            else:
                collected_data[team].append(year)

        team_and_year_played = []
        for team_name in list_of_teams:
            team_and_year_played.append(f"with the {team_name} in {", ".join(str(y) for y in collected_data[team_name])}")
        
        college_attended = f"{name} {f'attended {college}' if was_in_college == True else 'has not attended college'}"

        st.write(f"**{name}** was born on {filtered_college_birthplace_displaying_data["birthdate"][0].strftime('%m-%d-%Y')} in {filtered_college_birthplace_displaying_data["birthplace"][0]} and played {", and ".join(team_and_year_played)}. {college_attended}.")

    form = st.form("pitcher_data")
    name = form.selectbox('Select Pitcher', pitchers_name, placeholder="Select or type pitcher name", index=None)
    submitted = form.form_submit_button("Submit")
    if submitted:
        pitcher_name(name)

    st.header('College attendance')

    tab1, tab2, tab3, tab4 = st.tabs(['Pie Chart', 'Line Chart By Year', 'Line Chart By Team', 'Dropdown By College'])

    with tab1:
        chart = alt.Chart(college_attendance).mark_arc().encode(
        theta=alt.Theta(field='count', type='quantitative'),
        color=alt.Color(field='attendance', type='nominal', scale=alt.Scale(range=["#0000FF", "#FF0000"])),
    )
        st.altair_chart(chart)
    with tab2:
        st.line_chart(line_chart_college_attendance_by_year, x='year', y=['attended', 'non attended'], color=["#0000FF", "#FF0000"]) 
    with tab3:
        st.line_chart(line_chart_college_attendance_by_team, x='team', y=['attended', 'non attended'], color=["#0000FF", "#FF0000"]) 
    with tab4:  
        st.subheader('Explore college attendance via sidebar dropdown', divider='blue')
        st.dataframe(filtered_college_data, hide_index=True)
    



    st.header('Birth Places')


    filtered_birthplace_data = ws_pitchers_biography[['name', 'birthplace']]

    filtered_birthplace_data = filtered_birthplace_data[(ws_pitchers_biography['birthplace'] == selected_country)]
        
    birthplace_data = ws_pitchers_biography.groupby('birthplace', as_index=False)['name'].count()
   
    birthplace_data= birthplace_data.rename(columns={'name': 'count'}, errors='raise')

    tab11, tab12 = st.tabs(['Line Chart By Country', 'Dropdown By Country'])
    with tab11:
        st.line_chart(birthplace_data, x='birthplace', y='count')
    with tab12:
        st.subheader('Explore places of birth via sidebar dropdown', divider='blue')
        st.dataframe(filtered_birthplace_data, hide_index=True)



except Exception as e:
        st.toast(f"The error occur: {e}")
        
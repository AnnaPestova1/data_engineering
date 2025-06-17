import streamlit as st  
import pandas as pd   
import altair as alt

try: 
    ws_results=pd.read_csv('../cleaned dataframes/world_series_data.csv')
    nl_results=pd.read_csv('../cleaned dataframes/nl_results.csv')
    al_results=pd.read_csv('../cleaned dataframes/al_results.csv')
    ws_pitchers_biography=pd.read_csv('../cleaned dataframes/clean_df_world_series_pitchers_biography.csv')
    unique_teams_name=pd.read_csv('../cleaned dataframes/unique_teams_name.csv')


    # data for search
    teams = unique_teams_name['team_name'].sort_values()
    years = ws_results['year']
    leagues = ['National League', 'American League']
    colleges = ws_pitchers_biography['college'].unique().tolist()
    countries = ws_pitchers_biography['birthplace'].unique().tolist()
    
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

    game_table = ws_results[['year', 'nl team', 'nl score', 'al team', 'al score']]
    game_table= game_table.rename(columns={'nl team': 'NL team', 'nl score': 'NL score', 'al team': 'AL team', 'al score': 'AL score'}, errors='raise')
    
    if min_year >1903 & max_year<2024:  
        game_table = game_table[(game_table['year'] >= min_year) & (game_table['year'] <= max_year)]
    if selected_league!= None:

        if selected_league == 'National League':
            game_table = game_table.drop(columns=['AL team', 'AL score'])
        else:
            game_table = game_table.drop(columns=['NL team', 'NL score'])


    if selected_team!= None:
        game_table = game_table[(game_table['AL team'] == selected_team) | (game_table['NL team'] == selected_team)]
       
    st.title('Some Facts About World Series')

    st.header('World Series games')
    st.dataframe(game_table, hide_index=True)

    
    total_pitchers_number = len(ws_pitchers_biography)
    in_college = ws_pitchers_biography['college'].value_counts().get('None Attended', 0)
    no_college = total_pitchers_number - in_college
    college_attendance = pd.DataFrame({'attendance': ['attended', 'non_attended'], 'count':[in_college, no_college]})

    filtered_college_data = ws_pitchers_biography[['name', 'college']]

    filtered_college_data = filtered_college_data[(ws_pitchers_biography['college'] == selected_college)]

    st.header('College attendance')

    chart = alt.Chart(college_attendance).mark_arc().encode(
    theta=alt.Theta(field="count", type="quantitative"),
    color=alt.Color(field="attendance", type="nominal"),
)
    st.altair_chart(chart)

    st.subheader('Explore college attendance via sidebar dropdown', divider='blue')
    st.dataframe(filtered_college_data, hide_index=True)

    st.header('Birth Places')

    filtered_birthplace_data = ws_pitchers_biography[['name', 'birthplace']]

    filtered_birthplace_data = filtered_birthplace_data[(ws_pitchers_biography['birthplace'] == selected_country)]
        
    birthplace_data = ws_pitchers_biography.groupby('birthplace', as_index=False)['name'].count()
   
    birthplace_data= birthplace_data.rename(columns={'name': 'count'}, errors='raise')

    st.line_chart(birthplace_data, x='birthplace', y='count')

    st.subheader('Explore places of birth via sidebar dropdown', divider='blue')
    st.dataframe(filtered_birthplace_data, hide_index=True)
except Exception as e:
        st.toast(f"The error occur: {e}")
        
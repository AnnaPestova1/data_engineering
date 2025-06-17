**MLB World Series Data Explorer**
This project is part of the final assignment for the Python course at Code The Dream. It demonstrates end-to-end data handling: from web scraping and cleaning to database management and interactive data visualization.

*Project Components*
Web Scraping Program
Scrapes historical World Series data from the Major League Baseball History website. The data is cleaned, assembled into structured pandas DataFrames, and exported to CSV files.

Database Import Program
Loads the cleaned CSV files into a SQLite database, with each dataset stored in its own table. Foreign key constraints are used to maintain data integrity.

Database Query Program
A command-line interface that allows users to query the database using JOIN operations to combine and extract insights from different tables.

Dashboard Program
A Streamlit-based web dashboard that visualizes the World Series results, pitcher biographies, and other data. Users can interactively explore team performances and player stats by year or league.

_Live Demo_
 Streamlit app: 

_Running Locally_
To run this project locally:

Clone the repository.

Create and activate a virtual environment.

Install the required libraries:

`pip install -r requirements.txt`

Run the database import and query scripts from the terminal to generate the database.

_Run database query program:_

`python sql_queries.py`

_Launch the Streamlit app:_

`streamlit run streamlit_dashboard.py`
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
 Streamlit app: https://dataengineering-annapestova.streamlit.app

_Running Locally_
To run this project locally:

Clone the repository.

Create and activate a virtual environment.

Install the required libraries:

`pip install -r requirements.txt`

Run the database import and query scripts from the terminal to generate the database or use already existing results in the repository. 

_Run database query program:_
checkout into the `dataEngeneering` folder.

`python sql_queries.py`

_Launch the Streamlit app:_

`streamlit run streamlit_app.py`

Screenshots:
query via terminal:
<img width="962" alt="image" src="https://github.com/user-attachments/assets/4783fd8a-082d-4af2-ad89-7347c3b55cac" />

streamlit app:
<img width="1918" alt="image" src="https://github.com/user-attachments/assets/e11b3a3e-0533-4856-9844-f55b2655a722" />
<img width="1890" alt="image" src="https://github.com/user-attachments/assets/57aa2679-c1a2-4627-8850-017b9092cd1d" />
<img width="1755" alt="image" src="https://github.com/user-attachments/assets/093ab4ac-a52b-4df2-b445-1e6ba6581ce6" />




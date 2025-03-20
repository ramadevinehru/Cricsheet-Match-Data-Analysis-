import mysql.connector
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cricket Data Analysis", layout="wide")

print("Streamlit app is starting...")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "cricket_db",
}

def fetch_data(query):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        print(f"Error: {e}")
        return None

st.title("Cricket Match Data Analysis")
st.write("Select a query to fetch insights from MySQL.")

print("UI Loaded")

queries = {
    "Top 10 Batsmen by Runs (ODI)": "SELECT batter, SUM(runs_batter) AS total_runs FROM odi_matches GROUP BY batter ORDER BY total_runs DESC LIMIT 10",
    "Leading Wicket-Takers (T20)": "SELECT bowler, COUNT(wicket) AS total_wickets FROM t20_matches WHERE wicket IS NOT NULL GROUP BY bowler ORDER BY total_wickets DESC LIMIT 10",
    "Players with Most Centuries": """SELECT batter, COUNT(*) AS centuries FROM (
        SELECT batter, SUM(runs_batter) AS runs FROM test_matches GROUP BY batter HAVING runs >= 100
        UNION ALL
        SELECT batter, SUM(runs_batter) AS runs FROM odi_matches GROUP BY batter HAVING runs >= 100
        UNION ALL
        SELECT batter, SUM(runs_batter) AS runs FROM t20_matches GROUP BY batter HAVING runs >= 100
    ) AS centuries_count GROUP BY batter ORDER BY centuries DESC LIMIT 10""",
    
    "Team with Highest Win Percentage (Test)": """SELECT winner, COUNT(*) AS wins, 
        (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM test_matches)) AS win_percentage 
        FROM test_matches GROUP BY winner ORDER BY win_percentage DESC LIMIT 1""",
    "Most Wins by a Team (ODI)": "SELECT winner, COUNT(*) AS total_wins FROM odi_matches WHERE winner IS NOT NULL GROUP BY winner ORDER BY total_wins DESC LIMIT 1",
    "Matches with Narrowest Victory (ODI)": "SELECT * FROM odi_matches WHERE runs_total BETWEEN 1 AND 10 ORDER BY runs_total ASC LIMIT 5",
    
    "Most Frequent Player of the Match Winners": "SELECT player_of_match, COUNT(*) AS awards FROM odi_matches GROUP BY player_of_match ORDER BY awards DESC LIMIT 5",
    "Average Runs per Over (T20)": "SELECT AVG(runs_total) AS avg_runs_per_over FROM t20_matches WHERE `over` IS NOT NULL",
    "Impact of Toss on Match Result (ODI)": "SELECT toss_winner, winner, COUNT(*) AS match_count FROM odi_matches WHERE toss_winner = winner GROUP BY toss_winner, winner ORDER BY match_count DESC",
    
    "Most Common Match Venues (Test)": "SELECT venue, COUNT(*) AS match_count FROM test_matches GROUP BY venue ORDER BY match_count DESC LIMIT 5",
    "Cities with Highest ODI Matches": "SELECT city, COUNT(*) AS match_count FROM odi_matches GROUP BY city ORDER BY match_count DESC LIMIT 5",
    
    "Toss Winning Percentage Per Team": """SELECT toss_winner, COUNT(*) AS toss_wins, 
        (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM odi_matches)) AS toss_win_percentage 
        FROM odi_matches GROUP BY toss_winner ORDER BY toss_win_percentage DESC LIMIT 5""",
    
    "Highest Team Totals (ODI)": "SELECT teams, MAX(runs_total) AS highest_score FROM odi_matches GROUP BY teams ORDER BY highest_score DESC LIMIT 5",
    "Highest Partnership Runs in a Match": "SELECT team, SUM(runs_batter) AS total_partnership FROM odi_matches GROUP BY team ORDER BY total_partnership DESC LIMIT 5",
    
    "Bowlers with Best Economy (ODI)": """SELECT bowler, 
        (SUM(runs_total) / COUNT(DISTINCT `over`)) AS economy_rate 
        FROM odi_matches GROUP BY bowler ORDER BY economy_rate ASC LIMIT 5""",
    
    "Most Common Winning Margin (T20)": "SELECT winner, COUNT(*) AS match_wins FROM t20_matches WHERE runs_total >= 50 GROUP BY winner ORDER BY match_wins DESC LIMIT 5",
    
    "Players with Most Ducks (ODI)": "SELECT batter, COUNT(*) AS ducks FROM odi_matches WHERE runs_batter = 0 GROUP BY batter ORDER BY ducks DESC LIMIT 5",
    
    "Teams with Highest Run Rate (T20)": """SELECT teams, 
        (SUM(runs_total) / COUNT(DISTINCT `over`)) AS run_rate 
        FROM t20_matches GROUP BY teams ORDER BY run_rate DESC LIMIT 5""",
    "Most Wickets Taken in a Match (ODI)": "SELECT match_type, bowler, COUNT(wicket) AS wickets_in_match FROM odi_matches WHERE wicket IS NOT NULL GROUP BY match_type, bowler ORDER BY wickets_in_match DESC LIMIT 1",
    "Most Successful Chases (ODI)": """SELECT winner, COUNT(*) AS successful_chases 
        FROM odi_matches WHERE toss_decision = 'field' AND winner IS NOT NULL 
        GROUP BY winner ORDER BY successful_chases DESC LIMIT 5""",
}

selected_query = st.selectbox("Select a Query", list(queries.keys()))

if st.button("Run Query"):
    print(f"Running Query: {selected_query}")
    query = queries[selected_query]
    result_df = fetch_data(query)

    if result_df is not None and not result_df.empty:
        st.write(result_df)
        print("Query Executed Successfully")
    else:
        st.write("No data available for this query.")
        print("No Data Found")

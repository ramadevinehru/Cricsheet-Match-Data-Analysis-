import os
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

EDA_PLOTS_DIR = "eda_plots"
if not os.path.exists(EDA_PLOTS_DIR):
    os.makedirs(EDA_PLOTS_DIR)
    print(f" Created folder: {EDA_PLOTS_DIR}")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "cricket_db",
}

def fetch_data(query):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

odi_df = fetch_data("SELECT * FROM odi_matches")
t20_df = fetch_data("SELECT * FROM t20_matches")
test_df = fetch_data("SELECT * FROM tests_matches") 

print("ODI Matches Info:", odi_df.info(), "\n")
print("T20 Matches Info:", t20_df.info(), "\n")
print("Test Matches Info:", test_df.info(), "\n")

print("Missing Values in ODI Matches:\n", odi_df.isnull().sum(), "\n")
print("Missing Values in T20 Matches:\n", t20_df.isnull().sum(), "\n")
print("Missing Values in Test Matches:\n", test_df.isnull().sum(), "\n")

print("ODI Matches Stats:\n", odi_df.describe(), "\n")
print("T20 Matches Stats:\n", t20_df.describe(), "\n")
print("Test Matches Stats:\n", test_df.describe(), "\n")

sns.set_style("darkgrid")

top_batsmen = odi_df.groupby("batter")["runs_batter"].sum().nlargest(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_batsmen.values, y=top_batsmen.index, palette="Blues_r")
plt.title("Top 10 Batsmen by Total Runs (ODI)")
plt.xlabel("Total Runs")
plt.ylabel("Batsmen")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "top_10_batsmen_odi.png"))
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(odi_df["runs_total"], bins=30, kde=True, color="green")
plt.title("Distribution of Total Runs Scored (ODI)")
plt.xlabel("Total Runs")
plt.ylabel("Frequency")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "runs_distribution_odi.png"))
plt.show()

top_bowlers = t20_df.groupby("bowler")["wicket"].count().nlargest(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, palette="Reds_r")
plt.title("Top 10 Wicket-Takers (T20)")
plt.xlabel("Total Wickets")
plt.ylabel("Bowlers")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "top_10_wicket_takers_t20.png"))
plt.show()

toss_decision_counts = odi_df["toss_decision"].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(toss_decision_counts, labels=toss_decision_counts.index, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"])
plt.title("Toss Decision Distribution (ODI)")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "toss_decisions_odi.png"))
plt.show()

top_venues = test_df["venue"].value_counts().nlargest(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_venues.values, y=top_venues.index, palette="Purples_r")
plt.title("Most Common Match Venues (Test Matches)")
plt.xlabel("Number of Matches")
plt.ylabel("Venue")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "top_venues_test.png"))
plt.show()

top_teams = odi_df["winner"].value_counts().nlargest(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_teams.values, y=top_teams.index, palette="coolwarm")
plt.title("Most Wins by Teams (ODI)")
plt.xlabel("Number of Wins")
plt.ylabel("Teams")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "top_winning_teams_odi.png"))
plt.show()

plt.figure(figsize=(10, 5))
sns.boxplot(x=t20_df["over"], y=t20_df["runs_total"], palette="Set3")
plt.title("Runs per Over in T20 Matches")
plt.xlabel("Over Number")
plt.ylabel("Total Runs")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "runs_per_over_t20.png"))
plt.show()

plt.figure(figsize=(8, 5))
sns.scatterplot(x=odi_df["runs_total"], y=odi_df["wicket"], alpha=0.7)
plt.title("Runs vs. Wickets (ODI Matches)")
plt.xlabel("Total Runs")
plt.ylabel("Wickets Taken")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "runs_vs_wickets_odi.png"))
plt.show()

odi_df["season"] = pd.to_numeric(odi_df["season"], errors="coerce")
win_percentage = odi_df.groupby("season")["winner"].value_counts(normalize=True).unstack().fillna(0) * 100
plt.figure(figsize=(12, 5))
win_percentage.plot(kind="line", marker="o", cmap="viridis")
plt.title("Yearly Win Percentage by Teams (ODI)")
plt.xlabel("Year")
plt.ylabel("Win Percentage (%)")
plt.savefig(os.path.join(EDA_PLOTS_DIR, "yearly_win_percentage_odi.png"))
plt.show()

highest_totals_t20 = t20_df.groupby("teams")["runs_total"].max().nlargest(10).reset_index()
fig = px.bar(highest_totals_t20, x="teams", y="runs_total", title="Highest Team Totals in T20 Matches", color="teams")
fig.write_image(os.path.join(EDA_PLOTS_DIR, "highest_team_totals_t20.png"))
fig.show()

print("All EDA visualizations saved in `eda_plots/` folder!")

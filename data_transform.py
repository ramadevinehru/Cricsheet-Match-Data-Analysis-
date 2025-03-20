import os
import json
import pandas as pd

json_folder_path = "E:/cricket/IPL_json"
csv_output_path = "E:/cricket.csv"

def process_json_file(file_path):
    """Process a single JSON file and return a DataFrame."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    match_info = data.get("info", {})
    teams = match_info.get("teams", [])

    match_details = {
        "match_type": match_info.get("match_type"),
        "season": match_info.get("season"),
        "city": match_info.get("city"),
        "venue": match_info.get("venue"),
        "toss_winner": match_info.get("toss", {}).get("winner"),
        "toss_decision": match_info.get("toss", {}).get("decision"),
        "winner": match_info.get("outcome", {}).get("winner", "draw"),
        "player_of_match": ", ".join(match_info.get("player_of_match", [])),
        "teams": ", ".join(teams),
    }

    innings_data = []
    for inning in data.get("innings", []):
        team = inning.get("team", "Unknown")
        for over in inning.get("overs", []):
            over_number = over.get("over")
            for delivery in over.get("deliveries", []):
                delivery_data = {
                    "team": team,
                    "over": over_number,
                    "batter": delivery.get("batter"),
                    "bowler": delivery.get("bowler"),
                    "non_striker": delivery.get("non_striker"),
                    "runs_batter": delivery.get("runs", {}).get("batter", 0),
                    "runs_extras": delivery.get("runs", {}).get("extras", 0),
                    "runs_total": delivery.get("runs", {}).get("total", 0),
                    "wicket": delivery.get("wickets", [{}])[0].get("player_out", "None") if "wickets" in delivery else "None"
                }
                innings_data.append({**match_details, **delivery_data})

    return pd.DataFrame(innings_data)

all_data = []
for filename in os.listdir(json_folder_path):
    if filename.endswith(".json"):  
        file_path = os.path.join(json_folder_path, filename)
        df = process_json_file(file_path)
        all_data.append(df)

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(csv_output_path, index=False)
    print(f"Data saved to {csv_output_path}")
else:
    print("No JSON files found in the specified directory.")

# Cricsheet Match Data Analysis  

## Overview  
This project is a **Cricket Match Data Analysis** application built using **Python, MySQL, and Power BI**. It processes cricket match data from **Cricsheet**, stores it in a structured SQL database, performs **exploratory data analysis (EDA)**, and generates insights through **SQL queries and Power BI dashboards**.  

## Features  

- **Database Creation**: Automatically structures an SQL database with tables for **ODI, Test, T20, and IPL matches**.  
- **JSON Data Processing**: Reads and transforms raw JSON files into structured **DataFrames using Pandas**.  
- **SQL Queries for Insights**: Includes **20 SQL queries** to analyze:  
  - Top batsmen by total runs.  
  - Leading wicket-takers in T20s.  
  - Win percentage of teams across formats.  
  - Centuries scored across all matches.  
- **Exploratory Data Analysis (EDA)**:  
  - **10+ visualizations** using **Matplotlib, Seaborn, and Plotly**.  
  - Graphical representation of player and team performance.  
- **Power BI Dashboard**:  
  - Interactive reports on player statistics, team performance, and match outcomes.  
  - Visual storytelling of cricket data trends.  

## Technologies Used  

- **Python** (for data processing and EDA)  
- **MySQL / SQLite** (for database management)  
- **Pandas** (for data transformation)  
- **Matplotlib, Seaborn, Plotly** (for data visualization)  
- **Power BI** (for interactive dashboards)  
- **SQLAlchemy** (for database connectivity)  

## Prerequisites  

Ensure you have the following installed:  
- Python (>=3.x)  
- MySQL Server or SQLite  
- Power BI (for dashboard visualization)  
- Required Python libraries (`pip install -r requirements.txt`)  

## Usage  

1. **Load and Transform Data**  
   - Parse JSON match files and convert them into structured **Pandas DataFrames**.  
   - Save the structured data into an **SQL database**.  

2. **Run SQL Queries for Insights**  
   - Execute **queries.sql** to analyze match statistics.  

3. **Perform EDA using Python**  
   - Run `eda.py` to generate **visualizations and statistical insights**.  

4. **Analyze Data in Power BI**  
   - Connect Power BI to the SQL database.  
   - Open `powerbi_dashboard.pbix` to explore interactive reports.  

## Database Schema  

The database consists of **four main tables**, each representing a cricket match format:  

### **ODI_Matches Table**  
- Match type
- Season
- City
- Venue  
- Toss Winner & Decision  
- Match Winner
- Player of the Match
- Teams Batter Bowler
- Runs, Wickets, Overs  

### **Test_Matches Table**  
- Match type
- Season
- City
- Venue  
- Toss Winner & Decision  
- Match Winner
- Player of the Match
- Teams Batter Bowler
- Runs, Wickets, Overs   

### **T20_Matches Table**  
- Match type
- Season
- City
- Venue  
- Toss Winner & Decision  
- Match Winner
- Player of the Match
- Teams Batter Bowler
- Runs, Wickets, Overs  

### **IPL_Matches Table**  
- Match type
- Season
- City
- Venue  
- Toss Winner & Decision  
- Match Winner
- Player of the Match
- Teams Batter Bowler
- Runs, Wickets, Overs  

## Contribution  
Feel free to contribute by forking the repository and submitting pull requests.  

## License  
This project is licensed under the **MIT License**.  

## Author  
**Your Name**  
GitHub: Ramadevi N

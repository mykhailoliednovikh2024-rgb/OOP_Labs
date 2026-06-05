import pandas as pd
import sqlite3
conn = sqlite3.connect('Job opportunities.db') 
cursor = conn.cursor()
#1
df = pd.read_csv('Job opportunities.csv')
print(df.head())
df.to_sql('Job opportunities.csv', conn, if_exists='replace', index=False)
#2
query=("SELECT * FROM 'Job opportunities.csv'  LIMIT 10")
result=pd.read_sql(query,conn)
print(result)
#3
query=("SELECT * FROM 'Job opportunities.csv' WHERE \"Required Skills\" LIKE '%SQL%'")
result1=pd.read_sql(query, conn)
print(result1)
query=("SELECT DISTINCT Location FROM 'Job opportunities.csv'")
result2=pd.read_sql(query, conn)
query=("SELECT DISTINCT Company FROM 'Job opportunities.csv'")
result3=pd.read_sql(query, conn)
print(result2,result3)
#4

query = (
    "SELECT Industry, AVG(CAST(REPLACE(SUBSTR(\"Salary Range\", 2), ',', '') AS INTEGER)) "
    "as avg_salary FROM 'Job opportunities.csv' GROUP BY Industry"
)
result4 = pd.read_sql(query, conn)
print(result4)
query= (
    "SELECT Industry, COUNT(*) as vacancy_count FROM 'Job opportunities.csv' "
    "WHERE CAST(REPLACE(SUBSTR(\"Salary Range\", 2), ',', '') AS INTEGER) > 50000 "
    "GROUP BY Industry"
)
result5=pd.read_sql(query,conn)
print(result5)
#5
query= (
    "SELECT Location, COUNT(*) as loc_count FROM 'Job opportunities.csv' "
    "GROUP BY Location"
)
result6=pd.read_sql(query, conn)
print(result6)
query= (
    "SELECT \"Experience Level\", COUNT(*) as exp_count FROM 'Job opportunities.csv' "
    "GROUP BY \"Experience Level\""
)
result7=pd.read_sql(query,conn)
print(result7)
query=(
    "SELECT Industry, COUNT(*) as ind_count FROM 'Job opportunities.csv' "
    "GROUP BY Industry"
)
result8=pd.read_sql(query, conn)
print(result8)
query=(
    "SELECT \"Job Type\", COUNT(*) as jobtp_count FROM 'Job opportunities.csv' "
    "GROUP BY \"Job Type\""
)
result9=pd.read_sql(query, conn)
print(result9)
query = (
    "SELECT Industry, AVG(CAST(REPLACE(SUBSTR(\"Salary Range\", 2), ',', '') AS INTEGER)) "
    "as vac_salary FROM 'Job opportunities.csv'"
    "GROUP BY Location , \"Experience Level\""
)
result10 = pd.read_sql(query, conn)
print(result10)
#6
query =(
    """
SELECT *, 
       CAST(REPLACE(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 2), '£', ''), ',', '') AS INTEGER) as max_salary
FROM 'Job opportunities.csv'
ORDER BY max_salary DESC
LIMIT 5
""")
result11 = pd.read_sql(query, conn)
print(result11)
query=(
    "SELECT \"Required Skills\", COUNT (\"Required Skills\") as vac_skills FROM 'Job opportunities.csv' "
   " GROUP BY  \"Required Skills\" "
       
)
result12=pd.read_sql(query, conn)
print(result12)
query=(
    "SELECT Company, COUNT (\"Job Title\") as company_vac FROM 'Job opportunities.csv' "
    " GROUP BY Company "
    "ORDER BY company_vac DESC "
    "LIMIT 10"
)
result13=pd.read_sql(query, conn)
print(result13)
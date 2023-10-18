
#Goal 1: Report the number of tasks that are overdue
import pandas as pd
file_path = 'Construction_Data_PM_Tasks_All_Projects.csv'
column_name = 'OverDue'
df = pd.read_csv(file_path)
true_count = (df[column_name] == True).sum()
print(f"Number of 'TRUE' entries in '{column_name}': {true_count}")

#Goal 2: Report the total number of open and closed tasks by task group
grouped_data = df.groupby(['Task Group', 'Report Status']).size().unstack(fill_value=0)
print(grouped_data)

#Goal 3: Plot the total number of open and closed tasks by task group in a bar chart
import matplotlib.pyplot as plt
ax = grouped_data.plot(kind='bar', stacked=True)
plt.xlabel('Task Group')
plt.ylabel('Count')
plt.title('Counts of Open and Closed Items by Task Group')
plt.legend(title='Report Status')
plt.tight_layout()
plt.xticks(rotation=0)
plt.savefig('bar_chart.png', dpi=300)
print("The bar chart is saved as 'bar_chart.png'")

#Goal 4: Plot the total number of overdue tasks by project in a bar chart
project_overdue_counts = df[df['OverDue'] == True].groupby('project')['OverDue'].count()
plt.figure(figsize=(12, 6))
project_overdue_counts.plot(kind='bar', color='blue')
plt.xlabel('Project')
plt.ylabel('Number of Overdue Tasks')
plt.title('Number of Overdue Tasks by Project Number')
plt.xticks(rotation=0)
plt.savefig('project_overdue_bar_chart.png', dpi=300)  

#Goal 5: Create a bar chart of the percentage of overdue tasks by project
total_true_count = (df['OverDue'] == True).sum()
project_percentages = (project_overdue_counts / total_true_count) * 100
plt.figure(figsize=(12, 6))
ax = project_percentages.plot(kind='bar', color='green')
plt.xlabel('Project')
plt.ylabel('Percentage of Overdue Tasks')
plt.title('Percentage of Overdue Tasks by Project')
plt.xticks(rotation=0)
plt.savefig('project_overdue_percentage_bar_chart.png', dpi=300) 

#Goal 6: Mean number of days elapsed since 10/17/2023 from when form was created by project:
import datetime
file_path2 = 'Construction_Data_PM_Forms_All_Projects.csv'
df2 = pd.read_csv(file_path2)
df2['Created'] = pd.to_datetime(df['Created'], format='%d/%m/%Y')
target_date = pd.Timestamp(datetime.date(2023, 10, 17))
df2['DaysPassed'] = (target_date - df2['Created']).dt.days
project_mean_days = df2.groupby('Project')['DaysPassed'].mean()
print(project_mean_days)

#Goal 7: Create a bar chart for the number of open forms by type of form:
open_forms = df2[df2['Report Forms Status'] == 'Open']
open_forms_by_type = open_forms.groupby('Type')['Report Forms Status'].count()
plt.figure(figsize=(18, 6)) 
open_forms_by_type.plot(kind='bar', color='blue')
plt.xlabel('Type')
plt.ylabel('Number of Open Forms')
plt.title('Number of Open Forms by Type of Form')
plt.xticks(rotation=0)
plt.xticks(fontsize=6)
plt.savefig('open_forms_by_type.png', dpi=300)

#Goal 8: Create a time series plot of the number of currently open forms by Report Form Group:
df2['Created'] = pd.to_datetime(df['Created'], format='%d/%m/%Y')
open_forms_by_group = open_forms.groupby(['Report Forms Group', 'Created'])['Report Forms Status'].count()
open_forms_by_group = open_forms_by_group.reset_index()
plt.figure(figsize=(12, 6)) 
for group, data in open_forms_by_group.groupby('Report Forms Group'):
    plt.plot(data['Created'], data['Report Forms Status'], label=group)
plt.xlabel('Date')
plt.ylabel('Number of Open Forms')
plt.title('Time Series of Open Forms by Report Form Group')
plt.legend()
plt.savefig('open_forms_time_series.png', dpi=300)

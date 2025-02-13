import streamlit as st
import pandas as pd

# Define the JobSite class
class JobSite:
    def __init__(self, site_id, people_needed):
        self.site_id = site_id
        self.people_needed = people_needed
        self.assigned_groups = []

# Define the Group class
class Group:
    def __init__(self, group_name, num_people):
        self.group_name = group_name
        self.num_people = num_people
        self.membership = set(range(num_people))  # Track individual members

def upload_file():
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  # Changed to read CSV
        
        job_sites = []
        groups = []
        
        for index, row in df.iterrows():
            job_site_id = row['Job Site ID']
            people_needed = row['People Needed']
            
            job_sites.append({'site_id': job_site_id, 'people_needed': people_needed})
            
            group_name = row['Group Name']
            group_people = row['Number of People']
            
            groups.append({'group_name': group_name, 'number_of_people': group_people})
    
        return job_sites, groups
    else:
        return None, None

def main():
    st.title("Job Site Group Matching")
    
    job_sites_data, groups_data = upload_file()
    
    if job_sites_data and groups_data:
        st.subheader("Preview of Uploaded Data")
        st.write("Job Sites:")
        job_sites_df = pd.DataFrame(job_sites_data)
        st.dataframe(job_sites_df)
        
        st.write("Groups:")
        groups_df = pd.DataFrame(groups_data)
        st.dataframe(groups_df)
        
        # Convert data to objects
        job_sites = []
        for js in job_sites_data:
            job_sites.append(JobSite(js['site_id'], js['people_needed']))
        
        # Convert group data to Group objects
        group_objects = []
        for group in groups_data:
            group_objects.append(Group(group['group_name'], group['number_of_people']))
        
        # Perform matching
        assignments = []
        for job_site in job_sites:
            remaining_capacity = job_site.people_needed
            for group in group_objects:
                assign_count = min(group.num_people, remaining_capacity)
                if assign_count > 0:
                    assignments.append({
                        'Job Site ID': job_site.site_id,
                        'Group Name': group.group_name,
                        'Number of People Assigned': assign_count
                    })
                    remaining_capacity -= assign_count
        
        # Display results
        st.subheader("Assignments")
        if len(assignments) > 0:
            assignments_df = pd.DataFrame(assignments)
            st.dataframe(assignments_df)
        else:
            st.write("No assignments to display.")

if __name__ == "__main__":
    main()

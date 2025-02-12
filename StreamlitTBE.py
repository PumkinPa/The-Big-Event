import streamlit as st
import pandas as pd
from openpyxl import load_workbook

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
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        job_sites = []
        groups = []
        
        for index, row in df.iterrows():
            job_site_id = row['Job Site ID']
            people_needed = row['People Needed']
            group_name = row['Group Name']
            group_size = row['Number of People in Group']
            
            job_sites.append(JobSite(job_site_id=job_site_id, people_needed=people_needed))
            groups.append(Group(group_name=group_name, num_people=group_size))
        
        return job_sites, groups
    else:
        st.error("Please upload a file first!")
        return None, None

def match_groups_to_sites(job_sites, groups):
    assignments = []
    
    for site in job_sites:
        for group in groups:
            if len(group.membership) == 0:
                continue
                
            # Try to fit as much of the group into this job site
            max_possible = min(len(group.membership), site.people_needed)
            
            if max_possible > 0:
                new_assignment = {
                    'group_name': f"{group.group_name}{' (split)' if max_possible < len(group.membership) else ''}",
                    'site_id': site.site_id,
                    'num_people': max_possible
                }
                
                assignments.append(new_assignment)
                group.membership -= set(range(max_possible))  # Fixed the remove_members issue
                
    return assignments

def main():
    st.title("Job Site Group Matching")
    
    job_sites, groups = upload_file()
    
    if job_sites and groups:
        st.subheader("Preview of Uploaded Data")
        st.write("Job Sites:")
        st.dataframe(pd.DataFrame([[js.site_id, js.people_needed] for js in job_sites], 
                            columns=['Job Site ID', 'People Needed']))
        
        st.write("Groups:")
        st.dataframe(pd.DataFrame([[g.group_name, g.num_people] for g in groups],
                            columns=['Group Name', 'Number of People']))
        
        st.subheader("Matching Process")
        assignments = match_groups_to_sites(job_sites, groups)
        
        st.subheader("Assignment Results")
        result_df = pd.DataFrame(assignments)
        st.dataframe(result_df)

if __name__ == "__main__":
    main()

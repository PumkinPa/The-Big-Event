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
        df = pd.read_csv(uploaded_file)
        
        job_sites_data = []
        groups_data = []
        
        for index, row in df.iterrows():
            # Add Job Site data
            job_sites_data.append({
                'site_id': row['Job site ID'],
                'people_needed': row['People Needed']
            })
            
            # Add Group data
            groups_data.append({
                'group_name': row['Group Name'],
                'number_of_people': row['Number of people in group']
            })
    
        return job_sites_data, groups_data
    else:
        return None, None

def main():
    st.title("Job Site Group Matching")
    
    job_sites_data, groups_data = upload_file()
    
    if job_sites_data and groups_data:
        # Convert data to objects
        job_sites = []
        for js in job_sites_data:
            job_sites.append(JobSite(js['site_id'], js['people_needed']))
        
        # Create Group objects
        groups = []
        for group_dict in groups_data:
            groups.append(Group(
                group_dict['group_name'],
                group_dict['number_of_people']
            ))
        
        # List to hold the final assignments (dictionary of job sites with their assigned groups)
        all_assignments = {}
        
        # Create a list of remaining job sites
        remaining_job_sites = job_sites.copy()
        
        # Process each group and assign them to fill job sites in order
        for group in groups:
            current_people = group.num_people
            group_name = group.group_name
            
            while current_people > 0 and len(remaining_job_sites) > 0:
                # Get the first remaining job site
                current_site = remaining_job_sites[0]
                
                # Calculate how many people can be assigned to this site
                assign_amount = min(current_people, current_site.people_needed)
                
                if assign_amount > 0:
                    # Record the assignment
                    if current_site.site_id not in all_assignments:
                        all_assignments[current_site.site_id] = []
                    all_assignments[current_site.site_id].append({
                        'group': group_name,
                        'people_assigned': assign_amount
                    })
                    
                    # Update remaining people in the group
                    current_people -= assign_amount
                    
                    # Check if this job site is fully filled
                    current_site.people_needed -= assign_amount
                    if current_site.people_needed == 0:
                        # Remove the fully filled job site from remaining sites
                        remaining_job_sites.pop(0)
        
        # Display the assignments in a tabular format
        st.write("### Final Assignments")
        
        # Create lists to store assignment data
        table_data = []
        headers = ['Job Site ID', 'Group Name', 'People Assigned']
        
        for site_id, assignments in all_assignments.items():
            for a in assignments:
                table_data.append([
                    site_id,
                    a['group'],
                    a['people_assigned']
                ])
        
        # Create DataFrame and display
        if len(table_data) > 0:
            df = pd.DataFrame(table_data, columns=headers)
            st.table(df)
        else:
            st.write("No assignments were made.")

if __name__ == "__main__":
    main()

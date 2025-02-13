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
        
        for _, row in df.iterrows():
            job_sites_data.append({'site_id': row['Job site ID'], 'people_needed': row['People Needed']})
            groups_data.append({'group_name': row['Group Name'], 'number_of_people': row['Number of people in group']})
    
        return job_sites_data, groups_data
    return None, None

def main():

    with st.sidebar:
        st.logo("https://se-images.campuslabs.com/clink/images/e26c4fde-15c3-47fd-8397-32bb6365d558c47c3d2e-bc6e-4b8b-af51-75e9022b7440.png?preset=med-sq") 
        st.write("If anything needs to be fixed just have Claire tell me.")
    st.title("TBE Job Site Group Matching")
    
    job_sites_data, groups_data = upload_file()
    
    if job_sites_data and groups_data:
        job_sites = [JobSite(js['site_id'], js['people_needed']) for js in job_sites_data]
        groups = [Group(group_dict['group_name'], group_dict['number_of_people']) for group_dict in groups_data]
        
        all_assignments = []
        remaining_job_sites = job_sites.copy()
        
        for group in groups:
            current_people = group.num_people
            group_name = group.group_name
            
            while current_people > 0 and remaining_job_sites:
                site_assigned = None
                
                for i, site in enumerate(remaining_job_sites):
                    if site.people_needed == current_people:
                        site_assigned = i
                        break
                
                if site_assigned is not None:
                    site = remaining_job_sites.pop(site_assigned)
                    all_assignments.append([site.site_id, group_name, site.people_needed])
                    current_people = 0  
                else:
                    for i, site in enumerate(remaining_job_sites):
                        if current_people >= site.people_needed:
                            assigned = site.people_needed
                            all_assignments.append([site.site_id, group_name, assigned])
                            current_people -= assigned
                            remaining_job_sites.pop(i)
                            break
                    else:
                        break
        
        assignment_df = pd.DataFrame(all_assignments, columns=["Job Site ID", "Group Name", "People Assigned"])
        st.write("### Assignment Results:")
        st.dataframe(assignment_df)
        
        remaining_sites = [site.site_id for site in remaining_job_sites]
        if remaining_sites:
            st.warning(f"Warning: The following job sites are still unfilled: {', '.join(map(str, remaining_sites))}")

if __name__ == "__main__":
    main()

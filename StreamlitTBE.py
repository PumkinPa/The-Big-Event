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
            
            while True:
                site_assigned = None
                # First, try to find a perfect match
                for i, site in enumerate(remaining_job_sites):
                    if site.people_needed == current_people:
                        site_assigned = i
                        break
                
                if site_assigned is not None:
                    # Assign the entire group to this site
                    site = remaining_job_sites.pop(site_assigned)
                    all_assignments[site.site_id] = [group_name]
                    current_people -= site.people_needed  # Remove the assigned people from the group's count
                    if current_people <= 0:
                        break  # No more people left in the group
                else:
                    # If no perfect match found, proceed to assign remaining people partially
                    for i, site in enumerate(remaining_job_sites):
                        if current_people >= site.people_needed:
                            # Assign as much as needed from this group
                            assigned = site.people_needed
                            all_assignments.setdefault(site.site_id, []).append((group_name, assigned))
                            current_people -= assigned
                            # Remove the site if it's fully filled
                            if current_people <= 0:
                                break
                    break
        
        # Display results
        st.write("### Assignment Results:")
        for site_id, assignments in all_assignments.items():
            st.write(f"Site {site_id}:")
            for group_assignment in assignments:
                if isinstance(group_assignment, tuple):
                    group_name, num_assigned = group_assignment
                    st.write(f"- {group_name} assigned: {num_assigned}")
                else:
                    st.write(f"- {group_assignment} (full group)")
        
        # Check if any groups were partially assigned
        groups_used = set()
        for assignments in all_assignments.values():
            for a in assignments:
                if isinstance(a, tuple):
                    groups_used.add(a[0])
        partial_groups = [g.group_name for g in groups if g.group_name in groups_used]
        
        # Check if any job sites are still unfilled
        remaining_sites = [site.site_id for site in remaining_job_sites]
        if remaining_sites:
            st.write(f"### Warning: Sites {', '.join(remaining_sites)} are still unfilled.")

if __name__ == "__main__":
    main()

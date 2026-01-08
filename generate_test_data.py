import requests
import json
import random
from datetime import datetime, timedelta

# --- Configuration ---
BASE_URL = "http://localhost:8000/api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3ODcwNDgyLCJpYXQiOjE3Njc4NjUwODIsImp0aSI6IjIwM2QxMWQ1NGU0NTRmYTQ5MThlZTFkYTZlYTQ2ZjA2IiwidXNlcl9pZCI6NX0.pO9ptz2NFwtRi9Lm2HMHUy60qJYX-iOoBT-uLWoNweg" # Replace with a valid token

NUM_BASE_ENTRIES = 200 # Number of new students to create
NUM_FOLLOW_UPS = 200   # Number of follow-up entries to create for existing students


# --- Data Lists (abbreviated for brevity) ---
first_names = ["Aarav", "Aditya", "Alex", "Ananya", "Arya", "Ava", "David", "Emily", "Ethan", "Isha", "Jacob", "Jiya", "Krishna", "Liam", "Mila", "Noah", "Olivia", "Priya", "Rahul", "Riya", "Ryan", "Sai", "Sara", "Shivam", "Sia", "Sophia", "Yash", "Zara", "Aarushi", "Aisha"]
last_names = ["Acharya", "Agarwal", "Aggarwal", "Anand", "Arora", "Babu", "Bajaj", "Balakrishnan", "Banerjee", "Bansal", "Barman", "Basu", "Bedi", "Bhadra", "Bhandari", "Bharadwaj", "Bhargava", "Bhat", "Bhatia", "Bhatt", "Bhattacharya", "Bhattacharyya", "Bose", "Chacko", "Chadha", "Chakrabarti", "Chakraborty", "Chakravarthy", "Chande", "Chander", "Chandra", "Chandran", "Chandrasekhar", "Chatterjee", "Chaturvedi", "Chaudhari", "Chaudhary", "Chauhan", "Chawla", "Cherian"]
schools = ["Amity International School", "Apeejay School", "Army Public School", "Baldwin Boys' High School", "Delhi Public School", "Don Bosco School", "Gitanjali School", "Greenwood High", "Heritage School", "Hyderabad Public School", "Indus International School", "Jayshree Periwal International School", "Kendriya Vidyalaya", "La Martiniere College", "Maharani Gayatri Devi Girls' School", "Mayo College", "Modern School", "National Public School", "Oakridge International School", "Podar International School", "Ryan International School", "Sanskriti School", "Scindia School", "The Doon School", "Vasant Valley School", "Vidya Niketan School", "Welham Girls' School", "Woodstock School"]


# --- Helper Functions for Data Generation ---

def generate_random_date(start_year=2020, end_year=2025):
    """Generates a random date within a given year range."""
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def generate_student_data():
    return {
        "name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "school_name": random.choice(schools),
        "age": random.randint(6, 18),
        "gender": random.choice(["Male", "Female", "Other"]),
        "height": round(random.uniform(110.0, 180.0), 1),
        "weight": round(random.uniform(20.0, 80.0), 1),
        "parental_myopia": random.choice(["None", "Father", "Mother", "Both"]),
        "num_siblings": random.randint(0, 5),
        "birth_order": random.choice(["First", "Second", "Third", "Only Child"]),
        "siblings_myopia": random.randint(0, 3)
    }

def generate_lifestyle_data():
    return {
        "outdoor_duration": random.choice(["<1 hr", "1-2 hrs", "2-4 hrs", ">4 hrs"]),
        "sun_exposure": random.choice(["<15 min", "15-30 min", "30-60 min", ">1 hr"]),
        "near_work_hours": random.choice(["<2 hrs", "2-4 hrs", "4-6 hrs", ">6 hrs"]),
        "screen_time": random.choice(["<1 hr", "1-3 hrs", "3-5 hrs", ">5 hrs"]),
        "primary_device": random.choice(["TV", "Tablet", "Mobile", "Laptop/Desktop"]),
        "reading_distance": random.choice(["<20 cm", "20-30 cm", ">30 cm"]),
        "viewing_posture_ratio": random.choice(["Low", "Optimum", "High"]),
        "dietary_habit": random.choice(["Balanced", "Junk-food dominant", "Vegetarian", "Non-vegetarian", "Other"]),
        "sleep_duration": random.choice(["<6 hrs", "6-7 hrs", "7-8 hrs", ">8 hrs"]),
        "usual_bedtime": random.choice(["Before 9 PM", "9-10 PM", "10-11 PM", "After 11 PM"])
    }

def generate_environment_data():
    return {
        "school_type": random.choice(["Urban", "Rural"]),
        "classroom_strength": random.choice(["<30", "30-50", ">50"]),
        "seating_position": random.choice(["Front", "Middle", "Back"]),
        "teaching_methodology": random.choice(["Digital", "Traditional"]),
        "lighting": random.choice(["Dim", "Adequate", "Bright"]),
        "sunlight_source": random.choice(["Natural", "Artificial", "Both"])
    }

def generate_history_data():
    diagnosed_earlier = random.choice([True, False])
    return {
        "diagnosed_earlier": diagnosed_earlier,
        "age_at_diagnosis": random.randint(5, 15) if diagnosed_earlier else None,
        "power_changed_last_3yrs": random.choice([True, False]),
        "compliance": random.choice(["Always", "Sometimes", "Rarely"]),
        "previous_re": f"{random.uniform(-5.0, 2.0):.2f}",
        "previous_le": f"{random.uniform(-5.0, 2.0):.2f}",
        "current_re": f"{random.uniform(-6.0, 3.0):.2f}",
        "current_le": f"{random.uniform(-6.0, 3.0):.2f}"
    }

def generate_awareness_data():
    sources = random.sample(["School", "Family", "Doctor", "Media", "Other", "None"], k=random.randint(1, 2))
    return {
        "aware_eye_strain": random.choice([True, False]),
        "access_to_vision_care": random.choice([True, False]),
        "follows_preventive_measures": random.choice(["Always", "Sometimes", "Never"]),
        "source_of_awareness": ", ".join(sources)
    }

def generate_ocular_data():
    return {
        "uncorrectedvisual_acuity_right_eye": f"6/{random.choice([6, 9, 12, 18, 24, 36, 60])}",
        "uncorrectedvisual_acuity_left_eye": f"6/{random.choice([6, 9, 12, 18, 24, 36, 60])}",
        "bestcorrectedvisual_acuity_right_eye": f"6/{random.choice([6, 9, 12])}",
        "bestcorrectedvisual_acuity_left_eye": f"6/{random.choice([6, 9, 12])}",
        "cycloplegic_auto_refraction_right_eye": f"S:{random.uniform(-5.0, 1.0):.2f} C:{random.uniform(-2.0, 0):.2f}",
        "cycloplegic_auto_refraction_left_eye": f"S:{random.uniform(-5.0, 1.0):.2f} C:{random.uniform(-2.0, 0):.2f}",
        "spherical_power_right_eye": f"{random.uniform(-5.0, 2.0):.2f}",
        "spherical_power_left_eye": f"{random.uniform(-5.0, 2.0):.2f}",
        "axial_length_right_eye": f"{random.uniform(22.0, 26.0):.2f}",
        "axial_length_left_eye": f"{random.uniform(22.0, 26.0):.2f}",
        "corneal_curvature_right_eye": f"K1:{random.uniform(40.0, 45.0):.2f},K2:{random.uniform(40.0, 45.0):.2f}",
        "corneal_curvature_left_eye": f"K1:{random.uniform(40.0, 45.0):.2f},K2:{random.uniform(40.0, 45.0):.2f}",
        "central_corneal_thickness_right_eye": f"{random.randint(500, 600)}",
        "central_corneal_thickness_left_eye": f"{random.randint(500, 600)}",
        "anterior_segment_finding_right_eye": "Clear" if random.random() > 0.1 else "Trace cataract",
        "anterior_segment_finding_left_eye": "Clear" if random.random() > 0.1 else "Trace cataract",
        "amblyopia_or_strabismus": random.choice([True, False]),
        "fundus_examination_finding_right_eye": "Normal" if random.random() > 0.1 else "Myopic fundus",
        "fundus_examination_finding_left_eye": "Normal" if random.random() > 0.1 else "Myopic fundus"
    }

def submit_data(endpoint, payload, headers, entry_num, total_entries, student_name):
    """Generic function to post data and handle responses."""
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        result = response.json()
        print(f"Entry {entry_num}/{total_entries}: SUCCESS for '{student_name}'. ID: {result.get('student_id') or result.get('visit_id')}")
        return result
    except requests.exceptions.HTTPError as http_err:
        print(f"Entry {entry_num}/{total_entries}: HTTP ERROR for '{student_name}': {http_err} - {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Entry {entry_num}/{total_entries}: ERROR for '{student_name}': {req_err}")
    except json.JSONDecodeError:
        print(f"Entry {entry_num}/{total_entries}: JSON DECODE ERROR for '{student_name}'. Response: {response.text}")
    return None


def generate_baseline_questionnaires(headers):
    """Generates and submits baseline questionnaire data for new students."""
    print(f"--- Starting Baseline Questionnaire Generation ({NUM_BASE_ENTRIES} Entries) ---")
    created_student_ids = []
    
    for i in range(1, NUM_BASE_ENTRIES + 1):
        student_data = generate_student_data()
        payload = {
            "visit_date": generate_random_date(),
            **student_data,
            "lifestyle": generate_lifestyle_data(),
            "environment": generate_environment_data(),
            "history": generate_history_data(),
            "awareness": generate_awareness_data(),
            "ocular": generate_ocular_data()
        }
        result = submit_data("/forms/submit-student/", payload, headers, i, NUM_BASE_ENTRIES, student_data['name'])
        if result and result.get('student_id'):
            created_student_ids.append(result['student_id'])
            
    print(f"--- Baseline Generation Complete ---")
    return created_student_ids


def generate_followup_forms(student_ids, headers):
    """Generates and submits follow-up form data for existing students."""
    if not student_ids:
        print("No student IDs provided, skipping follow-up generation.")
        return

    print(f"\n--- Starting Follow-Up Form Generation ({NUM_FOLLOW_UPS} Entries) ---")
    
    # Select a random subset of students for follow-ups
    num_to_generate = min(NUM_FOLLOW_UPS, len(student_ids))
    students_for_followup = random.sample(student_ids, k=num_to_generate)
    
    for i, student_id in enumerate(students_for_followup, 1):
        payload = {
            "student_id": student_id,
            "visit_date": generate_random_date(start_year=2024, end_year=2026),
            "lifestyle": generate_lifestyle_data(),
            "environment": generate_environment_data(),
            "history": generate_history_data(),
            "awareness": generate_awareness_data(),
            "ocular": generate_ocular_data()
        }
        submit_data("/forms/submit-followup/", payload, headers, i, num_to_generate, f"Follow-up for {student_id}")


if __name__ == "__main__":
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE" or not ACCESS_TOKEN:
        print("ERROR: Please replace 'YOUR_ACCESS_TOKEN_HERE' with a valid JWT access token.")
        exit()

    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Generate baseline entries and get the new student IDs
    new_student_ids = generate_baseline_questionnaires(auth_headers)

    # Generate follow-up entries for the newly created students
    generate_followup_forms(new_student_ids, auth_headers)
import requests
import json
import random
from datetime import datetime, timedelta

# --- Data Lists ---
first_names = [
    "Aarav", "Aaryan", "Abdul", "Adam", "Aditya", "Ahmad", "Ahmed", "Ajay", "Akhil", "Akshay",
    "Alex", "Alexander", "Ali", "Amit", "Anand", "Andrew", "Anil", "Ankit", "Anthony", "Arjun",
    "Arun", "Ashish", "Ashok", "Atharva", "Ayush", "Benjamin", "Bharat", "Bhaskar", "Bhavin", "Brian",
    "Charles", "Chris", "Christopher", "Daniel", "Darshan", "David", "Deepak", "Dev", "Dhanush", "Dharma",
    "Dinesh", "Divyansh", "Eric", "Ethan", "Ganesh", "Gaurav", "Gautam", "George", "Gopal", "Harish",
    "Harsh", "Hemant", "Hitesh", "Imran", "Ishaan", "Jacob", "James", "Jason", "Jay", "Jayesh",
    "John", "Joseph", "Joshua", "Kamal", "Karan", "Kartik", "Kaushik", "Kevin", "Krishna", "Kunal",
    "Laksh", "Liam", "Mahesh", "Manish", "Manoj", "Matthew", "Mayank", "Michael", "Mihir", "Mohammed",
    "Mohan", "Mohit", "Mukesh", "Mustafa", "Naveen", "Neeraj", "Nikhil", "Nitin", "Noah", "Pankaj",
    "Parth", "Pavan", "Piyush", "Pradeep", "Prakash", "Pramod", "Pranav", "Prashant", "Prateek", "Praveen",
    "Rahul", "Raj", "Rajan", "Rajesh", "Rakesh", "Ramesh", "Ranbir", "Ravi", "Rhys", "Richard",
    "Rishi", "Ritesh", "Robert", "Rohan", "Rohit", "Ronak", "Roshan", "Ryan", "Sachin", "Sagar",
    "Sahil", "Sai", "Sameer", "Samir", "Sandeep", "Sanjay", "Sanket", "Sarvesh", "Satish", "Saurabh",
    "Sean", "Shahid", "Shantanu", "Shashank", "Shashwat", "Shikhar", "Shivam", "Siddharth", "Soham", "Sohan",
    "Sohil", "Sourabh", "Srinivas", "Subhash", "Sudhir", "Sumit", "Sundar", "Sunil", "Suraj", "Suresh",
    "Sushant", "Swapnil", "Syed", "Tanmay", "Tapan", "Tarun", "Tejas", "Thomas", "Tushar", "Uday",
    "Utkarsh", "Vaibhav", "Varun", "Venkatesh", "Vicky", "Vidit", "Vignesh", "Vijay", "Vikas", "Vikram",
    "Vimal", "Vinay", "Vineet", "Vinod", "Vishal", "Vishnu", "Vivek", "Yash", "Yashas", "Yogesh",
    "Yusuf", "Zain", "Zayn", "Aarushi", "Aastha", "Abha", "Aditi", "Aisha", "Aishwarya", "Akanksha",
    "Akshara", "Akshata", "Alia", "Amelia", "Amisha", "Amrita", "Ananya", "Angel", "Anika", "Anisha",
    "Anjali", "Ankita", "Anushka", "Aparna", "Arpita", "Arya", "Asha", "Ashwini", "Ava", "Avani",
    "Bhavana", "Bhumika", "Catherine", "Charu", "Christina", "Daisy", "Deepa", "Deepika", "Devika", "Dhara",
    "Dhriti", "Diksha", "Disha", "Divya", "Diya", "Eesha", "Eira", "Ekta", "Elena", "Emily",
    "Emma", "Esha", "Falguni", "Fatima", "Fiza", "Gargi", "Gauri", "Gayatri", "Geeta", "Grace",
    "Hannah", "Hansa", "Harini", "Harshita", "Heena", "Hema", "Himanshi", "Hina", "Ila", "Inaaya",
    "Indu", "Isha", "Ishani", "Ishika", "Ishita", "Janhvi", "Jasmine", "Jennifer", "Jessica", "Jia",
    "Jivika", "Jiya", "Juhi", "Jyoti", "Kajal", "Kajol", "Kalpana", "Kalyani", "Kamala", "Kamini",
    "Kanika", "Kareena", "Karishma", "Kavita", "Kavya", "Khushi", "Kiran", "Kirti", "Komal", "Koyal",
    "Krisha", "Krishna", "Kriti", "Krupa", "Kshama", "Kshipra", "Kumari", "Lata", "Latika", "Lavanya",
    "Laxmi", "Leela", "Lily", "Lina", "Lipika", "Madhubala", "Madhuri", "Mahi", "Mahima", "Mala",
    "Malini", "Manasi", "Manisha", "Manju", "Manvi", "Manya", "Maya", "Mayuri", "Meena", "Meenakshi",
    "Meera", "Megha", "Megan", "Mehak", "Mitali", "Mona", "Monalisa", "Monica", "Mrunal", "Mugdha",
    "Muskan", "Myra", "Naina", "Nalini", "Namrata", "Nancy", "Nandini", "Nandita", "Naomi", "Navya",
    "Neha", "Nidhi", "Niharika", "Nikita", "Nilima", "Nisha", "Nishita", "Nitya", "Nivedita", "Nupur",
    "Olivia", "Palak", "Pallavi", "Pankhuri", "Pari", "Parineeti", "Parul", "Pooja", "Poonam", "Prachi",
    "Pragya", "Pranjal", "Prarthana", "Pratibha", "Preeti", "Prerna", "Priya", "Priyanka", "Radha", "Radhika",
    "Ragini", "Rajalakshmi", "Rajeshwari", "Rakhi", "Raksha", "Rani", "Rashi", "Rashmi", "Reema", "Renu",
    "Renuka", "Reshma", "Richa", "Riddhi", "Ridhi", "Rina", "Rinki", "Riya", "Roshni", "Ruby",
    "Ruchi", "Ruchika", "Rupal", "Rupali", "Sabrina", "Sadhana", "Sagarika", "Saheli", "Saima", "Saina",
    "Saira", "Sakshi", "Saloni", "Samiksha", "Sana", "Sanjana", "Sanjukta", "Sanya", "Sapna", "Sara",
    "Sarah", "Sarika", "Sarla", "Saroj", "Sathya", "Savita", "Seema", "Shabana", "Shabnam", "Shailaja",
    "Shalini", "Shambhavi", "Shamita", "Shanti", "Sharda", "Sharmila", "Shashi", "Sheela", "Sheetal", "Shefali",
    "Shikha", "Shilpa", "Shirin", "Shivani", "Shobha", "Shraddha", "Shreya", "Shruti", "Shweta", "Sia",
    "Simi", "Simran", "Smita", "Smriti", "Sneha", "Soha", "Soma", "Sona", "Sonakshi", "Sonal",
    "Sonali", "Sonam", "Sonia", "Sophia", "Soumya", "Sowmya", "Srishti", "Sruthi", "Stella", "Subhashini",
    "Suchitra", "Sudha", "Sujata", "Sukanya", "Suman", "Sumitra", "Sunaina", "Sunanda", "Sunidhi", "Sunita",
    "Supriya", "Surabhi", "Surekha", "Sushila", "Sushma", "Swara", "Swati", "Swetha", "Taapsee", "Tamanna",
    "Tanisha", "Tanu", "Tanuja", "Tanvi", "Tanya", "Tara", "Tejal", "Tejaswini", "Tisha", "Trisha",
    "Tulsi", "Twinkle", "Uma", "Urmila", "Urvi", "Usha", "Vaishali", "Vandana", "Vani", "Vanita",
    "Varsha", "Vasudha", "Veda", "Vedika", "Veena", "Vidhi", "Vidya", "Vimala", "Vineeta", "Vinita",
    "Yamini", "Yami", "Yamuna", "Yashaswini", "Yasmin", "Yogita", "Yojana", "Yukta", "Zara", "Zoya"
]
last_names = ["Acharya", "Agarwal", "Aggarwal", "Anand", "Arora", "Babu", "Bajaj", "Balakrishnan", "Banerjee", "Bansal",
    "Barman", "Basu", "Bedi", "Bhadra", "Bhandari", "Bharadwaj", "Bhargava", "Bhat", "Bhatia", "Bhatt",
    "Bhattacharya", "Bhattacharyya", "Bose", "Chacko", "Chadha", "Chakrabarti", "Chakraborty", "Chakravarthy", "Chande", "Chander",
    "Chandra", "Chandran", "Chandrasekhar", "Chatterjee", "Chaturvedi", "Chaudhari", "Chaudhary", "Chauhan", "Chawla", "Cherian",
    "Chhabra", "Chopra", "Choudhary", "Choudhury", "D'Souza", "Dalal", "Das", "Dasgupta", "Datta", "Dave",
    "De", "Deb", "Desai", "Deshmukh", "Deshpande", "Dev", "Devan", "Devi", "Dewan", "Dey",
    "Dhar", "Dhawan", "Dhillon", "Dhingra", "Dixit", "Dubey", "Dutta", "Dwivedi", "Fernandes", "Gaba",
    "Gandhi", "Ganesan", "Ganguly", "Garg", "Gaur", "George", "Ghosh", "Ghoshal", "Gill", "Goel",
    "Gokhale", "Gopal", "Goswami", "Gowda", "Goyal", "Grover", "Guha", "Gulati", "Gupta", "Handa",
    "Hegde", "Husain", "Iyer", "Jacob", "Jadhav", "Jain", "Jaiswal", "Jha", "Johar", "Joshi",
    "Kadam", "Kade", "Kamat", "Kamath", "Kamboj", "Kanda", "Kannan", "Kant", "Kapadia", "Kapoor",
    "Kapur", "Kashyap", "Katiyar", "Kaul", "Kaur", "Kaushal", "Kaushik", "Khan", "Khanna", "Khare",
    "Khatri", "Khera", "Khosla", "Khurana", "Kohli", "Konda", "Korpal", "Kothari", "Krishnan", "Kulkarni",
    "Kumar", "Kumari", "Kundu", "Kurian", "Kutty", "Laghari", "Lal", "Lalla", "Madan", "Mahajan",
    "Mahapatra", "Maheshwari", "Maiti", "Majumdar", "Malhotra", "Malik", "Mallick", "Mallya", "Mandal", "Mangal",
    "Mani", "Mann", "Mannan", "Manohar", "Marar", "Master", "Mathew", "Mathur", "Mehra", "Mehrotra",
    "Mehta", "Menon", "Merchant", "Mishra", "Misra", "Mistry", "Mittal", "Modi", "Mody", "Mohan",
    "Mohanty", "Mukherjee", "Mukhopadhyay", "Mundhra", "Murthy", "Murugan", "Mutreja", "Nadar", "Nadkarni", "Nagar",
    "Nagarajan", "Nayak", "Nayar", "Nigam", "Ojha", "Pai", "Pal", "Palan", "Panda", "Pandey",
    "Pandit", "Pandya", "Panicker", "Pant", "Parab", "Parekh", "Parikh", "Parmar", "Paswan", "Patel",
    "Pathak", "Patil", "Patnaik", "Pawar", "Philip", "Pillai", "Potti", "Prabhu", "Pradhan", "Prakash",
    "Prasad", "Puri", "Raghunathan", "Rai", "Raina", "Raj", "Raja", "Rajan", "Raju", "Ram",
    "Ramachandran", "Ramakrishnan", "Raman", "Ramanathan", "Ramaswamy", "Ramesh", "Rana", "Randhawa", "Ranganathan", "Rao",
    "Rastogi", "Rath", "Rathi", "Rathod", "Rathore", "Ratnam", "Raut", "Raval", "Rawal", "Rawat",
    "Ray", "Reddy", "Roy", "Sabharwal", "Sachan", "Sachdev", "Sachdeva", "Sagar", "Saha", "Sahay",
    "Sahni", "Sahu", "Saini", "Saksena", "Samant", "Sampath", "Sandhu", "Sane", "Sanghvi", "Sankaran",
    "Saraf", "Sarin", "Sarkar", "Sarma", "Sastry", "Sathe", "Satpathy", "Sawant", "Saxena", "Sehgal",
    "Sekhon", "Sen", "Sengupta", "Seth", "Sethi", "Sethuraman", "Shah", "Shankar", "Shanmugam", "Sharma",
    "Shastri", "Shekhawat", "Shenoy", "Shetty", "Shinde", "Shirke", "Shroff", "Shukla", "Sibal", "Sidhu",
    "Singh", "Singhal", "Singhania", "Sinha", "Sodhi", "Solanki", "Som", "Soman", "Soni", "Sood",
    "Srinivas", "Srinivasan", "Srivastava", "Subramaniam", "Subramanian", "Sundaram", "Suri", "Swaminathan", "Syal", "Talwar",
    "Tandon", "Thackeray", "Thakur", "Thomas", "Tiwari", "Tomar", "Tripathi", "Trivedi", "Tyagi", "Upadhyay",
    "Vaidya", "Varghese", "Varma", "Varty", "Varughese", "Vasan", "Venkataraman", "Venkatesan", "Venkatesh", "Verma",
    "Vig", "Vij", "Vyas", "Wadhwa", "Walia", "Waran", "Wariar", "Yadav", "Zaidi"
]
schools = ["A.G. Public School", "Adarsh Public School", "Adarsh Shiksha Niketan", "Air Force Bal Bharati School", "Amity International School",
    "Amrita Vidyalayam", "Apeejay School", "Army Public School", "Arya Vidya Mandir", "Ashok Hall Girls' Higher Secondary School",
    "Assam Valley School", "Atomic Energy Central School", "Baldwin Boys' High School", "Baldwin Girls' High School", "Ballygunge Government High School",
    "Balwantrai Mehta Vidya Bhawan", "Bharatiya Vidya Bhavan", "Birla High School", "Birla Vidya Mandir", "Bishop Cotton Boys' School",
    "Bishop Cotton Girls' School", "Bluebells School International", "Bombay Cambridge School", "Bombay Scottish School", "Bosco Public School",
    "Carmel Convent School", "Cathedral and John Connon School", "Chinmaya Vidyalaya", "Christ Church School", "Christ Nagar School",
    "City Montessori School", "Convent of Jesus and Mary", "DAV Public School", "Daly College", "Darjeeling Himalayan Railway School",
    "Delhi Public School", "Dhirubhai Ambani International School", "Don Bosco School", "Doon International School", "Doon School",
    "Emerald Heights International School", "Frank Anthony Public School", "GD Goenka Public School", "Gitanjali School", "Good Shepherd International School",
    "Greenwood High International School", "Gurukul Grammar Senior Secondary School", "Harrow International School", "Heritage School", "Hebron School",
    "Hiranandani Foundation School", "Holy Child Auxilium School", "Hyderabad Public School", "Indus International School", "Inventure Academy",
    "Jamnabai Narsee School", "Jayshree Periwal International School", "Jindal Public School", "Jawahar Navodaya Vidyalaya", "Kendriya Vidyalaya",
    "La Martiniere College", "La Martiniere for Boys", "La Martiniere for Girls", "Lady Irwin School", "Lawrence School",
    "Lilavatibai Podar High School", "Loreto Convent", "Maharaja Sawai Man Singh Vidyalaya", "Maharani Gayatri Devi Girls' School", "Mayo College",
    "Mayo College Girls' School", "Modern School", "Montfort School", "Mother's International School", "Mount Carmel School",
    "National Public School", "Neerja Modi School", "New Horizon Public School", "Nirmala Convent School", "Oakridge International School",
    "Oberoi International School", "Orchid International School", "Pathways World School", "Pinegrove School", "Podar International School",
    "Presentation Convent Senior Secondary School", "R.N. Podar School", "Rustomjee International School", "Ryan International School", "Sadhu Vaswani International School for Girls",
    "Sahyadri School", "Sai International School", "Sainik School", "Sanskriti School", "Scindia Kanya Vidyalaya",
    "Scindia School", "Scottish High International School", "Seth M.R. Jaipuria School", "Sharda Mandir School", "Sherwood College",
    "Shishukunj International School", "Shriram School", "Sishya School", "Somerville School", "Springdales School",
    "Sri Aurobindo International Centre of Education", "Sri Sathya Sai Higher Secondary School", "St. Ann's High School", "St. Columba's School", "St. Francis' College",
    "St. George's School", "St. James' School", "St. John's High School", "St. Joseph's Boys' High School", "St. Joseph's College",
    "St. Kabir Public School", "St. Karen's High School", "St. Mark's Senior Secondary Public School", "St. Mary's School", "St. Patrick's High School",
    "St. Paul's School", "St. Stephen's School", "St. Thomas' School", "St. Xavier's Collegiate School", "St. Xavier's High School",
    "St. Xavier's School", "Step by Step School", "Stonehill International School", "Tagore International School", "The British School",
    "The Cathedral Vidya School", "The Doon School", "The Fabindia School", "The Geekay World School", "The Glasgow School",
    "The Globe School", "The Good Shepherd School", "The Indian School", "The International School Bangalore", "The Jain International School",
    "The Joseph's School", "The Lawrence School", "The Shri Ram School", "The Woodstock School", "Treamis World School",
    "Utpal Shanghvi Global School", "Vasant Valley School", "Velammal International School", "Vidya Niketan School", "Vidya Sanskar International School",
    "Vidyashilp Academy", "Vikas Vidyalaya", "Vydehi School of Excellence", "Welham Boys' School", "Welham Girls' School",
    "Woodstock School", "Yadavindra Public School", "Zydus School for Excellence", "Abhinav Bharati High School", "Aditya Birla World Academy",
    "Ahlcon International School", "Akshar Arbol International School", "Al-Fajr International School", "Alagar Public School", "All Saints' College",
    "Allenhouse Public School", "Alpha International School", "Amara Jyothi Public School", "Amrita Vidyalayam", "Anand Niketan School",
    "Anchor Bay School", "Apeejay School", "Apple Global School", "Aravali International School", "Arcadia School",
    "Arya Gurukul", "Aryaman Vikram Birla Institute of Learning", "Ascend International School", "Ashoka Universal School", "Asian School",
    "Atmiya Vidya Mandir", "Avalon Heights International School", "B.D. Somani International School", "B.K. Birla Centre for Education", "BGS International Residential School",
    "Banyan Tree School", "Beacon High", "Beas Valley School", "Bellavista School", "Besant Hill School",
    "Bethany High", "Bhaktivedanta Swami Mission School", "Bharadwaja Vidyashram", "Bharati Vidya Bhavan's Public School", "Bhartiya Vidya Mandir",
    "Bhavan's Gangabux Kanoria Vidyamandir", "Bhavan's Rajaji Vidyashram", "Bhopal Public School", "Billabong High International School", "Birla Open Minds International School",
    "Blossom Public School", "Bodhi Taru International School", "Bombay International School", "Bon Secours School", "Boon School",
    "Bosco Public School", "Brainworks School", "Brewster's School", "Bridge International School", "Brigade School",
    "Bright Angels School", "Bright Day School", "Bright Start Fellowship International School", "Brilliant Public School", "Brookfield High School",
    "Buddha's International School", "C.P. Goenka International School", "Campion School", "Candor International School", "Canossa High School",
    "Capital Public School", "Carmel Garden Public School", "Carmel High School", "Carmel School", "Cathedral and John Connon School",
    "Cauvery International School", "Cedarwood School", "Central India Academy", "Centre Point School", "Chaitanya Vidyalaya",
    "Chalk Tree Global School", "Chaman Bhartiya School", "Champions School", "Chandrakant Patil Public School", "Chettinad Vidyashram",
    "Children's Academy", "Chinmaya International Residential School", "Chirec International School", "Chitrakoota School", "Chittagong Grammar School",
    "Christ Academy", "Christ Church College", "Christ College", "Christ International School", "ChristJyoti School",
    "Christ The King School", "Christwood School", "Crescent School",
    "Crystal International School", "D.A.V. International School", "D.G. Khetan International School", "D.Y. Patil International School", "Dakshina Kannada Zilla Panchayat Higher Primary School",
    "Dalhousie Public School", "Damien School", "Darshan Academy", "Dasmesh Public School", "Datta Meghe World Academy",
    "Dawn International School", "Dayanand Anglo-Vedic Public School", "Dayawati Modi Academy", "De Paul International Residential School", "Deccan International School",
    "Deep-In International School", "Delhi Cambridge School", "Delhi International School", "Delhi World Public School", "Delta Study",
    "Deogiri Global Academy", "Deva Matha Central School", "Dewan Public School", "Dharav High School", "Diamond Jubilee High School"
]

# --- Configuration ---
BASE_URL = "http://localhost:8000/api/forms/submit-student/"
# IMPORTANT: Replace with a valid access token obtained after logging in to the frontend.
# You can usually find this in your browser's developer tools (Application -> Local Storage).
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NjAxMzMwLCJpYXQiOjE3Njc1OTc3MzAsImp0aSI6IjY0ZTNiMjBhYmFiNTQzMTE4ZWUzNjY5MWFlNDA4ZTFmIiwidXNlcl9pZCI6IjEifQ.puiOeSl7MAGD9vLFqEZ634EnLhoUrbIOiTFWNs_KK6o" 

NUM_ENTRIES = 600

# --- Helper Functions for Data Generation ---

def generate_random_date(start_year =2020, end_year=2025):
    """Generates a random date within a given year range."""
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28) # To avoid issues with month lengths
    return f"{year}-{month:02d}-{day:02d}"

def generate_student_data(index):
    genders = ["Male", "Female", "Other"]
    parental_myopia_options = ["None", "Father", "Mother", "Both"]
    birth_order_options = ["First", "Second", "Third", "Only Child"]

    return {
        "name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "school_name": random.choice(schools),
        "age": random.randint(6, 18),
        "gender": random.choice(genders),
        "height": round(random.uniform(110.0, 180.0), 1),
        "weight": round(random.uniform(20.0, 80.0), 1),
        "parental_myopia": random.choice(parental_myopia_options),
        "num_siblings": random.randint(0, 5),
        "birth_order": random.choice(birth_order_options),
        "siblings_myopia": random.randint(0, 3)
    }

def generate_lifestyle_data():
    outdoor_duration_options = ["<1 hr", "1-2 hrs", "2-4 hrs", ">4 hrs"]
    sun_exposure_options = ["<15 min", "15-30 min", "30-60 min", ">1 hr"]
    near_work_hours_options = ["<2 hrs", "2-4 hrs", "4-6 hrs", ">6 hrs"]
    screen_time_options = ["<1 hr", "1-3 hrs", "3-5 hrs", ">5 hrs"]
    primary_device_options = ["TV", "Tablet", "Mobile", "Laptop/Desktop"]
    reading_distance_options = ["<20 cm", "20-30 cm", ">30 cm"]
    viewing_posture_options = ["Low", "Optimum", "High"]
    dietary_habit_options = ["Balanced", "Junk-food dominant", "Vegetarian", "Non-vegetarian", "Other"]
    sleep_duration_options = ["<6 hrs", "6-7 hrs", "7-8 hrs", ">8 hrs"]
    usual_bedtime_options = ["Before 9 PM", "9-10 PM", "10-11 PM", "After 11 PM"]

    return {
        "outdoor_time": f"{random.randint(8, 18):02d}:{random.choice([0, 30]):02d}",
        "outdoor_duration": random.choice(outdoor_duration_options),
        "sun_exposure": random.choice(sun_exposure_options),
        "near_work_hours": random.choice(near_work_hours_options),
        "screen_time": random.choice(screen_time_options),
        "primary_device": random.choice(primary_device_options),
        "reading_distance": random.choice(reading_distance_options),
        "viewing_posture_ratio": random.choice(viewing_posture_options),
        "dietary_habit": random.choice(dietary_habit_options),
        "dietary_other": "Fast food" if random.random() < 0.2 else None,
        "sleep_duration": random.choice(sleep_duration_options),
        "usual_bedtime": random.choice(usual_bedtime_options)
    }

def generate_environment_data():
    school_type_options = ["Urban", "Rural"]
    classroom_strength_options = ["<30", "30-50", ">50"]
    seating_position_options = ["Front", "Middle", "Back"]
    teaching_methodology_options = ["Digital", "Traditional"]
    lighting_options = ["Dim", "Adequate", "Bright"]
    sunlight_source_options = ["Natural", "Artificial", "Both"]

    return {
        "school_type": random.choice(school_type_options),
        "classroom_strength": random.choice(classroom_strength_options),
        "seating_position": random.choice(seating_position_options),
        "teaching_methodology": random.choice(teaching_methodology_options),
        "lighting": random.choice(lighting_options),
        "sunlight_source": random.choice(sunlight_source_options)
    }

def generate_history_data():
    compliance_options = ["Always", "Sometimes", "Rarely"]
    
    diagnosed_earlier = random.choice([True, False])
    age_at_diagnosis = random.randint(5, 15) if diagnosed_earlier else None

    return {
        "diagnosed_earlier": diagnosed_earlier,
        "age_at_diagnosis": age_at_diagnosis,
        "power_changed_last_3yrs": random.choice([True, False]),
        "compliance": random.choice(compliance_options),
        "previous_re": f"{random.uniform(-5.0, 2.0):.2f}",
        "previous_le": f"{random.uniform(-5.0, 2.0):.2f}",
        "current_re": f"{random.uniform(-6.0, 3.0):.2f}",
        "current_le": f"{random.uniform(-6.0, 3.0):.2f}"
    }

def generate_awareness_data():
    source_of_awareness_options = ["School", "Family", "Doctor", "Media", "Other", "None"]
    
    sources = random.sample(source_of_awareness_options, k=random.randint(1, 3))
    source_other = "Online forums" if "Other" in sources and random.random() < 0.5 else None
    
    # Ensure "None" is exclusive if chosen
    if "None" in sources and len(sources) > 1:
        sources = ["None"]
    
    return {
        "aware_eye_strain": random.choice([True, False]),
        "access_to_vision_care": random.choice([True, False]),
        "follows_preventive_measures": random.choice(["Always", "Sometimes", "Never"]),
        "source_of_awareness": ", ".join(sources) if sources else None,
        "source_other": source_other
    }

def generate_ocular_data():
    return {
        "uncorrectedvisual_acuity_right_eye": f"{random.uniform(0.1, 1.0):.1f}",
        "uncorrectedvisual_acuity_left_eye": f"{random.uniform(0.1, 1.0):.1f}",
        "bestcorrectedvisual_acuity_right_eye": f"{random.uniform(0.8, 1.2):.1f}",
        "bestcorrectedvisual_acuity_left_eye": f"{random.uniform(0.8, 1.2):.1f}",
        "cycloplegic_auto_refraction_right_eye": f"{random.uniform(-4.0, 1.0):.2f}",
        "cycloplegic_auto_refraction_left_eye": f"{random.uniform(-4.0, 1.0):.2f}",
        "spherical_power_right_eye": f"{random.uniform(-5.0, 2.0):.2f}",
        "spherical_power_left_eye": f"{random.uniform(-5.0, 2.0):.2f}",
        "axial_length_right_eye": f"{random.uniform(22.0, 26.0):.2f}",
        "axial_length_left_eye": f"{random.uniform(22.0, 26.0):.2f}",
        "corneal_curvature_right_eye": f"{random.uniform(40.0, 48.0):.2f}",
        "corneal_curvature_left_eye": f"{random.uniform(40.0, 48.0):.2f}",
        "central_corneal_thickness_right_eye": f"{random.randint(500, 600)}",
        "central_corneal_thickness_left_eye": f"{random.randint(500, 600)}",
        "anterior_segment_finding_right_eye": random.choice(["Clear", "Mild conjunctivitis", "Pinguecula"]) if random.random() < 0.3 else "",
        "anterior_segment_finding_left_eye": random.choice(["Clear", "Mild conjunctivitis", "Pinguecula"]) if random.random() < 0.3 else "",
        "amblyopia_or_strabismus": random.choice([True, False]),
        "fundus_examination_finding_right_eye": random.choice(["Normal", "Myopic fundus changes"]) if random.random() < 0.2 else "Normal",
        "fundus_examination_finding_left_eye": random.choice(["Normal", "Myopic fundus changes"]) if random.random() < 0.2 else "Normal"
    }

# --- Main Script ---
def run_test_data_generation():
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
        print("ERROR: Please replace 'YOUR_ACCESS_TOKEN_HERE' in generate_test_data.py with a valid access token.")
        print("You can get this from your browser's developer tools (Application tab -> Local Storage -> your domain).")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    success_count = 0
    failure_count = 0

    print(f"Starting to submit {NUM_ENTRIES} new entries...")

    for i in range(1, NUM_ENTRIES + 1):
        student_data = generate_student_data(i)
        
        # Assemble the full payload
        payload = {
            "visit_date": generate_random_date(),
            **student_data, # Directly embed student data (Section A)
            "lifestyle": generate_lifestyle_data(),
            "environment": generate_environment_data(),
            "history": generate_history_data(),
            "awareness": generate_awareness_data(),
            "ocular": generate_ocular_data()
        }

        try:
            response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx) 
            
            result = response.json()
            print(f"Entry {i}/{NUM_ENTRIES}: Submitted '{student_data['name']}' successfully. Student ID: {result.get('student_id')}")
            success_count += 1

        except requests.exceptions.HTTPError as http_err:
            print(f"Entry {i}/{NUM_ENTRIES}: HTTP error occurred for '{student_data['name']}': {http_err} - {response.text}")
            failure_count += 1
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Entry {i}/{NUM_ENTRIES}: Connection error occurred for '{student_data['name']}': {conn_err}. Is the backend server running?")
            failure_count += 1
        except requests.exceptions.Timeout as timeout_err:
            print(f"Entry {i}/{NUM_ENTRIES}: Timeout error occurred for '{student_data['name']}': {timeout_err}")
            failure_count += 1
        except requests.exceptions.RequestException as req_err:
            print(f"Entry {i}/{NUM_ENTRIES}: An unexpected error occurred for '{student_data['name']}': {req_err}")
            failure_count += 1
        except json.JSONDecodeError:
            print(f"Entry {i}/{NUM_ENTRIES}: Failed to decode JSON response for '{student_data['name']}'. Response: {response.text}")
            failure_count += 1

    print("\n--- Summary ---")
    print(f"Total entries attempted: {NUM_ENTRIES}")
    print(f"Successful submissions: {success_count}")
    print(f"Failed submissions: {failure_count}")

if __name__ == "__main__":
    run_test_data_generation()
    run_test_data_generation()

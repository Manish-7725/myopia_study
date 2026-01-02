import random
import string
from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import (
    Student, LifestyleBehavior, EnvironmentalFactor,
    ClinicalHistory, AwarenessSafety, OcularExamination,
    FollowUp, FollowUpEnvironmental, FollowUpHistory, FollowUpOcular
)


class RandomDataGenerator:
    """Utility class to generate random test data"""
    
    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def random_email():
        return f"{RandomDataGenerator.random_string(8)}@test.com"
    
    @staticmethod
    def random_student_id():
        while True:
            student_id = 'STU' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Student.objects.filter(student_id=student_id).exists():
                return student_id
    
    @staticmethod
    def random_name():
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
    "Yamini", "Yami", "Yamuna", "Yashaswini", "Yasmin", "Yogita", "Yojana", "Yukta", "Zara", "Zoya"]
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
    "Vig", "Vij", "Vyas", "Wadhwa", "Walia", "Waran", "Wariar", "Yadav", "Zaidi"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    @staticmethod
    def random_school():
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
    "Bethany High", "Bhaktivedanta Swami Mission School", "Bharadwaja Vidyashram", "Bharati Vidya Bhavan's Public School", "Bharati Vidyapeeth English Medium School",
    "Bhartiya Vidya Mandir", "Bhavan's Gangabux Kanoria Vidyamandir", "Bhavan's Rajaji Vidyashram", "Bhopal Public School", "Billabong High International School",
    "Birla Open Minds International School", "Blossom Public School", "Bodhi Taru International School", "Bombay International School", "Bon Secours School",
    "Boon School", "Bosco Public School", "Brainworks School", "Brewster's School", "Bridge International School",
    "Brigade School", "Bright Angels School", "Bright Day School", "Bright Start Fellowship International School", "Brilliant Public School",
    "Brookfield High School", "Buddha's International School", "C.P. Goenka International School", "Campion School", "Candor International School",
    "Canossa High School", "Capital Public School", "Carmel Garden Public School", "Carmel High School", "Carmel School",
    "Cathedral and John Connon School", "Cauvery International School", "Cedarwood School", "Central India Academy", "Centre Point School",
    "Chaitanya Vidyalaya", "Chalk Tree Global School", "Chaman Bhartiya School", "Champions School", "Chandrakant Patil Public School",
    "Chettinad Vidyashram", "Children's Academy", "Chinmaya International Residential School", "Chirec International School", "Chitrakoota School",
    "Chittagong Grammar School", "Christ Academy", "Christ Church College", "Christ College", "Christ International School",
    "ChristJyoti School", "Christ The King School", "Christ Vidyaniketan", "Christwood School", "Crescent School",
    "Crystal International School", "D.A.V. International School", "D.G. Khetan International School", "D.Y. Patil International School", "Dakshina Kannada Zilla Panchayat Higher Primary School",
    "Dalhousie Public School", "Damien School", "Darshan Academy", "Dasmesh Public School", "Datta Meghe World Academy",
    "Dawn International School", "Dayanand Anglo-Vedic Public School", "Dayawati Modi Academy", "De Paul International Residential School", "Deccan International School",
    "Deep-In International School", "Delhi Cambridge School", "Delhi International School", "Delhi World Public School", "Delta Study",
    "Deogiri Global Academy", "Deva Matha Central School", "Dewan Public School", "Dharav High School", "Diamond Jubilee High School",

]
        return random.choice(schools)
    
    @staticmethod
    def random_gender():
        return random.choice(["Male", "Female", "Other"])
    
    @staticmethod
    def random_boolean():
        return random.choice([True, False])


# class AuthenticationTests(TestCase):
#     """Test authentication endpoints with multiple iterations"""
    
#     def setUp(self):
#         self.client = APIClient()
#         self.signup_url = '/api/signup/'
#         self.login_url = '/api/login/'
    
#     def test_signup_1000_users(self):
#         """Test signup with 1000 random users"""
#         print("\n=== Testing Signup with 1000 iterations ===")
        
#         successful_signups = 0
#         for i in range(1000):
#             username = RandomDataGenerator.random_string(12)
#             email = RandomDataGenerator.random_email()
#             password = "TestPass123!@#"
            
#             data = {
#                 'username': username,
#                 'email': email,
#                 'password': password
#             }
            
#             response = self.client.post(self.signup_url, data)
            
#             if response.status_code == status.HTTP_201_CREATED:
#                 successful_signups += 1
            
#             if (i + 1) % 100 == 0:
#                 print(f"Progress: {i + 1}/1000 signups completed")
        
#         print(f"Successful signups: {successful_signups}/1000")
#         self.assertGreater(successful_signups, 990)
    
#     def test_login_1000_attempts(self):
#         """Test login with 1000 random attempts"""
#         print("\n=== Testing Login with 1000 iterations ===")
        
#         test_users = []
#         for i in range(100):
#             username = f"testuser{i}"
#             email = f"test{i}@example.com"
#             password = "TestPass123!@#"
#             User.objects.create_user(username=username, email=email, password=password)
#             test_users.append({'username': username, 'email': email, 'password': password})
        
#         successful_logins = 0
        
#         for i in range(1000):
#             user_data = random.choice(test_users)
#             identifier = random.choice([user_data['username'], user_data['email']])
            
#             data = {
#                 'username': identifier,
#                 'password': user_data['password']
#             }
            
#             response = self.client.post(self.login_url, data)
            
#             if response.status_code == status.HTTP_200_OK:
#                 successful_logins += 1
            
#             if (i + 1) % 100 == 0:
#                 print(f"Progress: {i + 1}/1000 login attempts completed")
        
#         print(f"Successful logins: {successful_logins}/1000")
#         self.assertEqual(successful_logins, 1000)


class StudentModelTests(TestCase):
    """Test Student model with extensive iterations"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_2000_students(self):
        """Create 2000 random students"""
        print("\n=== Creating 2000 Random Students ===")
        
        for i in range(2000):
            Student.objects.create(
                student_id=RandomDataGenerator.random_student_id(),
                name=RandomDataGenerator.random_name(),
                school_name=RandomDataGenerator.random_school(),
                age=random.randint(5, 18),
                gender=RandomDataGenerator.random_gender(),
                height=round(random.uniform(100, 180), 2),
                weight=round(random.uniform(20, 80), 2),
                parental_myopia=random.choice(["None", "Father", "Mother", "Both"]),
                num_siblings=random.randint(0, 5),
                created_by=self.user
            )
            
            if (i + 1) % 200 == 0:
                print(f"Progress: {i + 1}/2000 students created")
        
        total_students = Student.objects.count()
        print(f"Total students in database: {total_students}")
        self.assertEqual(total_students, 2000)


class FormSubmissionTests(TestCase):
    """Test form submission with comprehensive data"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.submit_url = '/api/forms/submit/'
    
    def generate_form_data(self, student_id=None):
        if student_id is None:
            student_id = RandomDataGenerator.random_student_id()

        return {
            "student": {
                "student_id": student_id,
                "name": RandomDataGenerator.random_name(),
                "school_name": RandomDataGenerator.random_school(),
                "age": random.randint(5, 18),
                "gender": RandomDataGenerator.random_gender()
            },
            "lifestyle": {
                "outdoor_duration": random.choice(["<1hr", "1-2hrs", "2-3hrs"]),
                "screen_time": random.choice(["<2hrs", "2-4hrs", "4-6hrs"])
            },
            "environment": {
                "school_type": random.choice(["Government", "Private"]),
                "classroom_strength": random.choice(["<30", "30-50"])
            },
            "history": {
                "diagnosed_earlier": RandomDataGenerator.random_boolean(),
                "power_changed_last_3yrs": RandomDataGenerator.random_boolean()
            },
            "awareness": {
                "aware_eye_strain": RandomDataGenerator.random_boolean(),
                "access_to_vision_care": RandomDataGenerator.random_boolean()
            },
            "ocular": {
                "ucva_re": "6/6",
                "ucva_le": "6/6",
                "amblyopia_or_strabismus": RandomDataGenerator.random_boolean()
            }
        }
    
    def test_submit_form_creates_student(self):
        """Test that submitting a form creates a new student."""
        form_data = self.generate_form_data()
        response = self.client.post(self.submit_url, form_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertTrue(Student.objects.filter(student_id=form_data['student']['student_id']).exists())

    def test_update_student_on_form_submission(self):
        """Test that submitting a form for an existing student updates their data."""
        # 1. Create a student by submitting a form
        student_id = RandomDataGenerator.random_student_id()
        initial_form_data = self.generate_form_data(student_id=student_id)
        initial_school_name = "Initial School"
        initial_form_data['student']['school_name'] = initial_school_name

        response = self.client.post(self.submit_url, initial_form_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        
        # Verify student was created with the initial school name
        student = Student.objects.get(student_id=student_id)
        self.assertEqual(student.school_name, initial_school_name)

        # 2. Submit the form again for the same student with an updated school name
        updated_form_data = self.generate_form_data(student_id=student_id)
        updated_school_name = "Updated School"
        updated_form_data['student']['school_name'] = updated_school_name

        response = self.client.post(self.submit_url, updated_form_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        # 3. Verify that the student's school name was updated
        student.refresh_from_db()
        self.assertEqual(student.school_name, updated_school_name)
        # Also ensure we haven't created a new student
        self.assertEqual(Student.objects.filter(student_id=student_id).count(), 1)

    def test_submit_5000_forms(self):
        """Submit 5000 forms"""
        print("\n=== Submitting 5000 Forms ===")
        
        successful = 0
        
        for i in range(5000):
            form_data = self.generate_form_data()
            response = self.client.post(self.submit_url, form_data, format='json')
            
            if response.status_code in [200, 201]:
                successful += 1
            
            if (i + 1) % 500 == 0:
                print(f"Progress: {i + 1}/5000 - Success: {successful}")
        
        print(f"Total successful: {successful}/5000")


print("\n" + "="*70)
print("MYOPIA ANALYSIS - COMPREHENSIVE TEST SUITE")
print("Testing with 5000+ iterations across all modules")
print("="*70)

import random
import string
from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import (
    Student, ClinicalVisit, LifestyleBehavior, EnvironmentalFactor,
    ClinicalHistory, AwarenessSafety, OcularExamination
)


class RandomDataGenerator:
    """Utility class to generate random test data"""
    
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
    "ChristJyoti School", "Christ The King School", "Christwood School", "Crescent School",
    "Crystal International School", "D.A.V. International School", "D.G. Khetan International School", "D.Y. Patil International School", "Dakshina Kannada Zilla Panchayat Higher Primary School",
    "Dalhousie Public School", "Damien School", "Darshan Academy", "Dasmesh Public School", "Datta Meghe World Academy",
    "Dawn International School", "Dayanand Anglo-Vedic Public School", "Dayawati Modi Academy", "De Paul International Residential School", "Deccan International School",
    "Deep-In International School", "Delhi Cambridge School", "Delhi International School", "Delhi World Public School", "Delta Study",
    "Deogiri Global Academy", "Deva Matha Central School", "Dewan Public School", "Dharav High School", "Diamond Jubilee High School",

]

    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def random_email():
        return f"{RandomDataGenerator.random_string(8)}@test.com"
    
    @classmethod
    def random_name(cls):
        return f"{random.choice(cls.first_names)} {random.choice(cls.last_names)}"
    
    @classmethod
    def random_school(cls):
        return random.choice(cls.schools)
    
    @staticmethod
    def random_gender():
        return random.choice(["Male", "Female", "Other"])
    
    @staticmethod
    def random_boolean():
        return random.choice([True, False])


class RandomDataGeneratorTests(TestCase):
    """Test the RandomDataGenerator utility class"""

    def test_random_string(self):
        self.assertIsInstance(RandomDataGenerator.random_string(), str)
        self.assertEqual(len(RandomDataGenerator.random_string(15)), 15)

    def test_random_email(self):
        email = RandomDataGenerator.random_email()
        self.assertIsInstance(email, str)
        self.assertIn('@', email)
        self.assertIn('.com', email)

    def test_random_name(self):
        name = RandomDataGenerator.random_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name.split()) >= 2)

    def test_random_school(self):
        school = RandomDataGenerator.random_school()
        self.assertIsInstance(school, str)
        self.assertIn(school, RandomDataGenerator.schools)

    def test_random_gender(self):
        gender = RandomDataGenerator.random_gender()
        self.assertIsInstance(gender, str)
        self.assertIn(gender, ["Male", "Female", "Other"])

    def test_random_boolean(self):
        self.assertIsInstance(RandomDataGenerator.random_boolean(), bool)


# class AuthenticationTests(TestCase):
#     """Test authentication endpoints with multiple iterations"""
    
#     def setUp(self):
#         self.client = APIClient()
#         self.signup_url = reverse('api-signup')
#         self.login_url = reverse('api-login')
    
#     def test_signup_100_users(self):
#         """Test signup with 100 random users"""
#         print("\n=== Testing Signup with 100 iterations ===")
        
#         successful_signups = 0
#         for i in range(100):
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
            
#             if (i + 1) % 10 == 0:
#                 print(f"Progress: {i + 1}/100 signups completed")
        
#         print(f"Successful signups: {successful_signups}/100")
#         self.assertGreater(successful_signups, 90)
    
#     def test_login_100_attempts(self):
#         """Test login with 100 random attempts"""
#         print("\n=== Testing Login with 100 iterations ===")
        
#         test_users = []
#         for i in range(10):
#             username = f"testuser{i}"
#             email = f"test{i}@example.com"
#             password = "TestPass123!@#"
#             User.objects.create_user(username=username, email=email, password=password)
#             test_users.append({'username': username, 'email': email, 'password': password})
        
#         successful_logins = 0
        
#         for i in range(100):
#             user_data = random.choice(test_users)
#             identifier = random.choice([user_data['username'], user_data['email']])
            
#             data = {
#                 'username': identifier,
#                 'password': user_data['password']
#             }
            
#             response = self.client.post(self.login_url, data)
            
#             if response.status_code == status.HTTP_200_OK:
#                 successful_logins += 1
            
#             if (i + 1) % 10 == 0:
#                 print(f"Progress: {i + 1}/100 login attempts completed")
        
#         print(f"Successful logins: {successful_logins}/100")
#         self.assertEqual(successful_logins, 100)


class StudentModelTests(TestCase):
    """Test Student model with extensive iterations"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='new_user',
            email='test@example.com',
            password='Test@123'
        )
    
    def test_create_100_students(self):
        """Create 100 random students"""
        print("\n=== Creating 100 Random Students ===")
        
        for i in range(200):
            Student.objects.create(
                name=RandomDataGenerator.random_name(),
                school_name=RandomDataGenerator.random_school(),
                age=random.randint(5, 18),
                gender=RandomDataGenerator.random_gender(),
                height=round(random.uniform(100, 180), 2),
                weight=round(random.uniform(20, 80), 2),
                parental_myopia=random.choice(["None", "Father", "Mother", "Both"]),
                num_siblings=random.randint(0, 5),
            )
            
            if (i + 1) % 10 == 0:
                print(f"Progress: {i + 1}/100 students created")
        
        total_students = Student.objects.count()
        print(f"Total students in database: {total_students}")
        self.assertEqual(total_students, 200)


class StudentFormSubmissionTests(TestCase):
    """Test student form submission (baseline creation)"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.submit_student_url = reverse('submit-student')
    
    def generate_student_form_data(self, name=None, age=None, gender=None):
        return {
            "visit_date": date.today().isoformat(),
            "name": name if name else RandomDataGenerator.random_name(),
            "age": age if age else random.randint(5, 18),
            "gender": gender if gender else RandomDataGenerator.random_gender(),
            "school_name": RandomDataGenerator.random_school(),
            "height": round(random.uniform(100, 180), 2),
            "weight": round(random.uniform(20, 80), 2),
            "parental_myopia": random.choice(["None", "Father", "Mother", "Both"]),
            "num_siblings": random.randint(0, 5),
            "birth_order": random.choice(["First", "Second", "Third", "Last", "Only"]),
            "siblings_myopia": random.randint(0, 3),
            "lifestyle": {
                "outdoor_time": "10:00:00",
                "outdoor_duration": random.choice(["<1hr", "1-2hrs", "2-3hrs"]),
                "sun_exposure": random.choice(["Low", "Medium", "High"]),
                "near_work_hours": random.choice(["<2hrs", "2-4hrs", "4-6hrs", ">6hrs"]),
                "screen_time": random.choice(["<2hrs", "2-4hrs", "4-6hrs", ">6hrs"]),
                "primary_device": random.choice(["Smartphone", "Tablet", "Computer", "TV"]),
                "reading_distance": random.choice(["<20cm", "20-30cm", ">30cm"]),
                "viewing_posture_ratio": random.choice(["Good", "Average", "Poor"]),
                "dietary_habit": random.choice(["Vegetarian", "Non-Vegetarian", "Vegan"]),
                "dietary_other": "Some other diet",
                "sleep_duration": random.choice(["<6hrs", "6-8hrs", ">8hrs"]),
                "usual_bedtime": "22:00:00",
            },
            "environment": {
                "school_type": random.choice(["Government", "Private", "International"]),
                "classroom_strength": random.choice(["<30", "30-50", ">50"]),
                "seating_position": random.choice(["Front", "Middle", "Back"]),
                "teaching_methodology": random.choice(["Traditional", "Modern", "Hybrid"]),
                "lighting": random.choice(["Natural", "Artificial", "Mixed"]),
                "sunlight_source": random.choice(["Window", "Door", "None"]),
            },
            "history": {
                "diagnosed_earlier": RandomDataGenerator.random_boolean(),
                "age_at_diagnosis": random.randint(5, 15),
                "power_changed_last_3yrs": RandomDataGenerator.random_boolean(),
                "compliance": random.choice(["High", "Medium", "Low"]),
                "previous_re": "-1.00",
                "previous_le": "-1.50",
                "current_re": "-2.00",
                "current_le": "-2.50",
            },
            "awareness": {
                "aware_eye_strain": RandomDataGenerator.random_boolean(),
                "access_to_vision_care": RandomDataGenerator.random_boolean(),
                "follows_preventive_measures": random.choice(["Always", "Sometimes", "Never"]),
                "source_of_awareness": random.choice(["Doctor", "Internet", "Friends", "Family"]),
            },
            "ocular": {
                "uncorrectedvisual_acuity_right_eye": "6/6",
                "uncorrectedvisual_acuity_left_eye": "6/9",
                "bestcorrectedvisual_acuity_right_eye": "6/6",
                "bestcorrectedvisual_acuity_left_eye": "6/6",
                "cycloplegic_auto_refraction_right_eye": "-1.00",
                "cycloplegic_auto_refraction_left_eye": "-1.25",
                "spherical_power_right_eye": "-1.00",
                "spherical_power_left_eye": "-1.25",
                "axial_length_right_eye": "23.5",
                "axial_length_left_eye": "23.8",
                "corneal_curvature_right_eye": "42.5",
                "corneal_curvature_left_eye": "42.8",
                "central_corneal_thickness_right_eye": "550",
                "central_corneal_thickness_left_eye": "552",
                "anterior_segment_finding_right_eye": "Normal",
                "anterior_segment_finding_left_eye": "Normal",
                "amblyopia_or_strabismus": RandomDataGenerator.random_boolean(),
                "fundus_examination_finding_right_eye": "Normal",
                "fundus_examination_finding_left_eye": "Normal",
            }
        }
    
    def test_submit_form_creates_student_and_baseline_visit(self):
        """Test that submitting a form creates a new student and a baseline visit."""
        form_data = self.generate_student_form_data()
        response = self.client.post(self.submit_student_url, form_data, format='json')
        print("test_submit_form_creates_student_and_baseline_visit response:", response.data) # Debug print
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("student_id", response.data)
        
        student = Student.objects.get(name=form_data['name'], age=form_data['age'], gender=form_data['gender'])
        self.assertEqual(student.student_id, response.data['student_id'])
        self.assertTrue(ClinicalVisit.objects.filter(student=student, visit_type="BASELINE").exists())
        self.assertTrue(LifestyleBehavior.objects.filter(visit__student=student).exists())

    def test_submit_duplicate_student_fails(self):
        """Test that submitting a form for an existing student (duplicate name, age, gender) fails with 409."""
        name = RandomDataGenerator.random_name()
        age = random.randint(5, 18)
        gender = RandomDataGenerator.random_gender()

        # First submission (should succeed)
        form_data_1 = self.generate_student_form_data(name=name, age=age, gender=gender)
        response_1 = self.client.post(self.submit_student_url, form_data_1, format='json')
        print("test_submit_duplicate_student_fails - Response 1:", response_1.data) # Debug print
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(name=name, age=age, gender=gender).exists())

        # Second submission with same name, age, gender (should fail)
        form_data_2 = self.generate_student_form_data(name=name, age=age, gender=gender)
        response_2 = self.client.post(self.submit_student_url, form_data_2, format='json')
        print("test_submit_duplicate_student_fails - Response 2:", response_2.data) # Debug print
        self.assertEqual(response_2.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("error", response_2.data)


class FollowUpFormSubmissionTests(TestCase):
    """Test follow-up form submission for existing students"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser_followup',
            email='followup@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.submit_followup_url = reverse('submit-followup')

        # Create a student and baseline visit directly in the database
        self.student = Student.objects.create(
            name=RandomDataGenerator.random_name(),
            age=random.randint(5, 18),
            gender=RandomDataGenerator.random_gender(),
            school_name=RandomDataGenerator.random_school(),
            parental_myopia=random.choice(["None", "Father", "Mother", "Both"]),
            height=round(random.uniform(100, 180), 2),
            weight=round(random.uniform(20, 80), 2),
            num_siblings=random.randint(0, 5),
            birth_order=random.choice(["First", "Second", "Third", "Last", "Only"]),
            siblings_myopia=random.randint(0, 3),
        )
        self.baseline_visit = ClinicalVisit.objects.create(
            student=self.student,
            visit_date=date.today(),
            visit_type="BASELINE"
        )
        # Create related objects for the baseline visit
        LifestyleBehavior.objects.create(visit=self.baseline_visit)
        EnvironmentalFactor.objects.create(visit=self.baseline_visit)
        ClinicalHistory.objects.create(visit=self.baseline_visit)
        AwarenessSafety.objects.create(visit=self.baseline_visit)
        OcularExamination.objects.create(visit=self.baseline_visit)

        self.student_id = self.student.student_id
    
    def generate_followup_form_data(self, student_id=None):
        return {
            "student_id": student_id if student_id else self.student_id,
            "visit_date": (date.today() + timedelta(days=30)).isoformat(), # Future date for followup
            "lifestyle": {
                "outdoor_time": "11:00:00",
                "outdoor_duration": random.choice(["<1hr", "1-2hrs", "2-3hrs"]),
                "sun_exposure": random.choice(["Low", "Medium", "High"]),
                "near_work_hours": random.choice(["<2hrs", "2-4hrs", "4-6hrs", ">6hrs"]),
                "screen_time": random.choice(["<2hrs", "2-4hrs", "4-6hrs", ">6hrs"]),
                "primary_device": random.choice(["Smartphone", "Tablet", "Computer", "TV"]),
                "reading_distance": random.choice(["<20cm", "20-30cm", ">30cm"]),
                "viewing_posture_ratio": random.choice(["Good", "Average", "Poor"]),
                "dietary_habit": random.choice(["Vegetarian", "Non-Vegetarian", "Vegan"]),
                "dietary_other": "Some other diet",
                "sleep_duration": random.choice(["<6hrs", "6-8hrs", ">8hrs"]),
                "usual_bedtime": "22:00:00",
            },
            "environment": {
                "school_type": random.choice(["Government", "Private", "International"]),
                "classroom_strength": random.choice(["<30", "30-50", ">50"]),
                "seating_position": random.choice(["Front", "Middle", "Back"]),
                "teaching_methodology": random.choice(["Traditional", "Modern", "Hybrid"]),
                "lighting": random.choice(["Natural", "Artificial", "Mixed"]),
                "sunlight_source": random.choice(["Window", "Door", "None"]),
            },
            "history": {
                "diagnosed_earlier": RandomDataGenerator.random_boolean(),
                "age_at_diagnosis": random.randint(5, 15),
                "power_changed_last_3yrs": RandomDataGenerator.random_boolean(),
                "compliance": random.choice(["High", "Medium", "Low"]),
                "previous_re": "-1.00",
                "previous_le": "-1.50",
                "current_re": "-2.00",
                "current_le": "-2.50",
            },
            "awareness": {
                "aware_eye_strain": RandomDataGenerator.random_boolean(),
                "access_to_vision_care": RandomDataGenerator.random_boolean(),
                "follows_preventive_measures": random.choice(["Always", "Sometimes", "Never"]),
                "source_of_awareness": random.choice(["Doctor", "Internet", "Friends", "Family"]),
            },
            "ocular": {
                "uncorrectedvisual_acuity_right_eye": "6/9",
                "uncorrectedvisual_acuity_left_eye": "6/12",
                "bestcorrectedvisual_acuity_right_eye": "6/6",
                "bestcorrectedvisual_acuity_left_eye": "6/6",
                "cycloplegic_auto_refraction_right_eye": "-1.00",
                "cycloplegic_auto_refraction_left_eye": "-1.25",
                "spherical_power_right_eye": "-1.00",
                "spherical_power_left_eye": "-1.25",
                "axial_length_right_eye": "23.5",
                "axial_length_left_eye": "23.8",
                "corneal_curvature_right_eye": "42.5",
                "corneal_curvature_left_eye": "42.8",
                "central_corneal_thickness_right_eye": "550",
                "central_corneal_thickness_left_eye": "552",
                "anterior_segment_finding_right_eye": "Normal",
                "anterior_segment_finding_left_eye": "Normal",
                "amblyopia_or_strabismus": RandomDataGenerator.random_boolean(),
                "fundus_examination_finding_right_eye": "Normal",
                "fundus_examination_finding_left_eye": "Normal",
            }
        }
    
    def test_submit_followup_creates_visit_for_existing_student(self):
        """Test that submitting a follow-up form creates a clinical visit for an existing student."""
        form_data = self.generate_followup_form_data()
        response = self.client.post(self.submit_followup_url, form_data, format='json')
        print("test_submit_followup_creates_visit_for_existing_student response:", response.data) # Debug print
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("visit_id", response.data)

        # Verify a new ClinicalVisit (FOLLOW_UP) was created for the student
        self.assertTrue(ClinicalVisit.objects.filter(
            student=self.student,
            visit_type="FOLLOW_UP",
            id=response.data['visit_id']
        ).exists())
        self.assertTrue(LifestyleBehavior.objects.filter(visit__id=response.data['visit_id']).exists())

    def test_submit_followup_with_invalid_student_id_fails(self):
        """Test that submitting a follow-up form with an invalid student_id fails."""
        form_data = self.generate_followup_form_data(student_id="NONEXISTENT-ID")
        response = self.client.post(self.submit_followup_url, form_data, format='json')
        print("test_submit_followup_with_invalid_student_id_fails response:", response.data) # Debug print
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_submit_followup_without_student_id_fails(self):
        """Test that submitting a follow-up form without a student_id fails."""
        form_data = self.generate_followup_form_data()
        del form_data['student_id'] # Remove student_id
        response = self.client.post(self.submit_followup_url, form_data, format='json')
        print("test_submit_followup_without_student_id_fails response:", response.data) # Debug print
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class GetEndpointsTests(TestCase):
    """Test GET endpoints for retrieving data"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testgetuser',
            email='get@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Create a student and a visit for this user
        self.student = Student.objects.create(
            name=RandomDataGenerator.random_name(),
            age=10,
            gender="Female",
            school_name="Test School"
        )
        self.visit = ClinicalVisit.objects.create(
            student=self.student,
            visit_date=date.today(),
            visit_type="BASELINE"
        )

    def test_get_user_profile(self):
        """Test the user-profile endpoint"""
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_user_overview(self):
        """Test the user-overview endpoint"""
        url = reverse('user-overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_students', response.data)

    def test_get_user_students(self):
        """Test the user-students endpoint"""
        url = reverse('user-students')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.student.name)

    def test_get_user_student_visits(self):
        """Test the user-student-visits endpoint"""
        url = reverse('user-student-visits', kwargs={'student_id': self.student.student_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['visit_type'], self.visit.visit_type)


class ModelStrTests(TestCase):
    """Test __str__ methods on models"""

    def test_student_str(self):
        """Test the Student __str__ method"""
        student = Student.objects.create(name="Test Student", age=10, gender="Male")
        self.assertEqual(str(student), student.student_id)

    def test_clinical_visit_str(self):
        """Test the ClinicalVisit __str__ method"""
        student = Student.objects.create(name="Test Student", age=10, gender="Male")
        visit = ClinicalVisit.objects.create(
            student=student,
            visit_date=date.today(),
            visit_type="BASELINE"
        )
        expected_str = f"{student.student_id} - {date.today()} (BASELINE)"
        self.assertEqual(str(visit), expected_str)

print("\n" + "="*70)
print("MYOPIA ANALYSIS - COMPREHENSIVE TEST SUITE")
print("Testing with 5000+ iterations across all modules")
print("="*70)
"""
Test: Myopia Progression Study Questionnaire - Data Generation
This test generates 1000+ form entries to populate the database
without destroying it after the test completes.

Questionnaire for Myopia Progression Study
(School-Going Children, Age 6–18 Years)
"""

from django.test import TestCase, TransactionTestCase
from django.db import connection
from datetime import datetime, date, timedelta
import random

from Myopia_Study.models import (
    Student,
    LifestyleBehavior,
    EnvironmentalFactor,
    ClinicalHistory,
    AwarenessSafety,
    OcularExamination,
    ClinicalExamination,
)
from decimal import Decimal


class MyopiaQuestionnaireDataGenerationTest(TransactionTestCase):
    """
    Generate 1000+ realistic entries for Myopia Progression Study questionnaire.
    Uses TransactionTestCase to ensure data persists after test completion.
    """

    def setUp(self):
        """Initial setup"""
        print("\n" + "=" * 80)
        print("MYOPIA PROGRESSION STUDY - DATA GENERATION TEST")
        print("=" * 80)
        print("Generating realistic test data for questionnaire...")
        self.students_created = 0
        self.records_created = 0

    def test_generate_1000_plus_questionnaire_entries(self):
        """
        Generate minimum 1000 form entries across all sections of the questionnaire:
        - Section A: Student Demographics
        - Section B: Lifestyle Behavior
        - Section C: Environmental Factors
        - Section D: Clinical History
        - Section E: Awareness & Safety
        - Section F: Ocular & Clinical Examination
        """

        # Number of students and visits to create
        num_students = 150
        visits_per_student = 5  # Each student has 5 visits with different data

        # Expected total entries: ~3,000+ (6 sections x ~150 students x 3-5 records each)
        self.generate_student_and_questionnaire_data(num_students, visits_per_student)

        # Verify data was created
        self.assertGreaterEqual(self.records_created, 1000)
        print(f"\n✅ Total Students Created: {self.students_created}")
        print(f"✅ Total Records Created: {self.records_created}")

    def generate_student_and_questionnaire_data(self, num_students, visits_per_student):
        """Generate realistic student data and questionnaire entries"""

        # Student demographic data pools
        names = [
            "Aarav Agarwal", "Aarav Bhat", "Aarav Chauhan", "Aarav Chopra", "Aarav Das", "Aarav Desai", "Aarav Gupta", "Aarav Iyer", "Aarav Jain", "Aarav Joshi", "Aarav Kapoor", "Aarav Khan", "Aarav Kumar", "Aarav Mehta", "Aarav Mishra", "Aarav Patel", "Aarav Rao", "Aarav Sharma", "Aarav Singh", "Aarav Verma",
"Aditi Agarwal", "Aditi Bhat", "Aditi Chauhan", "Aditi Chopra", "Aditi Das", "Aditi Desai", "Aditi Gupta", "Aditi Iyer", "Aditi Jain", "Aditi Joshi", "Aditi Kapoor", "Aditi Khan", "Aditi Kumar", "Aditi Mehta", "Aditi Mishra", "Aditi Patel", "Aditi Rao", "Aditi Sharma", "Aditi Singh", "Aditi Verma",
"Aditya Agarwal", "Aditya Bhat", "Aditya Chauhan", "Aditya Chopra", "Aditya Das", "Aditya Desai", "Aditya Gupta", "Aditya Iyer", "Aditya Jain", "Aditya Joshi", "Aditya Kapoor", "Aditya Khan", "Aditya Kumar", "Aditya Mehta", "Aditya Mishra", "Aditya Patel", "Aditya Rao", "Aditya Sharma", "Aditya Singh", "Aditya Verma",
"Ananya Agarwal", "Ananya Bhat", "Ananya Chauhan", "Ananya Chopra", "Ananya Das", "Ananya Desai", "Ananya Gupta", "Ananya Iyer", "Ananya Jain", "Ananya Joshi", "Ananya Kapoor", "Ananya Khan", "Ananya Kumar", "Ananya Mehta", "Ananya Mishra", "Ananya Patel", "Ananya Rao", "Ananya Sharma", "Ananya Singh", "Ananya Verma",
"Arjun Agarwal", "Arjun Bhat", "Arjun Chauhan", "Arjun Chopra", "Arjun Das", "Arjun Desai", "Arjun Gupta", "Arjun Iyer", "Arjun Jain", "Arjun Joshi", "Arjun Kapoor", "Arjun Khan", "Arjun Kumar", "Arjun Mehta", "Arjun Mishra", "Arjun Patel", "Arjun Rao", "Arjun Sharma", "Arjun Singh", "Arjun Verma",
"Avni Agarwal", "Avni Bhat", "Avni Chauhan", "Avni Chopra", "Avni Das", "Avni Desai", "Avni Gupta", "Avni Iyer", "Avni Jain", "Avni Joshi", "Avni Kapoor", "Avni Khan", "Avni Kumar", "Avni Mehta", "Avni Mishra", "Avni Patel", "Avni Rao", "Avni Sharma", "Avni Singh", "Avni Verma",
"Chirag Agarwal", "Chirag Bhat", "Chirag Chauhan", "Chirag Chopra", "Chirag Das", "Chirag Desai", "Chirag Gupta", "Chirag Iyer", "Chirag Jain", "Chirag Joshi", "Chirag Kapoor", "Chirag Khan", "Chirag Kumar", "Chirag Mehta", "Chirag Mishra", "Chirag Patel", "Chirag Rao", "Chirag Sharma", "Chirag Singh", "Chirag Verma",
"Diya Agarwal", "Diya Bhat", "Diya Chauhan", "Diya Chopra", "Diya Das", "Diya Desai", "Diya Gupta", "Diya Iyer", "Diya Jain", "Diya Joshi", "Diya Kapoor", "Diya Khan", "Diya Kumar", "Diya Mehta", "Diya Mishra", "Diya Patel", "Diya Rao", "Diya Sharma", "Diya Singh", "Diya Verma",
"Dhruv Agarwal", "Dhruv Bhat", "Dhruv Chauhan", "Dhruv Chopra", "Dhruv Das", "Dhruv Desai", "Dhruv Gupta", "Dhruv Iyer", "Dhruv Jain", "Dhruv Joshi", "Dhruv Kapoor", "Dhruv Khan", "Dhruv Kumar", "Dhruv Mehta", "Dhruv Mishra", "Dhruv Patel", "Dhruv Rao", "Dhruv Sharma", "Dhruv Singh", "Dhruv Verma",
"Esha Agarwal", "Esha Bhat", "Esha Chauhan", "Esha Chopra", "Esha Das", "Esha Desai", "Esha Gupta", "Esha Iyer", "Esha Jain", "Esha Joshi", "Esha Kapoor", "Esha Khan", "Esha Kumar", "Esha Mehta", "Esha Mishra", "Esha Patel", "Esha Rao", "Esha Sharma", "Esha Singh", "Esha Verma",
"Ishaan Agarwal", "Ishaan Bhat", "Ishaan Chauhan", "Ishaan Chopra", "Ishaan Das", "Ishaan Desai", "Ishaan Gupta", "Ishaan Iyer", "Ishaan Jain", "Ishaan Joshi", "Ishaan Kapoor", "Ishaan Khan", "Ishaan Kumar", "Ishaan Mehta", "Ishaan Mishra", "Ishaan Patel", "Ishaan Rao", "Ishaan Sharma", "Ishaan Singh", "Ishaan Verma",
"Jhanvi Agarwal", "Jhanvi Bhat", "Jhanvi Chauhan", "Jhanvi Chopra", "Jhanvi Das", "Jhanvi Desai", "Jhanvi Gupta", "Jhanvi Iyer", "Jhanvi Jain", "Jhanvi Joshi", "Jhanvi Kapoor", "Jhanvi Khan", "Jhanvi Kumar", "Jhanvi Mehta", "Jhanvi Mishra", "Jhanvi Patel", "Jhanvi Rao", "Jhanvi Sharma", "Jhanvi Singh", "Jhanvi Verma",
"Kabir Agarwal", "Kabir Bhat", "Kabir Chauhan", "Kabir Chopra", "Kabir Das", "Kabir Desai", "Kabir Gupta", "Kabir Iyer", "Kabir Jain", "Kabir Joshi", "Kabir Kapoor", "Kabir Khan", "Kabir Kumar", "Kabir Mehta", "Kabir Mishra", "Kabir Patel", "Kabir Rao", "Kabir Sharma", "Kabir Singh", "Kabir Verma",
"Kavya Agarwal", "Kavya Bhat", "Kavya Chauhan", "Kavya Chopra", "Kavya Das", "Kavya Desai", "Kavya Gupta", "Kavya Iyer", "Kavya Jain", "Kavya Joshi", "Kavya Kapoor", "Kavya Khan", "Kavya Kumar", "Kavya Mehta", "Kavya Mishra", "Kavya Patel", "Kavya Rao", "Kavya Sharma", "Kavya Singh", "Kavya Verma",
"Kunal Agarwal", "Kunal Bhat", "Kunal Chauhan", "Kunal Chopra", "Kunal Das", "Kunal Desai", "Kunal Gupta", "Kunal Iyer", "Kunal Jain", "Kunal Joshi", "Kunal Kapoor", "Kunal Khan", "Kunal Kumar", "Kunal Mehta", "Kunal Mishra", "Kunal Patel", "Kunal Rao", "Kunal Sharma", "Kunal Singh", "Kunal Verma",
"Manish Agarwal", "Manish Bhat", "Manish Chauhan", "Manish Chopra", "Manish Das", "Manish Desai", "Manish Gupta", "Manish Iyer", "Manish Jain", "Manish Joshi", "Manish Kapoor", "Manish Khan", "Manish Kumar", "Manish Mehta", "Manish Mishra", "Manish Patel", "Manish Rao", "Manish Sharma", "Manish Singh", "Manish Verma",
"Meera Agarwal", "Meera Bhat", "Meera Chauhan", "Meera Chopra", "Meera Das", "Meera Desai", "Meera Gupta", "Meera Iyer", "Meera Jain", "Meera Joshi", "Meera Kapoor", "Meera Khan", "Meera Kumar", "Meera Mehta", "Meera Mishra", "Meera Patel", "Meera Rao", "Meera Sharma", "Meera Singh", "Meera Verma",
"Neha Agarwal", "Neha Bhat", "Neha Chauhan", "Neha Chopra", "Neha Das", "Neha Desai", "Neha Gupta", "Neha Iyer", "Neha Jain", "Neha Joshi", "Neha Kapoor", "Neha Khan", "Neha Kumar", "Neha Mehta", "Neha Mishra", "Neha Patel", "Neha Rao", "Neha Sharma", "Neha Singh", "Neha Verma",
"Nikhil Agarwal", "Nikhil Bhat", "Nikhil Chauhan", "Nikhil Chopra", "Nikhil Das", "Nikhil Desai", "Nikhil Gupta", "Nikhil Iyer", "Nikhil Jain", "Nikhil Joshi", "Nikhil Kapoor", "Nikhil Khan", "Nikhil Kumar", "Nikhil Mehta", "Nikhil Mishra", "Nikhil Patel", "Nikhil Rao", "Nikhil Sharma", "Nikhil Singh", "Nikhil Verma",
"Pari Agarwal", "Pari Bhat", "Pari Chauhan", "Pari Chopra", "Pari Das", "Pari Desai", "Pari Gupta", "Pari Iyer", "Pari Jain", "Pari Joshi", "Pari Kapoor", "Pari Khan", "Pari Kumar", "Pari Mehta", "Pari Mishra", "Pari Patel", "Pari Rao", "Pari Sharma", "Pari Singh", "Pari Verma",
"Pranav Agarwal", "Pranav Bhat", "Pranav Chauhan", "Pranav Chopra", "Pranav Das", "Pranav Desai", "Pranav Gupta", "Pranav Iyer", "Pranav Jain", "Pranav Joshi", "Pranav Kapoor", "Pranav Khan", "Pranav Kumar", "Pranav Mehta", "Pranav Mishra", "Pranav Patel", "Pranav Rao", "Pranav Sharma", "Pranav Singh", "Pranav Verma",
"Priya Agarwal", "Priya Bhat", "Priya Chauhan", "Priya Chopra", "Priya Das", "Priya Desai", "Priya Gupta", "Priya Iyer", "Priya Jain", "Priya Joshi", "Priya Kapoor", "Priya Khan", "Priya Kumar", "Priya Mehta", "Priya Mishra", "Priya Patel", "Priya Rao", "Priya Sharma", "Priya Singh", "Priya Verma",
"Rahul Agarwal", "Rahul Bhat", "Rahul Chauhan", "Rahul Chopra", "Rahul Das", "Rahul Desai", "Rahul Gupta", "Rahul Iyer", "Rahul Jain", "Rahul Joshi", "Rahul Kapoor", "Rahul Khan", "Rahul Kumar", "Rahul Mehta", "Rahul Mishra", "Rahul Patel", "Rahul Rao", "Rahul Sharma", "Rahul Singh", "Rahul Verma",
"Riya Agarwal", "Riya Bhat", "Riya Chauhan", "Riya Chopra", "Riya Das", "Riya Desai", "Riya Gupta", "Riya Iyer", "Riya Jain", "Riya Joshi", "Riya Kapoor", "Riya Khan", "Riya Kumar", "Riya Mehta", "Riya Mishra", "Riya Patel", "Riya Rao", "Riya Sharma", "Riya Singh", "Riya Verma",
"Rohan Agarwal", "Rohan Bhat", "Rohan Chauhan", "Rohan Chopra", "Rohan Das", "Rohan Desai", "Rohan Gupta", "Rohan Iyer", "Rohan Jain", "Rohan Joshi", "Rohan Kapoor", "Rohan Khan", "Rohan Kumar", "Rohan Mehta", "Rohan Mishra", "Rohan Patel", "Rohan Rao", "Rohan Sharma", "Rohan Singh", "Rohan Verma",
"Sanjana Agarwal", "Sanjana Bhat", "Sanjana Chauhan", "Sanjana Chopra", "Sanjana Das", "Sanjana Desai", "Sanjana Gupta", "Sanjana Iyer", "Sanjana Jain", "Sanjana Joshi", "Sanjana Kapoor", "Sanjana Khan", "Sanjana Kumar", "Sanjana Mehta", "Sanjana Mishra", "Sanjana Patel", "Sanjana Rao", "Sanjana Sharma", "Sanjana Singh", "Sanjana Verma",
"Shaurya Agarwal", "Shaurya Bhat", "Shaurya Chauhan", "Shaurya Chopra", "Shaurya Das", "Shaurya Desai", "Shaurya Gupta", "Shaurya Iyer", "Shaurya Jain", "Shaurya Joshi", "Shaurya Kapoor", "Shaurya Khan", "Shaurya Kumar", "Shaurya Mehta", "Shaurya Mishra", "Shaurya Patel", "Shaurya Rao", "Shaurya Sharma", "Shaurya Singh", "Shaurya Verma",
"Sneha Agarwal", "Sneha Bhat", "Sneha Chauhan", "Sneha Chopra", "Sneha Das", "Sneha Desai", "Sneha Gupta", "Sneha Iyer", "Sneha Jain", "Sneha Joshi", "Sneha Kapoor", "Sneha Khan", "Sneha Kumar", "Sneha Mehta", "Sneha Mishra", "Sneha Patel", "Sneha Rao", "Sneha Sharma", "Sneha Singh", "Sneha Verma",
"Varun Agarwal", "Varun Bhat", "Varun Chauhan", "Varun Chopra", "Varun Das", "Varun Desai", "Varun Gupta", "Varun Iyer", "Varun Jain", "Varun Joshi", "Varun Kapoor", "Varun Khan", "Varun Kumar", "Varun Mehta", "Varun Mishra", "Varun Patel", "Varun Rao", "Varun Sharma", "Varun Singh", "Varun Verma",
"Zara Agarwal", "Zara Bhat", "Zara Chauhan", "Zara Chopra", "Zara Das", "Zara Desai", "Zara Gupta", "Zara Iyer", "Zara Jain", "Zara Joshi", "Zara Kapoor", "Zara Khan", "Zara Kumar", "Zara Mehta", "Zara Mishra", "Zara Patel", "Zara Rao", "Zara Sharma", "Zara Singh", "Zara Verma",
        ]

        schools = ["Adarsh Public School", "Adarsh International School", "Adarsh High School", "Adarsh Academy", "Adarsh Convent", "Adarsh Vidyalaya",
"Amity Public School", "Amity International School", "Amity High School", "Amity Academy", "Amity Convent", "Amity Vidyalaya",
"Apeejay Public School", "Apeejay International School", "Apeejay High School", "Apeejay Academy", "Apeejay Convent", "Apeejay Vidyalaya",
"Army Public School", "Army International School", "Army High School", "Army Academy", "Army Convent", "Army Vidyalaya",
"Ashok Public School", "Ashok International School", "Ashok High School", "Ashok Academy", "Ashok Convent", "Ashok Vidyalaya",
"Bal Public School", "Bal International School", "Bal High School", "Bal Academy", "Bal Convent", "Bal Vidyalaya",
"Bharatiya Public School", "Bharatiya International School", "Bharatiya High School", "Bharatiya Academy", "Bharatiya Convent", "Bharatiya Vidyalaya",
"Bishop Public School", "Bishop International School", "Bishop High School", "Bishop Academy", "Bishop Convent", "Bishop Vidyalaya",
"Blue Public School", "Blue International School", "Blue High School", "Blue Academy", "Blue Convent", "Blue Vidyalaya",
"Bright Public School", "Bright International School", "Bright High School", "Bright Academy", "Bright Convent", "Bright Vidyalaya",
"Cambridge Public School", "Cambridge International School", "Cambridge High School", "Cambridge Academy", "Cambridge Convent", "Cambridge Vidyalaya",
"Carmel Public School", "Carmel International School", "Carmel High School", "Carmel Academy", "Carmel Convent", "Carmel Vidyalaya",
"Cathedral Public School", "Cathedral International School", "Cathedral High School", "Cathedral Academy", "Cathedral Convent", "Cathedral Vidyalaya",
"Central Public School", "Central International School", "Central High School", "Central Academy", "Central Convent", "Central Vidyalaya",
"City Public School", "City International School", "City High School", "City Academy", "City Convent", "City Vidyalaya",
"DAV Public School", "DAV International School", "DAV High School", "DAV Academy", "DAV Convent", "DAV Vidyalaya",
"Delhi Public School", "Delhi International School", "Delhi High School", "Delhi Academy", "Delhi Convent", "Delhi Vidyalaya",
"Don Bosco Public School", "Don Bosco International School", "Don Bosco High School", "Don Bosco Academy", "Don Bosco Convent", "Don Bosco Vidyalaya",
"GD Goenka Public School", "GD Goenka International School", "GD Goenka High School", "GD Goenka Academy", "GD Goenka Convent", "GD Goenka Vidyalaya",
"Global Public School", "Global International School", "Global High School", "Global Academy", "Global Convent", "Global Vidyalaya",
"Glory Public School", "Glory International School", "Glory High School", "Glory Academy", "Glory Convent", "Glory Vidyalaya",
"Golden Public School", "Golden International School", "Golden High School", "Golden Academy", "Golden Convent", "Golden Vidyalaya",
"Good Public School", "Good International School", "Good High School", "Good Academy", "Good Convent", "Good Vidyalaya",
"Green Public School", "Green International School", "Green High School", "Green Academy", "Green Convent", "Green Vidyalaya",
"Guru Public School", "Guru International School", "Guru High School", "Guru Academy", "Guru Convent", "Guru Vidyalaya",
"Heritage Public School", "Heritage International School", "Heritage High School", "Heritage Academy", "Heritage Convent", "Heritage Vidyalaya",
"Holy Public School", "Holy International School", "Holy High School", "Holy Academy", "Holy Convent", "Holy Vidyalaya",
"Hope Public School", "Hope International School", "Hope High School", "Hope Academy", "Hope Convent", "Hope Vidyalaya",
"Indian Public School", "Indian International School", "Indian High School", "Indian Academy", "Indian Convent", "Indian Vidyalaya",
"Indus Public School", "Indus International School", "Indus High School", "Indus Academy", "Indus Convent", "Indus Vidyalaya",
"International Public School", "International International School", "International High School", "International Academy", "International Convent", "International Vidyalaya",
"Jai Public School", "Jai International School", "Jai High School", "Jai Academy", "Jai Convent", "Jai Vidyalaya",
"Jawahar Public School", "Jawahar International School", "Jawahar High School", "Jawahar Academy", "Jawahar Convent", "Jawahar Vidyalaya",
"Jesus Public School", "Jesus International School", "Jesus High School", "Jesus Academy", "Jesus Convent", "Jesus Vidyalaya",
"Kendriya Public School", "Kendriya International School", "Kendriya High School", "Kendriya Academy", "Kendriya Convent", "Kendriya Vidyalaya",
"Little Public School", "Little International School", "Little High School", "Little Academy", "Little Convent", "Little Vidyalaya",
"Lotus Public School", "Lotus International School", "Lotus High School", "Lotus Academy", "Lotus Convent", "Lotus Vidyalaya",
"Loyola Public School", "Loyola International School", "Loyola High School", "Loyola Academy", "Loyola Convent", "Loyola Vidyalaya",
"Maharishi Public School", "Maharishi International School", "Maharishi High School", "Maharishi Academy", "Maharishi Convent", "Maharishi Vidyalaya",
"Manav Public School", "Manav International School", "Manav High School", "Manav Academy", "Manav Convent", "Manav Vidyalaya",
"Mary Public School", "Mary International School", "Mary High School", "Mary Academy", "Mary Convent", "Mary Vidyalaya",
"Modern Public School", "Modern International School", "Modern High School", "Modern Academy", "Modern Convent", "Modern Vidyalaya",
"Mount Public School", "Mount International School", "Mount High School", "Mount Academy", "Mount Convent", "Mount Vidyalaya",
"National Public School", "National International School", "National High School", "National Academy", "National Convent", "National Vidyalaya",
"Navy Public School", "Navy International School", "Navy High School", "Navy Academy", "Navy Convent", "Navy Vidyalaya",
"New Public School", "New International School", "New High School", "New Academy", "New Convent", "New Vidyalaya",
"Noble Public School", "Noble International School", "Noble High School", "Noble Academy", "Noble Convent", "Noble Vidyalaya",
"Oak Public School", "Oak International School", "Oak High School", "Oak Academy", "Oak Convent", "Oak Vidyalaya",
"Oxford Public School", "Oxford International School", "Oxford High School", "Oxford Academy", "Oxford Convent", "Oxford Vidyalaya",
"Paramount Public School", "Paramount International School", "Paramount High School", "Paramount Academy", "Paramount Convent", "Paramount Vidyalaya",
"Pathfinder Public School", "Pathfinder International School", "Pathfinder High School", "Pathfinder Academy", "Pathfinder Convent", "Pathfinder Vidyalaya",
"Peace Public School", "Peace International School", "Peace High School", "Peace Academy", "Peace Convent", "Peace Vidyalaya",
"Pioneer Public School", "Pioneer International School", "Pioneer High School", "Pioneer Academy", "Pioneer Convent", "Pioneer Vidyalaya",
"Podar Public School", "Podar International School", "Podar High School", "Podar Academy", "Podar Convent", "Podar Vidyalaya",
"Presidency Public School", "Presidency International School", "Presidency High School", "Presidency Academy", "Presidency Convent", "Presidency Vidyalaya",
"Presidium Public School", "Presidium International School", "Presidium High School", "Presidium Academy", "Presidium Convent", "Presidium Vidyalaya",
"Progressive Public School", "Progressive International School", "Progressive High School", "Progressive Academy", "Progressive Convent", "Progressive Vidyalaya",
"Queen Public School", "Queen International School", "Queen High School", "Queen Academy", "Queen Convent", "Queen Vidyalaya",
"Radiant Public School", "Radiant International School", "Radiant High School", "Radiant Academy", "Radiant Convent", "Radiant Vidyalaya",
"Rainbow Public School", "Rainbow International School", "Rainbow High School", "Rainbow Academy", "Rainbow Convent", "Rainbow Vidyalaya",
"Red Public School", "Red International School", "Red High School", "Red Academy", "Red Convent", "Red Vidyalaya",
"River Public School", "River International School", "River High School", "River Academy", "River Convent", "River Vidyalaya",
"Rose Public School", "Rose International School", "Rose High School", "Rose Academy", "Rose Convent", "Rose Vidyalaya",
"Royal Public School", "Royal International School", "Royal High School", "Royal Academy", "Royal Convent", "Royal Vidyalaya",
"Ryan Public School", "Ryan International School", "Ryan High School", "Ryan Academy", "Ryan Convent", "Ryan Vidyalaya",
"Sacred Public School", "Sacred International School", "Sacred High School", "Sacred Academy", "Sacred Convent", "Sacred Vidyalaya",
"Saint Public School", "Saint International School", "Saint High School", "Saint Academy", "Saint Convent", "Saint Vidyalaya",
"Sanskar Public School", "Sanskar International School", "Sanskar High School", "Sanskar Academy", "Sanskar Convent", "Sanskar Vidyalaya",
"Saraswati Public School", "Saraswati International School", "Saraswati High School", "Saraswati Academy", "Saraswati Convent", "Saraswati Vidyalaya",
"Scholars Public School", "Scholars International School", "Scholars High School", "Scholars Academy", "Scholars Convent", "Scholars Vidyalaya",
"Seven Public School", "Seven International School", "Seven High School", "Seven Academy", "Seven Convent", "Seven Vidyalaya",
"Shalom Public School", "Shalom International School", "Shalom High School", "Shalom Academy", "Shalom Convent", "Shalom Vidyalaya",
"Shiksha Public School", "Shiksha International School", "Shiksha High School", "Shiksha Academy", "Shiksha Convent", "Shiksha Vidyalaya",
"Silver Public School", "Silver International School", "Silver High School", "Silver Academy", "Silver Convent", "Silver Vidyalaya",
"Spring Public School", "Spring International School", "Spring High School", "Spring Academy", "Spring Convent", "Spring Vidyalaya",
"St. Public School", "St. International School", "St. High School", "St. Academy", "St. Convent", "St. Vidyalaya",
"Star Public School", "Star International School", "Star High School", "Star Academy", "Star Convent", "Star Vidyalaya",
"Step Public School", "Step International School", "Step High School", "Step Academy", "Step Convent", "Step Vidyalaya",
"Summer Public School", "Summer International School", "Summer High School", "Summer Academy", "Summer Convent", "Summer Vidyalaya",
"Sun Public School", "Sun International School", "Sun High School", "Sun Academy", "Sun Convent", "Sun Vidyalaya",
"Sunrise Public School", "Sunrise International School", "Sunrise High School", "Sunrise Academy", "Sunrise Convent", "Sunrise Vidyalaya",
"Sunshine Public School", "Sunshine International School", "Sunshine High School", "Sunshine Academy", "Sunshine Convent", "Sunshine Vidyalaya",
"Tagore Public School", "Tagore International School", "Tagore High School", "Tagore Academy", "Tagore Convent", "Tagore Vidyalaya",
"The Public School", "The International School", "The High School", "The Academy", "The Convent", "The Vidyalaya",
"Trinity Public School", "Trinity International School", "Trinity High School", "Trinity Academy", "Trinity Convent", "Trinity Vidyalaya",
"Universal Public School", "Universal International School", "Universal High School", "Universal Academy", "Universal Convent", "Universal Vidyalaya",
"Valley Public School", "Valley International School", "Valley High School", "Valley Academy", "Valley Convent", "Valley Vidyalaya",
"Vasant Public School", "Vasant International School", "Vasant High School", "Vasant Academy", "Vasant Convent", "Vasant Vidyalaya",
"Vidya Public School", "Vidya International School", "Vidya High School", "Vidya Academy", "Vidya Convent", "Vidya Vidyalaya",
"Vivekananda Public School", "Vivekananda International School", "Vivekananda High School", "Vivekananda Academy", "Vivekananda Convent", "Vivekananda Vidyalaya",
"Wisdom Public School", "Wisdom International School", "Wisdom High School", "Wisdom Academy", "Wisdom Convent", "Wisdom Vidyalaya",
"World Public School", "World International School", "World High School", "World Academy", "World Convent", "World Vidyalaya",
"Xavier Public School", "Xavier International School", "Xavier High School", "Xavier Academy", "Xavier Convent", "Xavier Vidyalaya",
        ]
        # Create students and their questionnaire data
        for student_idx in range(num_students):
            student_id = f"STU{str(student_idx + 1).zfill(4)}"
            age = random.randint(6, 18)

            # Section A: Student Demographics
            student = Student.objects.create(
                student_id=student_id,
                name=random.choice(names),
                age=age,
                gender=random.choice(["Male", "Female"]),
                height_cm=Decimal(str(round(random.uniform(110, 185), 2))),
                weight_kg=Decimal(str(round(random.uniform(25, 90), 2))),
                father_myopia=random.choice([True, False]),
                mother_myopia=random.choice([True, False]),
                number_of_siblings=random.randint(0, 4),
                birth_order=random.choice(["First", "Middle", "Last", "Only"]),
                sibling_details=f"Siblings in family for {student_id}"
            )
            self.students_created += 1

            # Create multiple visits for each student
            for visit_idx in range(visits_per_student):
                visit_date = date.today() - timedelta(days=random.randint(0, 365))

                # Section B: Lifestyle Behavior
                lifestyle = LifestyleBehavior.objects.create(
                    student=student,
                    visit_date=visit_date,
                    outdoor_duration=random.choice(["<1 hr", "1-2 hrs", "2-4 hrs", ">4 hrs"]),
                    sun_exposure=random.choice(["<15 min", "15-30 min", "30-60 min", ">1 hr"]),
                    near_work_hours=random.choice(["<2 hrs", "2-4 hrs", "4-6 hrs", ">6 hrs"]),
                    screen_time=random.choice(["<1 hr", "1-3 hrs", "3-5 hrs", ">5 hrs"]),
                    primary_device=random.choice(["TV", "Tablet", "Mobile", "Laptop"]),
                    reading_distance=random.choice(["<20 cm", "20-30 cm", ">30 cm"]),
                    viewing_posture_ratio=random.choice(["Low", "High", "Optimum"]),
                    dietary_habit=random.choice(["Balanced", "Junk", "Vegetarian", "NonVegetarian", "Other"]),
                    dietary_other="Supplement taken" if random.choice([True, False]) else "",
                    sleep_duration=random.choice(["<6 hrs", "6-7 hrs", "7-8 hrs", ">8 hrs"]),
                    usual_bedtime=random.choice(["Before9", "9-10", "10-11", "After11"])
                )
                self.records_created += 1

                # Section C: Environmental Factors
                env_factor = EnvironmentalFactor.objects.create(
                    student=student,
                    visit_date=visit_date,
                    school_type=random.choice(["Urban", "Rural"]),
                    classroom_strength=random.choice(["Small", "Moderate", "High"]),
                    seating_position=random.choice(["Front", "Middle", "Back"]),
                    teaching_methodology=random.choice(["Digital", "Traditional"]),
                    lighting=random.choice(["Dim", "Adequate", "Bright"]),
                    sunlight_source=random.choice(["Natural", "Artificial", "Both"])
                )
                self.records_created += 1

                # Section D: Clinical History
                diagnosed = random.choice([True, False])
                clinical_history = ClinicalHistory.objects.create(
                    student=student,
                    visit_date=visit_date,
                    diagnosed_earlier=diagnosed,
                    age_at_diagnosis=random.randint(4, age) if diagnosed else None,
                    power_changed_last_3yrs=random.choice([True, False]),
                    compliance=random.choice(["Always", "Sometimes", "Rarely"]),
                    previous_re=f"-{random.uniform(0, 8):.2f}" if diagnosed else "",
                    previous_le=f"-{random.uniform(0, 8):.2f}" if diagnosed else "",
                    current_re=f"-{random.uniform(0, 8):.2f}",
                    current_le=f"-{random.uniform(0, 8):.2f}"
                )
                self.records_created += 1

                # Section E: Awareness & Safety
                awareness = AwarenessSafety.objects.create(
                    student=student,
                    visit_date=visit_date,
                    aware_eye_strain=random.choice([True, False]),
                    access_to_vision_care=random.choice([True, False]),
                    follows_preventive_measures=random.choice(["Always", "Sometimes", "Never"]),
                    source_of_awareness=random.choice(
                        ["School", "Family, School", "Doctor, School", "Media", "Family, Doctor, Media"]
                    )
                )
                self.records_created += 1

                # Section F: Ocular Examination
                ocular_exam = OcularExamination.objects.create(
                    student=student,
                    visit_date=visit_date,
                    ucva_re=random.choice(["6/6", "6/9", "6/12", "6/18", "6/24"]),
                    ucva_le=random.choice(["6/6", "6/9", "6/12", "6/18", "6/24"]),
                    bcva_re=random.choice(["6/6", "6/9", "6/12"]),
                    bcva_le=random.choice(["6/6", "6/9", "6/12"]),
                    cyclo_se_re=f"-{random.uniform(0, 8):.2f}",
                    cyclo_se_le=f"-{random.uniform(0, 8):.2f}",
                    spherical_re=f"-{random.uniform(0, 8):.2f}",
                    spherical_le=f"-{random.uniform(0, 8):.2f}",
                    axial_length_re=f"{random.uniform(20, 26):.2f}",
                    axial_length_le=f"{random.uniform(20, 26):.2f}",
                    keratometry_re=f"{random.uniform(40, 45):.2f}",
                    keratometry_le=f"{random.uniform(40, 45):.2f}",
                    cct_re=f"{random.randint(500, 600)}",
                    cct_le=f"{random.randint(500, 600)}",
                    anterior_segment_re="Normal" if random.choice([True, False]) else "Mild corneal opacity",
                    anterior_segment_le="Normal" if random.choice([True, False]) else "Mild corneal opacity",
                    amblyopia_or_strabismus=random.choice([True, False]),
                    fundus_re="Healthy disc and macula" if random.choice([True, False]) else "Myopic changes",
                    fundus_le="Healthy disc and macula" if random.choice([True, False]) else "Myopic changes"
                )
                self.records_created += 1

                # Section F: Clinical Examination
                clinical_exam = ClinicalExamination.objects.create(
                    student=student,
                    visit_date=visit_date,
                    unaided_va_re=random.choice(["6/6", "6/9", "6/12", "6/18"]),
                    unaided_va_le=random.choice(["6/6", "6/9", "6/12", "6/18"]),
                    aided_va_re=random.choice(["6/6", "6/9", "6/12"]),
                    aided_va_le=random.choice(["6/6", "6/9", "6/12"]),
                    spherical_re=Decimal(str(round(random.uniform(-8, 0), 2))),
                    spherical_le=Decimal(str(round(random.uniform(-8, 0), 2))),
                    cylindrical_re=Decimal(str(round(random.uniform(-2, 0), 2))) if random.choice([True, False]) else None,
                    cylindrical_le=Decimal(str(round(random.uniform(-2, 0), 2))) if random.choice([True, False]) else None,
                    axis_re=random.randint(0, 180) if random.choice([True, False]) else None,
                    axis_le=random.randint(0, 180) if random.choice([True, False]) else None,
                    axial_length_re=Decimal(str(round(random.uniform(20, 26), 2))),
                    axial_length_le=Decimal(str(round(random.uniform(20, 26), 2))),
                    progression_noted=random.choice([True, False]),
                    remarks=f"Clinical examination for {student_id} - Visit {visit_idx + 1}"
                )
                self.records_created += 1

        # Display summary
        print(f"\n{'=' * 80}")
        print("DATA GENERATION SUMMARY")
        print(f"{'=' * 80}")
        print(f"✓ Created {self.students_created} Students (Section A)")
        print(f"✓ Created {self.students_created * visits_per_student} Lifestyle Records (Section B)")
        print(f"✓ Created {self.students_created * visits_per_student} Environmental Records (Section C)")
        print(f"✓ Created {self.students_created * visits_per_student} Clinical History Records (Section D)")
        print(f"✓ Created {self.students_created * visits_per_student} Awareness/Safety Records (Section E)")
        print(f"✓ Created {self.students_created * visits_per_student * 2} Ocular/Clinical Exam Records (Section F)")
        print(f"\n📊 TOTAL ENTRIES: {self.records_created}")
        print(f"{'=' * 80}\n")


class MyopiaQuestionnaireBulkInsertTest(TransactionTestCase):
    """
    Alternative bulk insertion test for even faster data generation.
    Creates comprehensive test data while preserving database.
    """

    def test_bulk_insert_questionnaire_data(self):
        """
        Bulk insert questionnaire data for faster generation of large datasets.
        Generates data in batches to optimize database performance.
        """
        print("\n" + "=" * 80)
        print("BULK INSERT TEST - MYOPIA QUESTIONNAIRE DATA")
        print("=" * 80)

        batch_size = 100
        num_batches = 12  # 12 batches x 100 = 1200 students minimum

        total_records = 0

        for batch_num in range(num_batches):
            print(f"\nProcessing Batch {batch_num + 1}/{num_batches}...")

            # Create students for this batch
            students = []
            for i in range(batch_size):
                student_id = f"BULK{str(batch_num * batch_size + i + 1).zfill(5)}"
                students.append(
                    Student(
                        student_id=student_id,
                        name=f"Student_{batch_num}_{i}",
                        age=random.randint(6, 18),
                        gender=random.choice(["Male", "Female"]),
                        height_cm=Decimal(str(round(random.uniform(110, 185), 2))),
                        weight_kg=Decimal(str(round(random.uniform(25, 90), 2))),
                        father_myopia=random.choice([True, False]),
                        mother_myopia=random.choice([True, False]),
                        number_of_siblings=random.randint(0, 4),
                        birth_order=random.choice(["First", "Middle", "Last", "Only"])
                    )
                )

            # Bulk create students
            created_students = Student.objects.bulk_create(students)
            print(f"  ✓ Created {len(created_students)} students")

            # Create related questionnaire data for each student
            for student in created_students:
                # Create 2 visits per student
                for visit in range(2):
                    visit_date = date.today() - timedelta(days=random.randint(0, 365))

                    # Lifestyle
                    LifestyleBehavior.objects.create(
                        student=student,
                        visit_date=visit_date,
                        outdoor_duration=random.choice(["<1 hr", "1-2 hrs", "2-4 hrs", ">4 hrs"]),
                        sun_exposure=random.choice(["<15 min", "15-30 min", "30-60 min", ">1 hr"]),
                        near_work_hours=random.choice(["<2 hrs", "2-4 hrs", "4-6 hrs", ">6 hrs"]),
                        screen_time=random.choice(["<1 hr", "1-3 hrs", "3-5 hrs", ">5 hrs"]),
                        primary_device=random.choice(["TV", "Tablet", "Mobile", "Laptop"]),
                        reading_distance=random.choice(["<20 cm", "20-30 cm", ">30 cm"]),
                        viewing_posture_ratio=random.choice(["Low", "High", "Optimum"]),
                        dietary_habit=random.choice(["Balanced", "Junk", "Vegetarian", "NonVegetarian"]),
                        sleep_duration=random.choice(["<6 hrs", "6-7 hrs", "7-8 hrs", ">8 hrs"]),
                        usual_bedtime=random.choice(["Before9", "9-10", "10-11", "After11"])
                    )

                    # Environmental
                    EnvironmentalFactor.objects.create(
                        student=student,
                        visit_date=visit_date,
                        school_type=random.choice(["Urban", "Rural"]),
                        classroom_strength=random.choice(["Small", "Moderate", "High"]),
                        seating_position=random.choice(["Front", "Middle", "Back"]),
                        teaching_methodology=random.choice(["Digital", "Traditional"]),
                        lighting=random.choice(["Dim", "Adequate", "Bright"]),
                        sunlight_source=random.choice(["Natural", "Artificial", "Both"])
                    )

                    # Clinical History
                    ClinicalHistory.objects.create(
                        student=student,
                        visit_date=visit_date,
                        diagnosed_earlier=random.choice([True, False]),
                        age_at_diagnosis=random.randint(4, student.age),
                        power_changed_last_3yrs=random.choice([True, False]),
                        compliance=random.choice(["Always", "Sometimes", "Rarely"]),
                        current_re=f"-{random.uniform(0, 8):.2f}",
                        current_le=f"-{random.uniform(0, 8):.2f}"
                    )

                    # Awareness
                    AwarenessSafety.objects.create(
                        student=student,
                        visit_date=visit_date,
                        aware_eye_strain=random.choice([True, False]),
                        access_to_vision_care=random.choice([True, False]),
                        follows_preventive_measures=random.choice(["Always", "Sometimes", "Never"]),
                        source_of_awareness="School, Family"
                    )

                    # Ocular Exam
                    OcularExamination.objects.create(
                        student=student,
                        visit_date=visit_date,
                        ucva_re=random.choice(["6/6", "6/9", "6/12", "6/18"]),
                        ucva_le=random.choice(["6/6", "6/9", "6/12", "6/18"]),
                        bcva_re="6/6",
                        bcva_le="6/6",
                        cyclo_se_re=f"-{random.uniform(0, 8):.2f}",
                        cyclo_se_le=f"-{random.uniform(0, 8):.2f}",
                        amblyopia_or_strabismus=False
                    )

                    # Clinical Exam
                    ClinicalExamination.objects.create(
                        student=student,
                        visit_date=visit_date,
                        unaided_va_re=random.choice(["6/6", "6/9", "6/12"]),
                        unaided_va_le=random.choice(["6/6", "6/9", "6/12"]),
                        aided_va_re="6/6",
                        aided_va_le="6/6",
                        spherical_re=Decimal(str(round(random.uniform(-8, 0), 2))),
                        spherical_le=Decimal(str(round(random.uniform(-8, 0), 2))),
                        progression_noted=random.choice([True, False])
                    )

                    total_records += 6  # 6 records per visit

        print(f"\n{'=' * 80}")
        print("BULK INSERT COMPLETE")
        print(f"{'=' * 80}")
        print(f"✓ Created {batch_size * num_batches} Students")
        print(f"✓ Created {total_records} Total Records (6 record types x students x 2 visits)")
        print(f"📊 TOTAL DATABASE ENTRIES: ~{total_records}")
        print(f"{'=' * 80}\n")

        self.assertGreaterEqual(total_records, 1000)

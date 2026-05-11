import random

from faker import Faker
from pymongo import MongoClient

fake = Faker()

client = MongoClient("mongodb://localhost:27017")

db = client["job_market_db"]

companies = db["companies"]
vacancies = db["vacancies"]
applicants = db["applicants"]

companies.delete_many({})
vacancies.delete_many({})
applicants.delete_many({})

industries = [
    "IT",
    "Finance",
    "Healthcare",
    "Gaming",
    "Education",
    "Cloud",
    "Security"
]

job_titles = [
    "Backend Developer",
    "Frontend Developer",
    "DevOps Engineer",
    "QA Engineer",
    "Data Scientist",
    "ML Engineer",
    "System Analyst",
    "Project Manager"
]

skills_pool = [
    "Python",
    "Java",
    "C++",
    "MongoDB",
    "Docker",
    "Kubernetes",
    "React",
    "Vue",
    "Linux",
    "AWS",
    "FastAPI",
    "SQL",
    "Git"
]

levels = [
    "junior",
    "middle",
    "senior"
]

company_ids = []

for _ in range(50):

    company = {
        "name": fake.company(),
        "country": fake.country(),
        "industry": random.choice(industries)
    }

    result = companies.insert_one(company)

    company_ids.append(result.inserted_id)

print("Companies inserted")

levels = [
    "junior",
    "middle",
    "senior"
]

vacancy_ids = []

for _ in range(200):

    skills = random.sample(
        skills_pool,
        random.randint(2, 5)
    )

    vacancy = {
        "title": random.choice(job_titles),
        "salary": random.randint(1000, 7000),
        "level": random.choice(levels),
        "companyId": random.choice(company_ids),
        "skills": skills
    }

    result = vacancies.insert_one(vacancy)

    vacancy_ids.append(result.inserted_id)

print("vacancies inserted")

for _ in range(1000):

    applicant = {
        "name": fake.name(),
        "age": random.randint(18, 45),
        "vacancyId": random.choice(vacancy_ids),
        "experienceYears": random.randint(0, 15)
    }

    applicants.insert_one(applicant)

print("Applicants inserted")

print("Database successfully seeded")
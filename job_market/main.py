from fastapi import FastAPI
from bson import ObjectId
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017")

db = client["job_market_db"]

companies = db["companies"]
vacancies = db["vacancies"]
applicants = db["applicants"]


def serialize(doc):

    doc["_id"] = str(doc["_id"])

    if "companyId" in doc:
        doc["companyId"] = str(doc["companyId"])

    if "vacancyId" in doc:
        doc["vacancyId"] = str(doc["vacancyId"])

    return doc


@app.get("/companies")
def get_companies():
    return [serialize(c) for c in companies.find()]


@app.post("/companies")
def create_company(company: dict):

    result = companies.insert_one(company)

    company["_id"] = str(result.inserted_id)

    return company


@app.delete("/companies/{company_id}")
def delete_company(company_id: str):

    companies.delete_one({
        "_id": ObjectId(company_id)
    })

    return {"message": "deleted"}

@app.get("/vacancies")
def get_vacancies():
    return [serialize(v) for v in vacancies.find()]


@app.post("/vacancies")
def create_vacancy(vacancy: dict):

    vacancy["companyId"] = ObjectId(vacancy["companyId"])

    result = vacancies.insert_one(vacancy)

    vacancy["_id"] = str(result.inserted_id)
    vacancy["companyId"] = str(vacancy["companyId"])

    return vacancy


@app.delete("/vacancies/{vacancy_id}")
def delete_vacancy(vacancy_id: str):

    vacancies.delete_one({
        "_id": ObjectId(vacancy_id)
    })

    return {"message": "deleted"}


@app.get("/applicants")
def get_applicants():
    return [serialize(a) for a in applicants.find()]


@app.post("/applicants")
def create_applicant(applicant: dict):

    applicant["vacancyId"] = ObjectId(applicant["vacancyId"])

    result = applicants.insert_one(applicant)

    applicant["_id"] = str(result.inserted_id)
    applicant["vacancyId"] = str(applicant["vacancyId"])

    return applicant


@app.delete("/applicants/{applicant_id}")
def delete_applicant(applicant_id: str):

    applicants.delete_one({
        "_id": ObjectId(applicant_id)
    })

    return {"message": "deleted"}


@app.get("/companies-with-vacancies")
def companies_with_vacancies():

    result = companies.aggregate([
        {
            "$lookup": {
                "from": "vacancies",
                "localField": "_id",
                "foreignField": "companyId",
                "as": "vacancies"
            }
        }
    ])

    output = []

    for company in result:

        company["_id"] = str(company["_id"])

        for vacancy in company["vacancies"]:

            vacancy["_id"] = str(vacancy["_id"])
            vacancy["companyId"] = str(vacancy["companyId"])

        output.append(company)

    return output
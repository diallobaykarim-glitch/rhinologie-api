# API Rhinologie FastAPI/PostgreSQL

API médicale de base pour un projet de rhinologie : patients, consultations, scores cliniques et examens endoscopiques.

## Démarrage avec Docker

```powershell
cd C:\Users\UTILISATEUR\rhinologie-api
docker compose up --build
```

API : http://localhost:8000  
Documentation Swagger : http://localhost:8000/docs

## Démarrage local

```powershell
cd C:\Users\UTILISATEUR\rhinologie-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Il faut une base PostgreSQL disponible et compatible avec la variable `DATABASE_URL`.

## Endpoints principaux

- `GET /health`
- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}`
- `PATCH /api/v1/patients/{patient_id}`
- `DELETE /api/v1/patients/{patient_id}`
- `POST /api/v1/consultations`
- `GET /api/v1/consultations?patient_id=1`
- `POST /api/v1/endoscopy`
- `GET /api/v1/endoscopy?patient_id=1`
- `GET /api/v1/statistics`
- `GET /api/v1/statistics/graphs`

## Exemple patient

```json
{
  "medical_record_number": "RHI-0001",
  "first_name": "Amina",
  "last_name": "Benali",
  "date_of_birth": "1984-03-12",
  "sex": "female",
  "phone": "+33123456789",
  "email": "amina.benali@example.com"
}
```

## Note sécurité médicale

Ce socle ne doit pas être utilisé en production avec des données réelles sans authentification, chiffrement, journalisation d'accès, politique RGPD/HIPAA adaptée, sauvegardes et revue de sécurité.

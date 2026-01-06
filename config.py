class Config:
    SECRET_KEY = "dev-secret-key-change-me"

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:Surya%40000777@localhost:5432/blood_bank_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

import pyodbc
from pymongo import MongoClient
from decimal import Decimal
from datetime import date, time, datetime
import logging

# Setup logging
logging.basicConfig(filename='migration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_for_mongo(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (date, time, datetime)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_for_mongo(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_for_mongo(i) for i in obj]
    else:
        return obj

def migrate_data():
    try:
        # SQL Server connection
        sql_conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=Dardans-HP\\SQLEXPRESS;"
            "DATABASE=ITCompany;"
            "Trusted_Connection=yes;"
        )
        cursor = sql_conn.cursor()

        # MongoDB connection
        mongo_client = MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["IT-Company"]
        client_collection = mongo_db["klientet"]
        project_collection = mongo_db["projektet"]
        department_collection = mongo_db["departamentet"]

        # Migrate klientët with embedded kontratа and projekti
        cursor.execute("SELECT * FROM klientët")
        clients = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        for client in clients:
            kid = client['kid']
            cursor.execute("SELECT * FROM kontratа WHERE klientët_kid = ?", kid)
            contracts = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

            for kontrata in contracts:
                pid = kontrata["projekti_pid"]
                cursor.execute("SELECT * FROM projekti WHERE pid = ?", pid)
                project = cursor.fetchone()
                if project:
                    project_columns = [col[0] for col in cursor.description]
                    kontrata["projekti"] = dict(zip(project_columns, project))

            client_doc = {
                **client,
                "kontratat": contracts
            }
            client_collection.insert_one(convert_for_mongo(client_doc))

        # Migrate projektet with embedded punëtori via punonnperprojektin
        cursor.execute("SELECT * FROM projekti")
        projects = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        for project in projects:
            pid = project["pid"]
            cursor.execute("SELECT * FROM punonnperprojektin WHERE projekti_pid = ?", pid)
            pun_ids = [row[0] for row in cursor.fetchall()]

            punetore = []
            for punid in pun_ids:
                cursor.execute("SELECT * FROM punëtori WHERE punid = ?", punid)
                row = cursor.fetchone()
                if row:
                    pun_columns = [col[0] for col in cursor.description]
                    punetore.append(dict(zip(pun_columns, row)))

            project_doc = {
                **project,
                "punetore": punetore
            }
            project_collection.insert_one(convert_for_mongo(project_doc))

        # Migrate departamenti with embedded punëtori
        cursor.execute("SELECT * FROM departamenti")
        departments = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        for dep in departments:
            did = dep["did"]
            cursor.execute("SELECT * FROM punëtori WHERE departamenti_did = ?", did)
            punetore = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
            dep_doc = {
                **dep,
                "punetore": punetore
            }
            department_collection.insert_one(convert_for_mongo(dep_doc))

        print("✅ Migration completed successfully.")
        logging.info("Migration completed successfully.")

    except Exception as e:
        logging.error(f"Migration failed: {e}")
        print(f"❌ Migration failed: {e}")

    finally:
        try:
            cursor.close()
            sql_conn.close()
        except:
            pass

if __name__ == "__main__":
    migrate_data()

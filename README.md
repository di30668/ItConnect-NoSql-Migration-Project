# ITConnect – Data Migration from Relational Database to MongoDB

## 📌 Project Overview
ITConnect is a database migration project that demonstrates the transition of structured data from a relational SQL Server database to a NoSQL MongoDB structure. The project reflects a real-world digital agency (ITera), managing clients, employees, departments, projects, and contracts. The migration includes embedded relationships and optimized document modeling to fit MongoDB’s strengths.

## 🛠️ Technologies & Libraries Used
- **SQL Server (MSSQL)** – for relational database modeling and data population
- **MongoDB** – as the target NoSQL document-oriented database
- **Python 3.12** – used to write the migration script
- **Libraries:**
  - `pyodbc` – to connect to SQL Server
  - `pymongo` – to insert data into MongoDB
  - `datetime` and `decimal` – for data handling
  - `logging` – for tracking migration process


## ⚙️ Setup Instructions

### 1. ✅ SQL Server Setup
- Open `SQL Server Management Studio (SSMS)`
- Create a database named `ITCompany`
- Run the SQL scripts inside `/sql_data/` to:
  - Create tables (`Departamenti`, `Punëtori`, `Klientët`, `Projekti`, `Kontrata`, etc.)
  - Insert 15–20 records per table
  - Ensure foreign key relationships are valid

### 2. ✅ MongoDB Setup
- Install [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- Start the MongoDB server (default port 27017)

### 3. ✅ Python Environment
Install dependencies:

```bash`
pip install pyodbc pymongo

Make sure you have the ODBC Driver 17 for SQL Server installed.

4. 🔄 Running the Migration Script
Edit your connection strings in migration.py if needed, then run:
python migration.py
If successful, you’ll see logs of inserted documents in your terminal, and also inside migration.log.

🧠 Data Modeling Strategy
Relational DB: Normalized with foreign key relationships between klientët, kontrata, projekti, departamenti, and punëtori.

MongoDB Model:

klientët collection embeds kontrata, which in turn embeds its corresponding projekti.

projekti also embeds the employees (punon_në) and department.

Employees and departments are also stored in a separate merged collection.

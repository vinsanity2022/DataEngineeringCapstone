# Import libraries required for connecting to mysql
# python3 -m pip install mysql-connector-python==8.0.31 -- resolved theia lab issue
# Import libraries required for connecting to DB2
# python3 -m pip install ibm-db

# Connect to MySQL
import mysql.connector

# Connect to a Database
connection = mysql.connector.connect(user='root', password='MTQ1NTYtbWFuYWdi',host='127.0.0.1',database='sales')

# Create a cursor
cursor = connection.cursor()


# Connect to DB2
import ibm_db

dsn_hostname = "824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = "fyw69793"        # e.g. "abc12345"
dsn_pwd = "hG0lm4P4BXG7V3sm"      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = "30119"                # e.g. "50000" 
dsn_database = "bludb"            # i.e. "BLUDB"
dsn_driver = "{IBM DB2 ODBC DRIVER}" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              # i.e. "SSL"

#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# create connection
conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)


# Find out the last rowid from DB2 data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database.

def get_last_rowid():
    SQL = "SELECT MAX(rowid) FROM sales_data"
    stmt = ibm_db.exec_immediate(conn, SQL)
    fetch_tup =  ibm_db.fetch_tuple(stmt)
    return fetch_tup[0]

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
	update_list = []

	SQL = "SELECT * FROM sales_data"
	cursor.execute(SQL)

	for row in cursor.fetchall():
		if row[0] > rowid:
		   update_list.append(row)

	return update_list

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database.

def insert_records(records):
	SQL = "INSERT INTO sales_data(rowid, product_id, customer_id, quantity) VALUES(?,?,?,?);"
	stmt = ibm_db.prepare(conn, SQL)
	for row in records:
		ibm_db.execute(stmt, row)


insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))


# disconnect from mysql warehouse
connection.close()

# disconnect from DB2 data warehouse
ibm_db.close(conn)

# End of program

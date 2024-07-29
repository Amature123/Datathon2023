import subprocess
import time
import os
import pandas as pd
from sqlalchemy import create_engine,text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def wait_for_postgres(host, max_retries=5, delay_seconds=3):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                logger.info("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            logger.info(f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    logger.error("Max retries reached. Exiting.")
    return False

# Use the function before running the ELT process
if not wait_for_postgres(host="source_postgres"):
    exit(1)

logger.info("Starting ELT script...")

# Configuration for the source PostgreSQL database
source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': '12345678',
    'host': 'source_postgres'
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': '12345678',
    'host': 'destination_postgres'
}

try:
    # Create SQLAlchemy engines for source and destination
    source_engine = create_engine(f"postgresql://{source_config['user']}:{source_config['password']}@{source_config['host']}/{source_config['dbname']}")
    dest_engine = create_engine(f"postgresql://{destination_config['user']}:{destination_config['password']}@{destination_config['host']}/{destination_config['dbname']}")

    # Directory containing CSV files
    list_directory = './InventoryAndSale_snapshot_data'

    # Iterate through CSV files in the directory
    for dir in os.listdir(list_directory):
        dir_path = os.path.join(list_directory, dir)
        logger.info(f"Processing directory: {dir}")
        for filename in os.listdir(dir_path):
            logger.info(f"Processing filename: {filename}")
            if filename.endswith('.csv'):
                table_name = os.path.splitext(filename)[0].lower()  # Use filename without extension as table name
                file_path = os.path.join(dir_path, filename)
                logger.info(f"Processing file: {table_name}")
                try:
                    # Read CSV file
                    df = pd.read_csv(file_path)
                    
                    # Load data into source database
                    df.to_sql(table_name, source_engine, if_exists='replace', index=False)
                    logger.info(f"Loaded {filename} into source database")
                    
                except Exception as e:
                    logger.error(f"Error processing {filename}: {str(e)}")
            else :
                logger.warning(f"File {filename} is not a CSV file. Skipping...")
    logger.info("CSV processing completed successfully")

    # Use pg_dump to dump the source database to a SQL file
    dump_command = [
        'pg_dump',
        '-h', source_config['host'],
        '-U', source_config['user'],
        '-d', source_config['dbname'],
        '-f', 'data_dump.sql',
        '-w'  # Do not prompt for password
    ]

    # Set the PGPASSWORD environment variable to avoid password prompt
    subprocess_env = dict(PGPASSWORD=source_config['password'])

    # Execute the dump command
    logger.info("Starting database dump...")
    subprocess.run(dump_command, env=subprocess_env, check=True)
    logger.info("Database dump completed successfully")

    # Use psql to load the dumped SQL file into the destination database
    load_command = [
        'psql',
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['dbname'],
        '-a', '-f', 'data_dump.sql'
    ]

    # Set the PGPASSWORD environment variable for the destination database
    subprocess_env = dict(PGPASSWORD=destination_config['password'])

    # Execute the load command
    logger.info("Starting to load data into destination database...")
    subprocess.run(load_command, env=subprocess_env, check=True)
    logger.info("Data loaded into destination database successfully")

except Exception as e:
    logger.error(f"An error occurred during the ELT process: {str(e)}")
    exit(1)

logger.info("ELT script completed successfully")
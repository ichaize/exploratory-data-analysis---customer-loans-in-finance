import yaml
from sqlalchemy import create_engine
import pandas as pd

class RDSDatabaseConnector:

    def __init__(self, credentials): 
        '''The RDSDatabaseConnector establishes connections to the RDS database.
        
           Args:
                credentials (str): the yaml file containing the access credentials
        '''
        self.credentials = self.read_credentials(credentials)

    def read_credentials(self, file):
        ''' Gets the credentials for accessing the database from a yaml file
        
            Args: 
                file (str): the yaml file containing the access credentials
                
            Returns:
                yaml dictionary
        '''
        with open(file) as stream:
            creds = yaml.safe_load(stream)
        return creds
    
    def init_db_engine(self):
        '''Iniiates an engine to connect to the RDS database
        
           Returns:
                sqlalchemy.engine
        '''
        user = self.credentials["RDS_USER"]
        password = self.credentials["RDS_PASSWORD"]
        host = self.credentials["RDS_HOST"]
        port = self.credentials["RDS_PORT"]
        database = self.credentials["RDS_DATABASE"]
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}", echo=True)
        return engine
    
    def read_rds_table(self, table_name):
        ''' Extracts data from an RDS database
        
            Args:
                connector (RDSDatabaseConnector): an instance of the RDSDatabaseConnector class
                table_name (str): the name of the RDS table to be extracted
                
            Returns:
                pandas.Dataframe
        '''  
        engine = self.init_db_engine()
        table = pd.read_sql_table(table_name, engine)
        return table
    
    def save_as_csv(self, table_name):
        table = self.read_rds_table(table_name)
        table.to_csv("loan_payments.csv")

connector = RDSDatabaseConnector("credentials.yaml")
loan_payments = connector.save_as_csv("loan_payments")
print(loan_payments)
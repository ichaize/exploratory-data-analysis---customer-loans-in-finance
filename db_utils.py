import pandas as pd
import yaml
from sqlalchemy import create_engine


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
                table_name (str): the name of the RDS table to be extracted
                
            Returns:
                pandas.Dataframe
        '''  
        engine = self.init_db_engine()
        table = pd.read_sql_table(table_name, engine)
        return table
    
    def save_as_csv(self, table_name):
        ''' Creates a csv.file containing the extracted data
        
            Args:
                table_name (str): the name of the RDS table the data is taken from
        '''
        table = self.read_rds_table(table_name)
        table.to_csv("loan_payments.csv")

    def load_as_df(self, csv_file):
        ''' Loads the data from the locally saved csv file into a dataframe
        
            Args:
                csv_file (str): the name of the file where the data is stored
            
            Returns:
                pandas.Dataframe
        '''
        df = pd.read_csv(csv_file)
        return df

    def upload_to_db(self, df, table):
        '''Uploads the cleaned data to the local SQL database
        
           Args:
                df (pandas.Dataframe): the dataframe to be uploaded
                table (str): the name of the table to create in the SQL database
        '''
        engine = self.init_db_engine()
        df.to_sql(table, engine, if_exists="replace")

connector = RDSDatabaseConnector("credentials.yaml")
loans_df = connector.load_as_df("loan_payments.csv")


from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import bigquery
import json
import os
import traceback
import pymysql


credentials = None
storage_client = None
client = None
shared_dataset_ref = None
sensor_values = None
connection = None
msg = None


def create_db_connection(self):
    global connection

    db_mysql_name = self.config.db_mysql
    print("starting init_helper for db mysql connection")
    print("using db for init_helper:", db_mysql_name)
    try:
        # Get project root dynamically
        project_root = os.path.abspath(os.getcwd())

        # Build config path
        config_path = os.path.join(
            project_root,
            "Components",
            "Configs",
            "mysql_config_credentials.json"
        )

        # Load JSON config
        with open(config_path, "r") as f:
            config = json.load(f)

        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db_mysql_name
        )

        self.config.connection = connection

        print("✅ Local DB connected")

        # return connection


    except Exception as e:
        print("❌ Error initializing Local DB")
        traceback.print_exc()


def init_gcp_backend(self):
    """
    Initialize heavy backend components.
    Should NOT create QApplication.
    """

    global credentials, storage_client
    global client, shared_dataset_ref
    global sensor_values

    project_id = self.config.project_id
    source_dataset_id = self.config.source_dataset_id
    print("starting init_runtime...")
    if self.config.client is not None:
        print("Runtime already initialized. Skipping.")
        return

    # Load sensor JSON
    with open('./utils/sensor_value_update.json', 'r') as f:
        sensor_values = json.load(f)

    # GCP clients
    credentials = service_account.Credentials.from_service_account_file('./utils/Authorization.json')
    storage_client = storage.Client.from_service_account_json('./utils/GCS_Auth.json')

    # BigQuery
    client = bigquery.Client(credentials=credentials, project=project_id)
    shared_dataset_ref = client.get_dataset(source_dataset_id)

    self.config.credentials = credentials
    self.config.client = client
    self.config.shared_dataset_ref = shared_dataset_ref
    print(shared_dataset_ref)

    print("Runtime backend initialized.")
    print("client id: ", id(client))
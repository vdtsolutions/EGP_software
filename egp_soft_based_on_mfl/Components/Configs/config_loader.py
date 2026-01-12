import importlib
import re

from google.cloud import bigquery

_import_cache = {}



def get_inch_config(selected_inch):
    inch = re.findall(r'\d+', str(selected_inch))
    if not inch:
        print("❌ Invalid inch string:", selected_inch)
        return None
    inch = inch[0]
    module_name = f"egp_soft_based_on_mfl.Components.Configs.config_{inch}_inch"
    try:
        config_module = importlib.import_module(module_name)
        print(f"✅ Loaded config: {config_module}")
        return config_module
    except ImportError as e:
        print(f"❌ Could not import {module_name}: {e}")
        return None




from google.cloud import bigquery

# Global shared variables (used by all other modules)
config = None
connection = None
company_list = []
credentials = None
project_id = None
client = None


def set_config(cfg):
    """
    Called ONCE after selecting the pipe inch (e.g., 12 Inch).
    It sets up BigQuery client, MySQL connection, etc.
    """
    global config, connection, company_list, credentials, project_id, client

    if not cfg:
        print("⚠️ set_config() called with None config.")
        return

    try:
        config = cfg
        connection = cfg.connection
        credentials = cfg.credentials
        project_id = cfg.project_id
        client = bigquery.Client(credentials=credentials, project=project_id)
        company_list = getattr(cfg, "company_list", [])

        print(f"✅ Config initialized → {project_id=} | {cfg.pipe_thickness=}")
    except Exception as e:
        print(f"❌ set_config() failed: {e}")


def get_all():
    """
    Safe getter — anywhere else, just do:
        from ...config_loader import get_all
        config, connection, company_list, credentials, project_id, client = get_all()
    """
    return config, connection, company_list, credentials, project_id, client



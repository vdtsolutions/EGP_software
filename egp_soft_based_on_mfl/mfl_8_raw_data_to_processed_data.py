from google.cloud import bigquery
#import Components.config as Config
#print(Config)
from google.oauth2 import service_account
# import Components.logger as logger
# credentials = Config.credentials
# project_id = Config.project_id
project_id ='quantum-theme-334609'
credentials = service_account.Credentials.from_service_account_file('../utils/Authorization.json')
client = bigquery.Client(credentials=credentials, project=project_id)
print(client)


# client = bigquery.Client(credentials=credentials, project=project_id)
processed_data_id = 'quantum-theme-334609.Processed_data.' + 'Main_8_copy_' + str(57)
query = 'create or replace table ' + processed_data_id + ' as SELECT * FROM `quantum-theme-334609.Raw_data.Main_8_copy` where runid={} AND F1H1 IS NOT NULL AND F1H2 IS NOT NULL ' \
                                                             'AND F1H3 IS NOT NULL AND F1H4 IS NOT NULL AND F1P1 IS NOT NULL AND F2H1 IS NOT NULL AND F2H2 IS NOT NULL AND F2H3 IS NOT NULL ' \
                                                             'AND F2H4 IS NOT NULL AND F2P2 IS NOT NULL AND F3H1 IS NOT NULL AND F3H2 IS NOT NULL AND F3H3 IS NOT NULL AND F3H4 IS NOT NULL AND ' \
                                                             'F3P3 IS NOT NULL AND F4H1 IS NOT NULL AND F4H2 IS NOT NULL AND F4H3 IS NOT NULL AND F4H4 IS NOT NULL AND F4P4 IS NOT NULL AND F5H1 ' \
                                                             'IS NOT NULL AND F5H2 IS NOT NULL AND F5H3 IS NOT NULL AND F5H4 IS NOT NULL AND F5P1 IS NOT NULL AND F6H1 IS NOT NULL AND F6H2 IS NOT NULL ' \
                                                             'AND F6H3 IS NOT NULL AND F6H4 IS NOT NULL AND F6P2 IS NOT NULL AND F7H1 IS NOT NULL AND F7H2 IS NOT NULL AND F7H3 IS NOT NULL AND F7H4 IS ' \
                                                             'NOT NULL AND F7P3 IS NOT NULL AND F8H1 IS NOT NULL AND F8H2 IS NOT NULL AND F8H3 IS NOT NULL AND F8H4 IS NOT NULL AND F8P4 IS NOT NULL AND ' \
                                                             'F9H1 IS NOT NULL AND F9H2 IS NOT NULL AND F9H3 IS NOT NULL AND F9H4 IS NOT NULL AND F9P1 IS NOT NULL AND F10H1 IS NOT NULL AND F10H2 IS NOT NULL ' \
                                                             'AND F10H3 IS NOT NULL AND F10H4 IS NOT NULL AND F10P2 IS NOT NULL AND F11H1 IS NOT NULL AND F11H2 IS NOT NULL AND F11H3 IS NOT NULL AND F11H4 IS NOT NULL ' \
                                                             'AND F11P3 IS NOT NULL AND F12H1 IS NOT NULL AND F12H2 IS NOT NULL AND F12H3 IS NOT NULL AND F12H4 IS NOT NULL AND F12P4 IS NOT NULL AND F13H1 IS NOT NULL ' \
                                                             'AND F13H2 IS NOT NULL AND F13H3 IS NOT NULL AND F13H4 IS NOT NULL AND F13P1 IS NOT NULL AND F14H1 IS NOT NULL AND F14H2 IS NOT NULL AND F14H3 IS NOT NULL ' \
                                                             'AND F14H4 IS NOT NULL AND F14P2 IS NOT NULL AND F15H1 IS NOT NULL AND F15H2 IS NOT NULL AND F15H3 IS NOT NULL AND F15H4 IS NOT NULL AND F15P3 IS NOT NULL ' \
                                                             'AND F16H1 IS NOT NULL AND F16H2 IS NOT NULL AND F16H3 IS NOT NULL AND F16H4 IS NOT NULL AND F16P4 IS NOT NULL AND F17H1 IS NOT NULL AND F17H2 IS NOT NULL ' \
                                                             'AND F17H3 IS NOT NULL AND F17H4 IS NOT NULL AND F17P1 IS NOT NULL AND F18H1 IS NOT NULL AND F18H2 IS NOT NULL AND F18H3 IS NOT NULL AND F18H4 IS NOT NULL ' \
                                                             'AND F18P2 IS NOT NULL AND F19H1 IS NOT NULL AND F19H2 IS NOT NULL AND F19H3 IS NOT NULL AND F19H4 IS NOT NULL AND F19P3 IS NOT NULL AND F20H1 IS NOT NULL ' \
                                                             'AND F20H2 IS NOT NULL AND F20H3 IS NOT NULL AND F20H4 IS NOT NULL AND F20P4 IS NOT NULL AND F21H1 IS NOT NULL AND F21H2 IS NOT NULL AND F21H3 IS NOT NULL ' \
                                                             'AND F21H4 IS NOT NULL AND F21P1 IS NOT NULL AND F22H1 IS NOT NULL AND F22H2 IS NOT NULL AND F22H3 IS NOT NULL AND F22H4 IS NOT NULL AND F22P2 IS NOT NULL ' \
                                                             'AND F23H1 IS NOT NULL AND F23H2 IS NOT NULL AND F23H3 IS NOT NULL AND F23H4 IS NOT NULL AND F23P3 IS NOT NULL AND F24H1 IS NOT NULL AND F24H2 IS NOT NULL ' \
                                                             'AND F24H3 IS NOT NULL AND F24H4 IS NOT NULL AND F24P4 IS NOT NULL AND ODDO1 IS NOT NULL AND ODDO2 IS NOT NULL'

runid_specific_table = client.query(query.format(57))
print("runid_specific_table", runid_specific_table)
# view_id = 'quantum-theme-334609.Processed_data.' + 'Main_8_copy_x' + str(21)
# view = bigquery.Table(view_id)
# print("<<<<<<<<<<<<<<<<<<")
# view.view_query = f"SELECT *, ROW_NUMBER() OVER (ORDER BY filename, Serialno) AS index FROM `{processed_data_id}` order by filename, Serialno"
# # view.view_query = 'CREATE OR REPLACE VIEW  ' + view_id + ' AS SELECT * FROM ' + processed_data_id
#
# # Make an API request to create the view.
# view = client.create_table(view)
# print(f"Created {view.table_type}: {str(view.reference)}")
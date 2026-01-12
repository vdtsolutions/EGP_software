# connection = Config.connection
# credentials = Config.credentials
# project_id = Config.project_id
# client = bigquery.Client(credentials=credentials, project=project_id)
# config = json.loads(open('../utils/sensor_value - Copy.json').read())
import os
import json

# import config as config
from google.cloud import bigquery
from egp_soft_based_on_mfl.Components.Configs import config_old as config

connection = config.connection
credentials = config.credentials
project_id = config.project_id
client = bigquery.Client(credentials=credentials, project=project_id)

# Fix the JSON path (relative to this script's location)
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.normpath(os.path.join(current_dir, '..', 'utils', 'sensor_value - Copy.json'))

# Load the JSON config
with open(json_path, 'r') as f:
    config = json.load(f)


class Query_flow():
    def __init__(self, runid, sensitivity):
        self.runid = runid
        self.sensitivity1 = float(sensitivity)
        #self.sensitivity1=float(1.02)
        #self.sensitivity1=self.sensitivity
        #print(self.sensitivity1)
        # self.F1H1 = self.sensitivity * float(config["F1H1"])
        # self.F1H2 = self.sensitivity * float(config["F1H2"])
        # self.F1H3 = self.sensitivity * float(config["F1H3"])
        # self.F1H4 = self.sensitivity * float(config["F1H4"])
        # self.F1P1 = self.sensitivity * float(config["F1P1"])
        # self.F2H1 = self.sensitivity * float(config["F2H1"])
        # self.F2H2 = self.sensitivity * float(config["F2H2"])
        # self.F2H3 = self.sensitivity * float(config["F2H3"])
        # self.F2H4 = self.sensitivity * float(config["F2H4"])
        # self.F2P2 = self.sensitivity * float(config["F2P2"])
        # self.F3H1 = self.sensitivity * float(config["F3H1"])
        # self.F3H2 = self.sensitivity * float(config["F3H2"])
        # self.F3H3 = self.sensitivity * float(config["F3H3"])
        # self.F3H4 = self.sensitivity * float(config["F3H4"])
        # self.F3P3 = self.sensitivity * float(config["F3P3"])
        # self.F4H1 = self.sensitivity * float(config["F4H1"])
        # self.F4H2 = self.sensitivity * float(config["F4H2"])
        # self.F4H3 = self.sensitivity * float(config["F4H3"])
        # self.F4H4 = self.sensitivity * float(config["F4H4"])
        # self.F4P4 = self.sensitivity * float(config["F4P4"])
        # self.F5H1 = self.sensitivity * float(config["F5H1"])
        # self.F5H2 = self.sensitivity * float(config["F5H2"])
        # self.F5H3 = self.sensitivity * float(config["F5H3"])
        # self.F5H4 = self.sensitivity * float(config["F5H4"])
        # self.F5P1 = self.sensitivity * float(config["F5P1"])
        # self.F6H1 = self.sensitivity * float(config["F6H1"])
        # self.F6H2 = self.sensitivity * float(config["F6H2"])
        # self.F6H3 = self.sensitivity * float(config["F6H3"])
        # self.F6H4 = self.sensitivity * float(config["F6H4"])
        # self.F6P2 = self.sensitivity * float(config["F6P2"])
        # self.F7H1 = self.sensitivity * float(config["F7H1"])
        # self.F7H2 = self.sensitivity * float(config["F7H2"])
        # self.F7H3 = self.sensitivity * float(config["F7H3"])
        # self.F7H4 = self.sensitivity * float(config["F7H4"])
        # self.F7P3 = self.sensitivity * float(config["F7P3"])
        # self.F8H1 = self.sensitivity * float(config["F8H1"])
        # self.F8H2 = self.sensitivity * float(config["F8H2"])
        # self.F8H3 = self.sensitivity * float(config["F8H3"])
        # self.F8H4 = self.sensitivity * float(config["F8H4"])
        # self.F8P4 = self.sensitivity * float(config["F8P4"])
        # self.F9H1 = self.sensitivity * float(config["F9H1"])
        # self.F9H2 = self.sensitivity * float(config["F9H2"])
        # self.F9H3 = self.sensitivity * float(config["F9H3"])
        # self.F9H4 = self.sensitivity * float(config["F9H4"])
        # self.F9P1 = self.sensitivity * float(config["F9P1"])
        # self.F10H1 = self.sensitivity * float(config["F10H1"])
        # self.F10H2 = self.sensitivity * float(config["F10H2"])
        # self.F10H3 = self.sensitivity * float(config["F10H3"])
        # self.F10H4 = self.sensitivity * float(config["F10H4"])
        # self.F10P2 = self.sensitivity * float(config["F10P2"])
        # self.F11H1 = self.sensitivity * float(config["F11H1"])
        # self.F11H2 = self.sensitivity * float(config["F11H2"])
        # self.F11H3 = self.sensitivity * float(config["F11H3"])
        # self.F11H4 = self.sensitivity * float(config["F11H4"])
        # self.F11P3 = self.sensitivity * float(config["F11P3"])
        # self.F12H1 = self.sensitivity * float(config["F12H1"])
        # self.F12H2 = self.sensitivity * float(config["F12H2"])
        # self.F12H3 = self.sensitivity * float(config["F12H3"])
        # self.F12H4 = self.sensitivity * float(config["F12H4"])
        # self.F12P4 = self.sensitivity * float(config["F12P4"])
        # self.F13H1 = self.sensitivity * float(config["F13H1"])
        # self.F13H2 = self.sensitivity * float(config["F13H2"])
        # self.F13H3 = self.sensitivity * float(config["F13H3"])
        # self.F13H4 = self.sensitivity * float(config["F13H4"])
        # self.F13P1 = self.sensitivity * float(config["F13P1"])
        # self.F14H1 = self.sensitivity * float(config["F14H1"])
        # self.F14H2 = self.sensitivity * float(config["F14H2"])
        # self.F14H3 = self.sensitivity * float(config["F14H3"])
        # self.F14H4 = self.sensitivity * float(config["F14H4"])
        # self.F14P2 = self.sensitivity * float(config["F14P2"])
        # self.F15H1 = self.sensitivity * float(config["F15H1"])
        # self.F15H2 = self.sensitivity * float(config["F15H2"])
        # self.F15H3 = self.sensitivity * float(config["F15H3"])
        # self.F15H4 = self.sensitivity * float(config["F15H4"])
        # self.F15P3 = self.sensitivity * float(config["F15P3"])
        # self.F16H1 = self.sensitivity * float(config["F16H1"])
        # self.F16H2 = self.sensitivity * float(config["F16H2"])
        # self.F16H3 = self.sensitivity * float(config["F16H3"])
        # self.F16H4 = self.sensitivity * float(config["F16H4"])
        # self.F16P4 = self.sensitivity * float(config["F16P4"])
        # self.F17H1 = self.sensitivity * float(config["F17H1"])
        # self.F17H2 = self.sensitivity * float(config["F17H2"])
        # self.F17H3 = self.sensitivity * float(config["F17H3"])
        # self.F17H4 = self.sensitivity * float(config["F17H4"])
        # self.F17P1 = self.sensitivity * float(config["F17P1"])
        # self.F18H1 = self.sensitivity * float(config["F18H1"])
        # self.F18H2 = self.sensitivity * float(config["F18H2"])
        # self.F18H3 = self.sensitivity * float(config["F18H3"])
        # self.F18H4 = self.sensitivity * float(config["F18H4"])
        # self.F18P2 = self.sensitivity * float(config["F18P2"])
        # self.F19H1 = self.sensitivity * float(config["F19H1"])
        # self.F19H2 = self.sensitivity * float(config["F19H2"])
        # self.F19H3 = self.sensitivity * float(config["F19H3"])
        # self.F19H4 = self.sensitivity * float(config["F19H4"])
        # self.F19P3 = self.sensitivity * float(config["F19P3"])
        # self.F20H1 = self.sensitivity * float(config["F20H1"])
        # self.F20H2 = self.sensitivity * float(config["F20H2"])
        # self.F20H3 = self.sensitivity * float(config["F20H3"])
        # self.F20H4 = self.sensitivity * float(config["F20H4"])
        # self.F20P4 = self.sensitivity * float(config["F20P4"])
        # self.F21H1 = self.sensitivity * float(config["F21H1"])
        # self.F21H2 = self.sensitivity * float(config["F21H2"])
        # self.F21H3 = self.sensitivity * float(config["F21H3"])
        # self.F21H4 = self.sensitivity * float(config["F21H4"])
        # self.F21P1 = self.sensitivity * float(config["F21P1"])
        # self.F22H1 = self.sensitivity * float(config["F22H1"])
        # self.F22H2 = self.sensitivity * float(config["F22H2"])
        # self.F22H3 = self.sensitivity * float(config["F22H3"])
        # self.F22H4 = self.sensitivity * float(config["F22H4"])
        # self.F22P2 = self.sensitivity * float(config["F22P2"])
        # self.F23H1 = self.sensitivity * float(config["F23H1"])
        # self.F23H2 = self.sensitivity * float(config["F23H2"])
        # self.F23H3 = self.sensitivity * float(config["F23H3"])
        # self.F23H4 = self.sensitivity * float(config["F23H4"])
        # self.F23P3 = self.sensitivity * float(config["F23P3"])
        # self.F24H1 = self.sensitivity * float(config["F24H1"])
        # self.F24H2 = self.sensitivity * float(config["F24H2"])
        # self.F24H3 = self.sensitivity * float(config["F24H3"])
        # self.F24H4 = self.sensitivity * float(config["F24H4"])
        # self.F24P4 = self.sensitivity * float(config["F24P4"])

        self.f1h1 = self.sensitivity1 * float(config["F1H1"])
        self.f1h2 = self.sensitivity1 * float(config["F1H2"])
        self.f1h3 = self.sensitivity1 * float(config["F1H3"])
        self.f1h4 = self.sensitivity1 * float(config["F1H4"])
        #self.f1p1 = self.sensitivity1 * float(config["F1P1"])
        self.f2h1 = self.sensitivity1 * float(config["F2H1"])
        self.f2h2 = self.sensitivity1 * float(config["F2H2"])
        self.f2h3 = self.sensitivity1 * float(config["F2H3"])
        self.f2h4 = self.sensitivity1 * float(config["F2H4"])
        #self.f2p2 = self.sensitivity1 * float(config["F2P2"])
        self.f3h1 = self.sensitivity1 * float(config["F3H1"])
        self.f3h2 = self.sensitivity1 * float(config["F3H2"])
        self.f3h3 = self.sensitivity1 * float(config["F3H3"])
        self.f3h4 = self.sensitivity1 * float(config["F3H4"])
        #self.f3p3 = self.sensitivity1 * float(config["F3P3"])
        self.f4h1 = self.sensitivity1 * float(config["F4H1"])
        self.f4h2 = self.sensitivity1 * float(config["F4H2"])
        self.f4h3 = self.sensitivity1 * float(config["F4H3"])
        self.f4h4 = self.sensitivity1 * float(config["F4H4"])
        #self.f4p4 = self.sensitivity1 * float(config["F4P4"])
        self.f5h1 = self.sensitivity1 * float(config["F5H1"])
        self.f5h2 = self.sensitivity1 * float(config["F5H2"])
        self.f5h3 = self.sensitivity1 * float(config["F5H3"])
        self.f5h4 = self.sensitivity1 * float(config["F5H4"])
        #self.f5p1 = self.sensitivity1 * float(config["F5P1"])
        self.f6h1 = self.sensitivity1 * float(config["F6H1"])
        self.f6h2 = self.sensitivity1 * float(config["F6H2"])
        self.f6h3 = self.sensitivity1 * float(config["F6H3"])
        self.f6h4 = self.sensitivity1 * float(config["F6H4"])
        #self.f6p2 = self.sensitivity1 * float(config["F6P2"])
        self.f7h1 = self.sensitivity1 * float(config["F7H1"])
        self.f7h2 = self.sensitivity1 * float(config["F7H2"])
        self.f7h3 = self.sensitivity1 * float(config["F7H3"])
        self.f7h4 = self.sensitivity1 * float(config["F7H4"])
        #self.f7p3 = self.sensitivity1 * float(config["F7P3"])
        self.f8h1 = self.sensitivity1 * float(config["F8H1"])
        self.f8h2 = self.sensitivity1 * float(config["F8H2"])
        self.f8h3 = self.sensitivity1 * float(config["F8H3"])
        self.f8h4 = self.sensitivity1 * float(config["F8H4"])
        #self.f8p4 = self.sensitivity1 * float(config["F8P4"])
        self.f9h1 = self.sensitivity1 * float(config["F9H1"])
        self.f9h2 = self.sensitivity1 * float(config["F9H2"])
        self.f9h3 = self.sensitivity1 * float(config["F9H3"])
        self.f9h4 = self.sensitivity1 * float(config["F9H4"])
        #self.f9p1 = self.sensitivity1 * float(config["F9P1"])
        self.f10h1 = self.sensitivity1 * float(config["F10H1"])
        self.f10h2 = self.sensitivity1 * float(config["F10H2"])
        self.f10h3 = self.sensitivity1 * float(config["F10H3"])
        self.f10h4 = self.sensitivity1 * float(config["F10H4"])
        #self.f10p2 = self.sensitivity1 * float(config["F10P2"])
        self.f11h1 = self.sensitivity1 * float(config["F11H1"])
        self.f11h2 = self.sensitivity1 * float(config["F11H2"])
        self.f11h3 = self.sensitivity1 * float(config["F11H3"])
        self.f11h4 = self.sensitivity1 * float(config["F11H4"])
        #self.f11p3 = self.sensitivity1 * float(config["F11P3"])
        self.f12h1 = self.sensitivity1 * float(config["F12H1"])
        self.f12h2 = self.sensitivity1 * float(config["F12H2"])
        self.f12h3 = self.sensitivity1 * float(config["F12H3"])
        self.f12h4 = self.sensitivity1 * float(config["F12H4"])
        #self.f12p4 = self.sensitivity1 * float(config["F12P4"])
        self.f13h1 = self.sensitivity1 * float(config["F13H1"])
        self.f13h2 = self.sensitivity1 * float(config["F13H2"])
        self.f13h3 = self.sensitivity1 * float(config["F13H3"])
        self.f13h4 = self.sensitivity1 * float(config["F13H4"])
        #self.f13p1 = self.sensitivity1 * float(config["F13P1"])
        self.f14h1 = self.sensitivity1 * float(config["F14H1"])
        self.f14h2 = self.sensitivity1 * float(config["F14H2"])
        self.f14h3 = self.sensitivity1 * float(config["F14H3"])
        self.f14h4 = self.sensitivity1 * float(config["F14H4"])
        #self.f14p2 = self.sensitivity1 * float(config["F14P2"])
        self.f15h1 = self.sensitivity1 * float(config["F15H1"])
        self.f15h2 = self.sensitivity1 * float(config["F15H2"])
        self.f15h3 = self.sensitivity1 * float(config["F15H3"])
        self.f15h4 = self.sensitivity1 * float(config["F15H4"])
        #self.f15p3 = self.sensitivity1 * float(config["F15P3"])
        self.f16h1 = self.sensitivity1 * float(config["F16H1"])
        self.f16h2 = self.sensitivity1 * float(config["F16H2"])
        self.f16h3 = self.sensitivity1 * float(config["F16H3"])
        self.f16h4 = self.sensitivity1 * float(config["F16H4"])
        #self.f16p4 = self.sensitivity1 * float(config["F16P4"])
        self.f17h1 = self.sensitivity1 * float(config["F17H1"])
        self.f17h2 = self.sensitivity1 * float(config["F17H2"])
        self.f17h3 = self.sensitivity1 * float(config["F17H3"])
        self.f17h4 = self.sensitivity1 * float(config["F17H4"])
        #self.f17p1 = self.sensitivity1 * float(config["F17P1"])
        self.f18h1 = self.sensitivity1 * float(config["F18H1"])
        self.f18h2 = self.sensitivity1 * float(config["F18H2"])
        self.f18h3 = self.sensitivity1 * float(config["F18H3"])
        self.f18h4 = self.sensitivity1 * float(config["F18H4"])
        #self.f18p2 = self.sensitivity1 * float(config["F18P2"])
        self.f19h1 = self.sensitivity1 * float(config["F19H1"])
        self.f19h2 = self.sensitivity1 * float(config["F19H2"])
        self.f19h3 = self.sensitivity1 * float(config["F19H3"])
        self.f19h4 = self.sensitivity1 * float(config["F19H4"])
        #self.f19p3 = self.sensitivity1 * float(config["F19P3"])
        self.f20h1 = self.sensitivity1 * float(config["F20H1"])
        self.f20h2 = self.sensitivity1 * float(config["F20H2"])
        self.f20h3 = self.sensitivity1 * float(config["F20H3"])
        self.f20h4 = self.sensitivity1 * float(config["F20H4"])
        #self.f20p4 = self.sensitivity1 * float(config["F20P4"])
        self.f21h1 = self.sensitivity1 * float(config["F21H1"])
        self.f21h2 = self.sensitivity1 * float(config["F21H2"])
        self.f21h3 = self.sensitivity1 * float(config["F21H3"])
        self.f21h4 = self.sensitivity1 * float(config["F21H4"])
        #self.f21p1 = self.sensitivity1 * float(config["F21P1"])
        self.f22h1 = self.sensitivity1 * float(config["F22H1"])
        self.f22h2 = self.sensitivity1 * float(config["F22H2"])
        self.f22h3 = self.sensitivity1 * float(config["F22H3"])
        self.f22h4 = self.sensitivity1 * float(config["F22H4"])
        #self.f22p2 = self.sensitivity1 * float(config["F22P2"])
        self.f23h1 = self.sensitivity1 * float(config["F23H1"])
        self.f23h2 = self.sensitivity1 * float(config["F23H2"])
        self.f23h3 = self.sensitivity1 * float(config["F23H3"])
        self.f23h4 = self.sensitivity1 * float(config["F23H4"])
        #self.f23p3 = self.sensitivity1 * float(config["F23P3"])
        self.f24h1 = self.sensitivity1 * float(config["F24H1"])
        self.f24h2 = self.sensitivity1 * float(config["F24H2"])
        self.f24h3 = self.sensitivity1 * float(config["F24H3"])
        self.f24h4 = self.sensitivity1 * float(config["F24H4"])
        #self.f24p4 = self.sensitivity1 * float(config["F24P4"])
        self.f25h1 = self.sensitivity1 * float(config["F25H1"])
        self.f25h2 = self.sensitivity1 * float(config["F25H2"])
        self.f25h3 = self.sensitivity1 * float(config["F25H3"])
        self.f25h4 = self.sensitivity1 * float(config["F25H4"])
        # self.f25p1 = self.sensitivity1 * float(config["F25P1"])
        self.f26h1 = self.sensitivity1 * float(config["F26H1"])
        self.f26h2 = self.sensitivity1 * float(config["F26H2"])
        self.f26h3 = self.sensitivity1 * float(config["F26H3"])
        self.f26h4 = self.sensitivity1 * float(config["F26H4"])
        # self.f26p2 = self.sensitivity1 * float(config["F26P2"])
        self.f27h1 = self.sensitivity1 * float(config["F27H1"])
        self.f27h2 = self.sensitivity1 * float(config["F27H2"])
        self.f27h3 = self.sensitivity1 * float(config["F27H3"])
        self.f27h4 = self.sensitivity1 * float(config["F27H4"])
        # self.f27p2 = self.sensitivity1 * float(config["F27P3"])
        self.f28h1 = self.sensitivity1 * float(config["F28H1"])
        self.f28h2 = self.sensitivity1 * float(config["F28H2"])
        self.f28h3 = self.sensitivity1 * float(config["F28H3"])
        self.f28h4 = self.sensitivity1 * float(config["F28H4"])
        # self.f28p4 = self.sensitivity1 * float(config["F28P4"])
        self.f29h1 = self.sensitivity1 * float(config["F29H1"])
        self.f29h2 = self.sensitivity1 * float(config["F29H2"])
        self.f29h3 = self.sensitivity1 * float(config["F29H3"])
        self.f29h4 = self.sensitivity1 * float(config["F29H4"])
        # self.f29p1 = self.sensitivity1 * float(config["F29P1"])
        self.f30h1 = self.sensitivity1 * float(config["F30H1"])
        self.f30h2 = self.sensitivity1 * float(config["F30H2"])
        self.f30h3 = self.sensitivity1 * float(config["F30H3"])
        self.f30h4 = self.sensitivity1 * float(config["F30H4"])
        # self.f30p2 = self.sensitivity1 * float(config["F30P2"])
        self.f31h1 = self.sensitivity1 * float(config["F31H1"])
        self.f31h2 = self.sensitivity1 * float(config["F31H2"])
        self.f31h3 = self.sensitivity1 * float(config["F31H3"])
        self.f31h4 = self.sensitivity1 * float(config["F31H4"])
        # self.f31p3 = self.sensitivity1 * float(config["F31P3"])
        self.f32h1 = self.sensitivity1 * float(config["F32H1"])
        self.f32h2 = self.sensitivity1 * float(config["F32H2"])
        self.f32h3 = self.sensitivity1 * float(config["F32H3"])
        self.f32h4 = self.sensitivity1 * float(config["F32H4"])
        # self.f32p4 = self.sensitivity1 * float(config["F32P4"])
        self.f33h1 = self.sensitivity1 * float(config["F33H1"])
        self.f33h2 = self.sensitivity1 * float(config["F33H2"])
        self.f33h3 = self.sensitivity1 * float(config["F33H3"])
        self.f33h4 = self.sensitivity1 * float(config["F33H4"])
        # self.f33p1 = self.sensitivity1 * float(config["F33P1"])
        self.f34h1 = self.sensitivity1 * float(config["F34H1"])
        self.f34h2 = self.sensitivity1 * float(config["F34H2"])
        self.f34h3 = self.sensitivity1 * float(config["F34H3"])
        self.f34h4 = self.sensitivity1 * float(config["F34H4"])
        # self.f34p2 = self.sensitivity1 * float(config["F34P2"])
        self.f35h1 = self.sensitivity1 * float(config["F35H1"])
        self.f35h2 = self.sensitivity1 * float(config["F35H2"])
        self.f35h3 = self.sensitivity1 * float(config["F35H3"])
        self.f35h4 = self.sensitivity1 * float(config["F35H4"])
        # self.f35p3 = self.sensitivity1 * float(config["F35P3"])
        self.f36h1 = self.sensitivity1 * float(config["F36H1"])
        self.f36h2 = self.sensitivity1 * float(config["F36H2"])
        self.f36h3 = self.sensitivity1 * float(config["F36H3"])
        self.f36h4 = self.sensitivity1 * float(config["F36H4"])
        # self.f36p4 = self.sensitivity1 * float(config["F36P4"])
        self.query_flow()

    def query_flow(self):
        sensitivity = self.sensitivity1
        runid = self.runid
        print("start of fetching weld record from bigquery")

        query = 'SELECT ODDO1, ODDO2, index FROM ' + config.table_name + ' WHERE (select countif(condition) from unnest([F1H1>{} , F1H2>{} , F1H3>{} , F1H4>{}  , F2H1>{} , F2H2>{} , F2H3>{} , F2H4>{} , F3H1>{} , F3H2>{} , F3H3>{} , F3H4>{}  , F4H1>{} , F4H2>{} , F4H3>{} , ' \
                                                                       'F4H4>{}  , F5H1>{} , F5H2>{} , F5H3>{} , F5H4>{}  , F6H1>{} , F6H2>{} , ' \
                                                                       'F6H3>{} , F6H4>{}  , F7H1>{} , F7H2>{} , F7H3>{} , F7H4>{}  , ' \
                                                                       'F8H1>{} , F8H2>{} , F8H3>{} , F8H4>{}  , F9H1>{} , F9H2>{} , F9H3>{} , F9H4>{} , F10H1>{} , F10H2>{} , F10H3>{} , F10H4>{}  , F11H1>{} , F11H2>{} , ' \
                                                                       'F11H3>{} , F11H4>{}  , F12H1>{} , F12H2>{} , F12H3>{} , F12H4>{}  , ' \
                                                                       'F13H1>{} , F13H2>{} , F13H3>{} , F13H4>{}  , F14H1>{} , F14H2>{} , F14H3>{} , ' \
                                                                       'F14H4>{}  , F15H1>{} , F15H2>{} , F15H3>{} , F15H4>{}  , F16H1>{} , ' \
                                                                       'F16H2>{} , F16H3>{} , F16H4>{}  , F17H1>{} , F17H2>{} , F17H3>{} , F17H4>{} , F18H1>{} , F18H2>{} , F18H3>{} , F18H4>{}  , F19H1>{} , F19H2>{} , ' \
                                                                       'F19H3>{} , F19H4>{}  , F20H1>{} , F20H2>{} , F20H3>{} , F20H4>{}  , ' \
                                                                       'F21H1>{} , F21H2>{} , F21H3>{} , F21H4>{}  , F22H1>{} , F22H2>{} , F22H3>{} , ' \
                                                                       'F22H4>{}  , F23H1>{} , F23H2>{} , F23H3>{} , F23H4>{}  , ' \
                                                                       'F24H1>{} , F24H2>{} , F24H3>{} , F24H4>{} , F25H1>{} , F25H2>{}, F25H3>{}, F25H4>{}, F26H1>{}, F26H2>{}, F26H3>{}, F26H4>{}, ' \
                                                                       'F27H1>{}, F27H2>{}, F27H3>{}, F27H4>{}, F28H1>{}, F28H2>{}, F28H3>{}, F28H4>{}, F29H1>{}, F29H2>{}, F29H3>{}, F29H4>{},' \
                                                                       'F30H1>{}, F30H2>{}, F30H3>{}, F30H4>{}, F31H1>{}, F31H2>{}, F31H3>{}, F31H4>{}, , F32H1>{}, F32H2>{}, F32H3>{}, F32H4>{}, F33H1>{}, F33H2>{}, F33H3>{}, F33H4>{},' \
                                                                       'F34H1>{}, F34H2>{}, F34H3>{}, F34H4>{}, F35H1>{}, F35H2>{}, F35H3>{}, F35H4>{}, , F36H1>{}, F36H2>{}, F36H3>{}, F36H4>{} runid={}]) condition) >= 64 ORDER BY index'


        query_job = client.query(
            query.format(self.f1h1, self.f1h2, self.f1h3, self.f1h4, self.f2h1, self.f2h2,
                         self.f2h3, self.f2h4, self.f3h1, self.f3h2, self.f3h3, self.f3h4,
                         self.f4h1, self.f4h2, self.f4h3, self.f4h4, self.f5h1,
                         self.f5h2, self.f5h3, self.f5h4, self.f6h1, self.f6h2, self.f6h3,
                         self.f6h4, self.f7h1, self.f7h2, self.f7h3, self.f7h4,
                         self.f8h1, self.f8h2, self.f8h3, self.f8h4, self.f9h1, self.f9h2,
                         self.f9h3, self.f9h4, self.f10h1, self.f10h2, self.f10h3, self.f10h4,
                         self.f11h1, self.f11h2, self.f11h3, self.f11h4,
                         self.f12h1, self.f12h2, self.f12h3, self.f12h4, self.f13h1,
                         self.f13h2, self.f13h3, self.f13h4, self.f14h1, self.f14h2,
                         self.f14h3, self.f14h4, self.f15h1, self.f15h2, self.f15h3,
                         self.f15h4, self.f16h1, self.f16h2, self.f16h3, self.f16h4,
                         self.f17h1, self.f17h2, self.f17h3, self.f17h4,
                         self.f18h1, self.f18h2, self.f18h3, self.f18h4, self.f19h1,
                         self.f19h2, self.f19h3, self.f19h4, self.f20h1, self.f20h2,
                         self.f20h3, self.f20h4, self.f21h1, self.f21h2, self.f21h3,
                         self.f21h4, self.f22h1, self.f22h2, self.f22h3, self.f22h4,
                         self.f23h1, self.f23h2, self.f23h3, self.f23h4,
                         self.f24h1, self.f24h2, self.f24h3, self.f24h4, self.f25h1,
                         self.f25h2, self.f25h3, self.f25h4, self.f26h1, self.f26h2,
                         self.f26h3, self.f26h4, self.f27h1, self.f27h2, self.f27h3,
                         self.f27h4, self.f28h1, self.f28h2, self.f28h3, self.f28h4,
                         self.f29h1, self.f29h2, self.f29h3, self.f29h4, self.f30h1,
                         self.f30h2, self.f30h3, self.f30h4, self.f31h1, self.f31h2,
                         self.f31h3, self.f31h4, self.f32h1, self.f32h2, self.f32h3,
                         self.f32h4, self.f33h1, self.f33h2, self.f33h3, self.f33h4,
                         self.f34h1, self.f34h2, self.f34h3, self.f34h4, self.f35h1,
                         self.f35h2, self.f35h3, self.f35h4, self.f36h1, self.f36h2,
                         self.f36h3, self.f36h4, runid))
        results = query_job.result()  # Waits for job to complete.
        print("End of fetching weld record from bigquery")

        if results.total_rows == 0:
            config.no_weld_indicator = True
            config.warning_msg("NO weld record Found", "")
            return
        else:
            config.no_weld_indicator = False
            config.print_with_time("weld record found")
            indexes = []
            oddo1 = []
            oddo2 = []
            config.print_with_time("creating list of indexes")
            #print(results)
            for row in results:
                indexes.append(row[2])
                oddo2.append(row[1])
                oddo1.append(row[0])
            # print("indexes",indexes)
            # print("oddo1",oddo1)
            # print("oddo2",oddo2)
            config.print_with_time("list of indexes created")
            p_data = ranges(indexes)
            f_data = []
            analytic_id = get_analytic_id(runid, sensitivity)
            config.print_with_time("Analytic Id is " + str(analytic_id))
            config.print_with_time("Generating Welds")
            for i, row in enumerate(p_data):
                index1 = indexes.index(row[0])
                index2 = indexes.index(row[1])
                start_oddo1 = oddo1[index1]
                end_oddo1 = oddo1[index2]
                start_oddo2 = oddo2[index1]
                end_oddo2 = oddo2[index2]
                weld_length = end_oddo1 - start_oddo1 if end_oddo1 >= end_oddo2 else end_oddo2 - start_oddo2
                temp = {"start_index": row[0], "end_index": row[1], "start_oddo1": start_oddo1, "end_oddo1": end_oddo1,
                        "start_oddo2": start_oddo2, "end_oddo2": end_oddo2, "weld_number": i + 1,
                        "analytic_id": analytic_id,
                        "length": weld_length, "sensitivity": sensitivity, "runid": runid}
                f_data.append(temp)
                insert_weld_to_db(temp)
            config.print_with_time("Weld Generation completed")
            ################################# Pipe Generation ######################
            # last_index = 0
            # last_oddo = 0
            # pipes = []
            # Config.print_with_time("Generating Pipe")
            # last_weld = f_data[-1]
            # for row in f_data:
            #     oddo = row["start_oddo1"] if row["start_oddo1"] > row["start_oddo2"] else row["start_oddo2"]
            #     length = oddo - last_oddo
            #     obj = {"start_index": last_index, "end_index": row["start_index"], "length": length,
            #            "analytic_id": analytic_id, "runid": runid}
            #     pipes.append(obj)
            #     last_index = row["end_index"]
            #     last_oddo = row["end_oddo1"] if row["end_oddo1"] > row["end_oddo2"] else row["end_oddo2"]
            #     insert_pipe_to_db(obj)
            # last_pipe = get_last_pipe(runid, last_weld, analytic_id)
            # insert_pipe_to_db(last_pipe)
            # Config.print_with_time("Pipe Generation completed")
            # Config.print_with_time("process end at : ")


# =======================================================================================================
# -----------------------------------Starting of helping module for Weld and Pipe Generation--------------
# ========================================================================================================
def ranges(arr):
    """"
    This will merge the continues indexes and return a list that will contain list of start_index and end_index
        :param arr : List of indexes to merge
    """
    try:
        nums = sorted(set(arr))
        gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s + 45 < e] #### old change s+1<e
        edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
        return list(zip(edges, edges))
    except:
        print("Error while Grouping Weld Range")


# ===========================================================================================================

def insert_weld_to_db(weld_obj):
    print("weld_obj", weld_obj)
    # with connection.cursor() as cursor:
    #     same_lw_up_check = cursor.execute(
    #         'SELECT sensitivity FROM temp_welds where sensitivity="' + weld_obj["sensitivity"] + '"')
    #     if same_lw_up_check:
    #         return 'HII'
    """
        This will insert weld object to mysql database
        :param weld_obj : Object with value of  runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length and weld_number
    """
    try:

        query_weld_insert = "INSERT INTO temp_welds (runid,analytic_id,sensitivity,start_index,end_index,start_oddo1,end_oddo1,start_oddo2,end_oddo2,length,weld_number) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(runid, analytic_id, Sensitivity, start_file, end_file, start_sno, end_sno)
        with connection.cursor() as cursor:
            cursor.execute(query_weld_insert, (
            weld_obj["runid"], weld_obj["analytic_id"], weld_obj["sensitivity"], weld_obj["start_index"],
            weld_obj["end_index"], weld_obj["start_oddo1"], weld_obj["end_oddo1"], weld_obj["start_oddo2"],
            weld_obj["end_oddo2"], weld_obj["length"], weld_obj["weld_number"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


# ===============================================================================================================
def insert_pipe_to_db(pipe_obj):
    """
        This will insert pipe_obj to mysql database
        :param pipe_obj : object will value of runid,analytic_id,length,start_index and end_index
    """
    try:
        query = "INSERT INTO Pipes (runid,analytic_id,length,start_index,end_index) VALUE(%s,%s," \
                "%s,%s,%s) "
        with connection.cursor() as cursor:
            cursor.execute(query,
                           (pipe_obj["runid"], pipe_obj["analytic_id"], pipe_obj["length"], pipe_obj["start_index"],
                            pipe_obj["end_index"]))
            connection.commit()
        return
    except:
        print("Error While Inserting weld for runid ")


# ===============================================================================================================

def get_analytic_id(runid, sensitivity):
    """
        This will return a New Analytic Id
        : param runid: Id of the Project
        : param sensitivity : Sensitivity of the Weld
    """
    with connection.cursor() as cursor:
        query_to_check_analyticsid = "SELECT runid,analytic_id,Sensitivity FROM welds ORDER BY id DESC LIMIT 1"
        cursor.execute(query_to_check_analyticsid)
        result_analytics_query = cursor.fetchone()
        if not result_analytics_query:
            return 1
        elif runid == result_analytics_query[0] and sensitivity != result_analytics_query[2]:
            return result_analytics_query[1] + 1
        elif runid != result_analytics_query[0]:
            return 1
        else:
            return result_analytics_query[1] + 1


# ============================================================================================================
def get_last_pipe(runid, weld_obj, analytic_id):
    """
        This will return the last pipe object to insert into mysql db
        :param runid: Id of the Project
    """
    query = "SELECT index,oddo1,oddo2 FROM `" + config.table_name + "` order by index desc LIMIT 1 "
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        length = row['oddo1'] - weld_obj['end_oddo1']
        end_index = row['index']
        start_index = weld_obj['end_index']
        end_index = row['index']
        obj = {"start_index": start_index, "end_index": end_index, "length": length, "analytic_id": analytic_id,
               "runid": runid}
        return obj

# =======================================================================================================
# -----------------------------------Ending of helping module for Weld and Pipe Generation----------------
# ========================================================================================================
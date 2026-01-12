import pandas as pd

pkl_path = r"D:\Anubhav\EGP_software\EGP_software\Egp_Desktop_12inch\ClockDataFrames\253.pkl"
csv_path = r"D:\Anubhav\EGP_software\EGP_software\Egp_Desktop_12inch\253.csv"

df = pd.read_pickle(pkl_path)
df.to_csv(csv_path, index=False)

print("Saved:", csv_path)


# pipe_df = pd.read_csv(csv_path)
# pipe_df['index'] = pipe_df['index'].astype(int)
#
# hall_cols = [
# 'F1H1','F1H2','F1H3','F1H4',
# 'F2H1','F2H2','F2H3','F2H4',
# 'F3H1','F3H2','F3H3','F3H4',
# 'F4H1','F4H2','F4H3','F4H4',
# 'F5H1','F5H2','F5H3','F5H4',
# 'F6H1','F6H2','F6H3','F6H4',
# 'F7H1','F7H2','F7H3','F7H4',
# 'F8H1','F8H2','F8H3','F8H4',
# 'F9H1','F9H2','F9H3','F9H4',
# 'F10H1','F10H2','F10H3','F10H4',
# 'F11H1','F11H2','F11H3','F11H4',
# 'F12H1','F12H2','F12H3','F12H4'
# ]
#
# df = pipe_df.loc[
#     (pipe_df['index'] > start_index) &
#     (pipe_df['index'] < end_index),
#     ['index','ROLL','ODDO1','ODDO2',*hall_cols,'PITCH','YAW']
# ].copy()
#
# df_main = df
# df_main = df_main.sort_values("index").reset_index(drop=True)
# hall_cols = [
#     f'F{i}H{j}'
#     for i in range(1, self.config.F_columns + 1)
#     for j in range(1, 5)
# ]
#
# df_hall = pd.DataFrame(df_main["HALL_DATA"].tolist(), columns=hall_cols)
#
# df_main = pd.concat([df_main.drop(columns=["HALL_DATA"]), df_hall], axis=1)
#
# df_main["ODDO1"] -= self.config.oddo1
# df_main["ODDO2"] -= self.config.oddo2
# df_main["ROLL"] -= self.config.roll_value
# df_main["PITCH"] -= self.config.pitch_value
# df_main["YAW"] -= self.config.yaw_value



import pandas as pd
from pathlib import Path

asegs = Path("agenda_segments")
legs = Path("legislations")


for leg_file in legs.rglob("*.csv"):
    aseg_file = asegs / leg_file.name
    

    aseg_df = pd.read_csv(aseg_file)
    leg_df = pd.read_csv(leg_file)

    aseg_df["matched_legislation"] = "NO_LEGISLATION"

    for leg_idx, leg_row in leg_df.iterrows():
        for aseg_idx, aseg_row in aseg_df.iterrows():
            if leg_row["item"] in aseg_row["agenda_segment"]:
                aseg_df.at[aseg_idx,"matched_legislation"] = leg_row["text"]
        

    aseg_df.to_csv(aseg_file,index=False)
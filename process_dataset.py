import pandas as pd
from pathlib import Path
import os
# this script is not meant to run the actual desktop pet
# won't be dangerous if you run it but yeah, just a script for one-time use

df = pd.read_csv(os.path.join(Path(__file__).resolve().parent, "intent_clf_dataset/", "shantae_intents.csv"))
groups = df.groupby(by = 'split')
for group_name, group_df in groups:
    group_df[['text', 'intent']].to_csv(f"./intent_clf_dataset/{group_name}.csv")
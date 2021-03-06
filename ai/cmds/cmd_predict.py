"""
  cmds/cmd_predict.py

  FIT3162 - Team 10 - Final Year Computer Science Project
  Copyright Luke Silva, Aichi Tsuchihira, Harsil Patel 2019

  Script to predict the reliability of a dataset using the selected model

"""

import pandas as pd
from joblib import load

from lib.transform import add_vic_coordinates
from lib.filter_columns import filter_columns
from lib.add_env_data import add_columns


def predict(args):
    """
    :param args: the arguments parsed from the command line interface
    :return: reliability predictions of the dataset
    """
    dataset = pd.read_csv(args.infile)

    data = filter_columns(dataset)
    data = add_vic_coordinates(data)

    data = add_columns(data)

    model = load(args.modelfile)
    predictions = model.predict(
        data.drop(columns=["is_reliable", "vic_x", "vic_y", "latitude", "longitude"])
    )

    if args.outfile:
        pd.concat(
            [
                dataset,
                data.drop(
                    columns=["is_reliable", "vic_x", "vic_y", "latitude", "longitude"]
                ),
                pd.DataFrame(predictions, columns=["predictions"]),
            ],
            axis=1,
        ).to_csv(args.outfile)

    return predictions

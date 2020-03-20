#!/usr/bin/env python3

import json
import os
from os.path import dirname

import click
import geopandas as gpd
import pandas as pd
from pandas.api.types import is_numeric_dtype


@click.command()
@click.option('--dataset')
@click.option('--json_output')
@click.option('--n_bins', default=10)
def main(dataset, json_output, n_bins=10):
    g = gpd.read_file(dataset)

    breaks = {}
    for c in g.columns:
        s = g[c]
        if is_numeric_dtype(s):
            _, bins = pd.qcut(s, 10, duplicates='drop', retbins=True)
            breaks[c] = list(bins)

    d = dirname(json_output)
    if d != '' and not os.path.isdir():
        os.makedirs(dirname(json_output))

    with open(json_output, 'w') as f:
        json.dump(breaks, f)


if __name__ == "__main__":
    main()

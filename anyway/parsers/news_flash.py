import pandas as pd
from anyway import db
from anyway.core.utils import Utils
from anyway.common.models.news_flash_models import NewsFlash


def _remove_nan_from_dict(row_dict):
    for key, value in row_dict.items():
        if pd.isnull(value):
            row_dict[key] = -1


def _iter_rows(filename):
    df = pd.read_csv(filename, encoding='utf-8')

    for df_tuple in df.itertuples():
        ordered_row_dict = df_tuple._asdict()
        row_dict = dict(ordered_row_dict)
        row_dict.pop('Index', None)
        _remove_nan_from_dict(row_dict)
        yield row_dict


def parse(filename):

    for batch in Utils.batch_iterator(_iter_rows(filename), batch_size=50):
        db.session.bulk_insert_mappings(NewsFlash, batch)
        db.session.commit()

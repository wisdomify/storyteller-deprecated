import pandas as pd

from storyteller.secrets import controller


def get_definitions(definition_origins: list) -> pd.DataFrame:
    """
    :param definition_origins: this is where definition has been collected. (eg: wikiquote, namuwiki, opendict)
    :return: pandas dataframe of select origin
    """
    def_condition = ' or '.join(map(lambda org: f"origin='{org}'", definition_origins))
    total_condition = f"where {def_condition}" if def_condition else ''
    return controller.get_df_from_sql(target_query=f"""
                select * from story.definition {total_condition}'
            """)


def get_examples(definition_origins: list, example_origins: list) -> pd.DataFrame:
    """
    :param definition_origins: this is where definition has been collected. (eg: wikiquote, namuwiki, opendict)
    :param example_origins: this is where example has been collected. (eg: naverDict, daumDict, KoreaUnivCorpus)
    :return:
    """
    def_condition = ' or '.join(map(lambda org: f"origin='{org}'", definition_origins))
    eg_condition = ' or '.join(map(lambda org: f"wisdom_from='{org}'", example_origins))
    total_condition = []

    if def_condition:
        total_condition.append(def_condition)

    if eg_condition:
        total_condition.append(eg_condition)

    total_condition = f"where {' and '.join(total_condition)}" if total_condition else ""

    return controller.get_df_from_sql(target_query=f"""
            select * from story.example {total_condition}
        """)


def save_data(of: str, to: str, definition_from: list, example_from: list = None):
    """
    :param of: definition or example
    :param to: save path (with file name)
    :param definition_from: definition origins
    :param example_from:
    :return:
    """
    sep = '\t' if to.split('.')[-1].lower() == '.tsv' else ','
    if of == 'definition':
        get_definitions(definition_from).to_csv(to, sep=sep, index=False)

    elif of == 'example':
        get_examples(definition_from, example_from).to_csv(to, sep=sep, index=False)

    else:
        raise NotImplementedError(f"Wrong data type: {of}")

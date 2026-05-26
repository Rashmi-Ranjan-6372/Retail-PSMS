import pandas as pd


def generate_excel(data, file_name="report.xlsx"):

    dataframe = pd.DataFrame(data)

    dataframe.to_excel(
        file_name,
        index=False
    )

    return file_name
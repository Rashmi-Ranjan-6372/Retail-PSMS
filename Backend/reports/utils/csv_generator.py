import csv


def generate_csv(data, headers, file_name="report.csv"):

    with open(file_name, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        for row in data:
            writer.writerow(row)

    return file_name
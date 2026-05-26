def generate_chart_data(labels, values):

    return {
        "labels": labels,
        "datasets": [
            {
                "data": values
            }
        ]
    }
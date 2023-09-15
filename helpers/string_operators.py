def sort_csv(csv):
    li = csv.split(",")
    li.sort()
    csv = ','.join(li)
    return csv
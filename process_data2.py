import csv

mammoth_data = []

with open('pbdb_data.csv', 'r') as csvfile:

    reader = csv.reader(csvfile)

    columns = reader.__next__()

    for row in reader:

        name = row[9]
        abd = row[22]
        abd_unit = row[23]
        lat = float(row[25])
        lng = float(row[24])
        state = row[27]
        country = row[28]
        comment = row[32]

        mammoth_data.append([name, abd, abd_unit, lat, lng, state, country, comment])

with open('mammoth_data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['name', 'abd', 'abd_unit', 'lat', 'lng', 'state', 'country', 'comment'])
    writer.writerows(mammoth_data)

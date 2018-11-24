import csv

if __name__ == "__main__":
    values = []
    with open('thermal.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values.append((row['timestamp'], row['thermal']))

    old_values_float = []
    for time_data, value in values:
        st = value.split('[')
        new_st = []
        for s in st:
            s = s.replace(']', '').replace(' ', '')
            if s:
                new_st.append(s)
        list_of_lists = []
        for new_s in new_st:
            kk = new_s.split(',')
            list_of_lists.append([float(k) for k in kk if k])
        old_values_float.append((time_data, list_of_lists))

    new_values_float = []
    counter = 0
    for i, _ in enumerate(old_values_float):
        if not i % 3:
            if i:
                sum = 0
                for j, row in enumerate(old_values_float[i][1]):
                    for k, ss in enumerate(row):
                        sum += ss - old_values_float[i - 1][1][j][k]
                new_values_float.append((counter, old_values_float[i][0], sum))
            else:
                new_values_float.append((counter, old_values_float[i][0], 0))
            counter += 1

    with open('thermal_delta_15_min.csv', 'w') as csvfile:
        field_names = ['', 'timestamp', 'thermal']
        csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        csv_writer.writeheader()

        for index, timestamp, d in new_values_float:
            csv_writer.writerow({'': index, 'timestamp': timestamp, 'thermal': d})

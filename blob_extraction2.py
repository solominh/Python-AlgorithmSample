

def load_data(filepath):
    data = []
    with open(filepath) as f:
        for line in f:
            row = [int(x) for x in line.strip()]
            data.append(row)
    return data


def save_data(filepath, labels):
    with open(filepath, 'w') as f:
        for row in range(row_count):
            for col in range(col_count):
                if labels[row][col]:
                    f.write(str(labels[row][col]))
                else:
                    f.write('0')
            f.write('\n')


def find_neighboring_labels(row, col, labels):
    west = (row, col - 1)
    northwest = (row - 1, col - 1)
    north = (row - 1, col)
    northeast = (row - 1, col + 1)

    neighbors = [west, northwest, north, northeast]
    neighboring_labels = []
    for neighbor in neighbors:
        if neighbor[0] >= 0 and neighbor[0] < row_count and neighbor[1] >= 0 and neighbor[1] < col_count:
            if labels[neighbor[0]][neighbor[1]]:
                neighboring_labels.append(labels[neighbor[0]][neighbor[1]])

    return neighboring_labels


def find_min_neighboring_label(neighboring_labels):
    min_label = 1000000
    for label in neighboring_labels:
        if label < min_label:
            min_label = label
    return min_label


def two_pass(data):
    global row_count, col_count

    row_count = len(data)
    col_count = len(data[0])
    labels = data.copy()
    label_count = 0

    linked = {}

    # First pass
    for row in range(row_count):
        for col in range(col_count):
            if not labels[row][col]:
                continue

            neighboring_labels = find_neighboring_labels(row, col, labels)
            if not neighboring_labels:
                label_count += 1
                labels[row][col] = label_count
                linked[label_count] = label_count
                continue

            # Find the smallest label
            labels[row][col] = find_min_neighboring_label(neighboring_labels)
            all_root_labels = [linked[label]for label in neighboring_labels]
            min_label = find_min_neighboring_label(all_root_labels)
            for label in neighboring_labels:
                linked[label] = min_label

    # Second pass
    for row in range(row_count):
        for col in range(col_count):
            if not data[row][col]:
                continue
            labels[row][col] = linked[labels[row][col]]

    return labels


def main():
    data = load_data('./blob_extraction_input.txt')
    labels = two_pass(data)
    save_data('./blob_extraction_output.txt',  labels)


main()

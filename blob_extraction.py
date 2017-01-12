

def load_data(filepath):
    data = []
    with open(filepath) as f:
        for line in f:
            row = [int(x) for x in line.strip()]
            data.append(row)
    return data


def find_neighboring_labels(row, col, data, labels):
    west = (row, col - 1)
    northwest = (row - 1, col - 1)
    north = (row - 1, col)
    northeast = (row - 1, col + 1)

    neighbors = [west, northwest, north, northeast]
    neighboring_labels = []
    for neighbor in neighbors:
        if neighbor[0] >= 0 and neighbor[0] < row_count and neighbor[1] >= 0 and neighbor[1] < col_count:
            if data[neighbor[0]][neighbor[1]]:
                neighboring_labels.append(labels[neighbor[0]][neighbor[1]])

    return neighboring_labels


def find_min_neighboring_label(neighboring_labels):
    min_label = None
    for label in neighboring_labels:
        if min_label:
            min_label = label if label.value < min_label.value else min_label
        else:
            min_label = label
    return min_label


class Label:

    def __init__(self, value):
        self.make_set()
        self.value = value

    def make_set(self):
        self.parent = self
        self.rank = 0


def two_pass(data):
    global row_count, col_count

    row_count = len(data)
    col_count = len(data[0])
    labels = [[0] * col_count for _ in range(row_count)]
    label_count = 0

    linked = {}

    # First pass
    for row in range(row_count):
        for col in range(col_count):
            if not data[row][col]:
                continue

            neighboring_labels = find_neighboring_labels(
                row, col, data, labels)
            if not neighboring_labels:
                label_count += 1
                next_lable = Label(label_count)
                labels[row][col] = next_lable

                linked[next_lable.value] = next_lable
                continue

            # Find the smallest label
            labels[row][col] = find_min_neighboring_label(
                neighboring_labels)

            all_root_labels = [linked[label.value]
                               for label in neighboring_labels]
            for label in neighboring_labels:
                linked[label.value] = find_min_neighboring_label(
                    all_root_labels)

    # Second pass
    for row in range(row_count):
        for col in range(col_count):
            if not data[row][col]:
                continue
            labels[row][col] = linked[labels[row][col].value]

    return labels


def union(x, y):
    xRoot = find(x)
    yRoot = find(y)
    # if x and y are already in the same set(i.e., have the same root or
    # representative)
    if xRoot == yRoot:
        return

    if xRoot.value < yRoot.value:
        yRoot.parent = xRoot
        return xRoot
    else:
        xRoot.parent = yRoot
        return yRoot

    # x and y are not in same set, so we merge them
    # if xRoot.rank < yRoot.rank:
    #     xRoot.parent = yRoot
    # elif xRoot.rank > yRoot.rank:
    #     yRoot.parent = xRoot
    # else:
    #     yRoot.parent = xRoot
    #     xRoot.rank = xRoot.rank + 1


def find(x):
    if x.parent != x:
        x.parent = find(x.parent)
    return x.parent


def save_data(filepath, data, labels):
    with open(filepath, 'w') as f:
        for row in range(row_count):
            for col in range(col_count):
                if data[row][col]:
                    f.write(str(labels[row][col].value))
                else:
                    f.write('0')
            f.write('\n')


def main():
    data = load_data('./blob_extraction_input.txt')
    labels = two_pass(data)
    save_data('./blob_extraction_output.txt',data, labels)


main()

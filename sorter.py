
def bubble_sort(sequence,attribute):
    changed = True
    length = len(sequence)

    if attribute == 'date':
        return sequence

    while changed:
        changed = False
        for index in range(1, length):
            diary1 = get_weight_by_attribute(sequence[index-1], attribute)
            diary2 = get_weight_by_attribute(sequence[index], attribute)
            if diary1 > diary2:
                sequence[index-1], sequence[index] = sequence[index], sequence[index-1]
                changed = True
        length -= 1

    if attribute != 'alphabetical':
        sequence.reverse()

    return sequence


def get_weight_by_attribute(diary, attribute):
    if attribute == 'alphabetical':
        return ord((diary[0])[0].lower())
    elif attribute == 'content':
        return len(diary[2])
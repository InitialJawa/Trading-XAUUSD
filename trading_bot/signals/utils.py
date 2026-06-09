def min_max_normalize(values):
    min_v = min(values)
    max_v = max(values)
    if max_v == min_v:
        return [50 for _ in values]
    return [((v - min_v) / (max_v - min_v)) * 100 for v in values]


def scale_to_0_100(value, min_val, max_val):
    if max_val == min_val:
        return 50
    return max(0, min(100, ((value - min_val) / (max_val - min_val)) * 100))


def reverse_scale(value, min_val, max_val):
    return 100 - scale_to_0_100(value, min_val, max_val)

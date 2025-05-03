from collections import defaultdict


def safe_format(template, values):
    return template.format_map(defaultdict(lambda key=None: f"{{{key}}}", values))

def safe_pos_format(template, args):
    count = template.count('{}')
    safe_args = list(args) + [''] * (count - len(args))
    return template.format(*safe_args[:count])
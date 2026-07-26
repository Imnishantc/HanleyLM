def safe_text(value):

    if value is None:
        return "-"

    return str(value)


def truncate(text, limit=250):

    text = safe_text(text)

    if len(text) <= limit:
        return text

    return text[:limit] + "..."


def percentage(value):

    return f"{value:.2f}%"


def score(value):

    return f"{value:.1f}/10"


def seconds(value):

    return f"{value:.2f}s"
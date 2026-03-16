from typing import Iterable


def average_ratios(numbers: Iterable[float]) -> float:
    """Compute the average of 100 / x for each non-zero x in `numbers`.

    Zeros are skipped. If there are no non-zero numbers, raises ValueError.

    Args:
        numbers: iterable of numeric values.

    Returns:
        The arithmetic mean of the ratios (100 / x) for non-zero x.

    Raises:
        TypeError: if `numbers` is not an iterable or contains non-numeric items.
        ValueError: if there are no non-zero numbers to divide by.
    """
    try:
        iterator = iter(numbers)
    except TypeError as exc:
        raise TypeError("numbers must be an iterable") from exc

    ratios = []
    for item in iterator:
        try:
            val = float(item)
        except (TypeError, ValueError) as exc:
            raise TypeError("all items in numbers must be numeric") from exc
        if val == 0.0:
            # skip zeros to avoid division-by-zero
            continue
        ratios.append(100.0 / val)

    if not ratios:
        raise ValueError("no non-zero numbers to divide by")

    return sum(ratios) / len(ratios)


if __name__ == "__main__":
    # Example usage
    print(average_ratios([10, 5, 0]))

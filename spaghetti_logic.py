from typing import Iterable, List
from pathlib import Path


def apply_markup(value: float, rate: float = 0.15) -> float:
    """Return value after applying a markup/percentage.

    Args:
        value: numeric input value.
        rate: markup rate (default 0.15 for +15%).

    Returns:
        The new value after markup.

    Raises:
        TypeError: if value or rate are not numbers.
    """
    try:
        return float(value) * (1.0 + float(rate))
    except (TypeError, ValueError) as exc:
        raise TypeError("value and rate must be numeric") from exc


def format_total(value: float, prefix: str = "Total:") -> str:
    """Format a numeric total as a human-readable string with 2 decimals.

    Example: format_total(12.345) -> "Total: 12.35"
    """
    return f"{prefix} {value:.2f}"


def log_results(results: Iterable[float], filename: str = "log.txt") -> None:
    """Append a representation of results to a log file.

    Uses Path to ensure cross-platform behavior. Writes one list per line.
    """
    path = Path(filename)
    # Ensure parent exists (no-op if current dir)
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(str(list(results)) + "\n")


from typing import Iterable, List, Union


def _validate_input(data: Iterable[Union[int, float]]) -> List[float]:
    """Convert input iterable to a list of floats.

    Raises TypeError if data is not iterable. Raises ValueError if any
    element cannot be converted to float.
    """
    try:
        iterator = iter(data)
    except TypeError as exc:
        raise TypeError("data must be an iterable of numbers") from exc

    out: List[float] = []
    for i, v in enumerate(iterator):
        try:
            out.append(float(v))
        except Exception as exc:
            raise ValueError(f"item at index {i} is not a number: {v!r}") from exc
    return out


def calculate_totals(values: Iterable[Union[int, float]], multiplier: float = 1.15) -> List[float]:
    """Return a new list where each input value is multiplied by multiplier.

    This is a pure function with no side-effects.
    """
    nums = _validate_input(values)
    return [n * multiplier for n in nums]


def format_total(value: float) -> str:
    """Return the display string for a single total value.

    Example: 12.345 -> "Total: 12.35"
    """
    return f"Total: {value:.2f}"


def print_totals(totals: Iterable[float]) -> None:
    """Print formatted totals to stdout, one per line."""
    for t in totals:
        print(format_total(t))


def write_log(totals: Iterable[float], path: str = "log.txt") -> None:
    """Append the representation of totals to the given log file.

    The format is kept intentionally compatible with the original implementation
    (it writes the string form of the Python list followed by a newline).
    """
    with open(path, "a") as f:
        f.write(str(list(totals)) + "\n")


def process_data(data: Iterable[Union[int, float]], multiplier: float = 1.15, log_path: str = "log.txt") -> List[float]:
    """High-level coordinator that mirrors the original behavior.

    - Validates and converts input
    - Calculates totals (multiplied by multiplier)
    - Prints formatted totals
    - Appends the list of totals to log_path
    - Returns the list of totals
    """
    totals = calculate_totals(data, multiplier=multiplier)
    print_totals(totals)
    write_log(totals, path=log_path)
    return totals


__all__ = ["process_data", "calculate_totals", "format_total", "print_totals", "write_log"]


if __name__ == "__main__":
    # Small example run when executed directly
    sample = [10, 20, 30]
    print("Processing sample data:")
    processed = process_data(sample)
    print("Processed:", processed)

def format_seconds(seconds: int) -> str:
    """
    Format seconds in MM:SS format
    """
    if seconds:
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes}:{seconds:02d}"
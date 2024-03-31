def cut_str(input_str: str, max_size: int, add_three_dots: bool = False) -> str:
    if input_str:
        if len(input_str) > max_size:
            result = input_str[:max_size]
            if add_three_dots:
                result += '...'
        else:
            result = input_str

        return result
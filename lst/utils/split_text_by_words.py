def split_text_by_words(text: str, max_chars_per_line: int) -> str:
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) <= max_chars_per_line:
            current_line += word + " "
        else:
            if len(word) > max_chars_per_line:
                lines.extend(
                    [current_line.strip()]
                    + [
                        word[i : i + max_chars_per_line]
                        for i in range(0, len(word), max_chars_per_line)
                    ]
                )
                current_line = ""
            else:
                lines.append(current_line.strip())
                current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    result = "\n".join(lines)
    if result != "":
        if result[0] == "\n":
            result = result[1:]
        return result
import re


def convert_invalid_characters(string: str) -> str:
    if string is not None:
        double_quotes = "\""
        question_mark = r"\?"
        right_quote = "’"
        invalid_filename_chars = "[\\/:*<>|]"

        string = re.sub(double_quotes, "", string)
        string = re.sub(question_mark, " ", string)
        string = re.sub(right_quote, "'", string)
        string = re.sub(invalid_filename_chars, "_", string)
        string = string.strip()

    return string

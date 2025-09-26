import language_tool_python

def lt_correct(text: str, lang: str = "en-US") -> str:
    tool = language_tool_python.LanguageToolPublicAPI(lang)  # χωρίς Java, deterministic αρκετά
    matches = tool.check(text)
    return language_tool_python.utils.correct(text, matches)

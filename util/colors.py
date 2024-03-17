class Colors:
    BOT_COLORS = [
        0x0E0E10,
        0xB59410,
        0x1B1B1B,
        0xFFCA4B,
        0xD0AF00,
        0xB69900,
        0x343434,
        0x414A4C
    ]
    DARK_GRAY = "[1;30m"
    RED = "[1;31m"
    YELLOW_GREEN = "[1;32m"
    GOLD = "[1;33m"
    YELLOW = "[1;33m"
    LIGHT_BLUE = "[1;34m"
    PINK = "[1;35m"
    TEAL = "[1;36m"
    WHITE = "[1;37m"
    RESET = "[1;0m"
    
    @staticmethod
    def interpolate_color(start_color, end_color, ratio):
        return tuple(int(start + (ratio * (end - start))) for start, end in zip(start_color, end_color))

    @staticmethod
    def make_ansi(col: tuple, text: str) -> str:
        return f"\033[38;2;{col[0]};{col[1]};{col[2]}m{text}\033[38;2;255;255;255m"

    @staticmethod
    def get_spaces(text: str) -> int:
        return len(text) - len(text.lstrip())

    @staticmethod
    def fade_horizontal(start_color: tuple, end_color: tuple, text: str, steps: int = 10) -> str:
        lines = text.splitlines()
        result = ""

        for lin in lines:
            carac = list(lin)
            for i, car in enumerate(carac):
                ratio = i / (len(carac) - 1) 
                color = Colors.interpolate_color(start_color, end_color, ratio)
                result += " " * Colors.get_spaces(car) + Colors.make_ansi(color, car.strip())
            result += "\n"
        return result.rstrip()
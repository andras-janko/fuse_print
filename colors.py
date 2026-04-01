# ANSI Color Code Utilities

class Color:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    @staticmethod
    def colored(text: str, color: str) -> str:
        return f'{color}{text}{Color.RESET}'

# Example Usage
if __name__ == '__main__':
    print(Color.colored('Hello, World!', Color.RED))
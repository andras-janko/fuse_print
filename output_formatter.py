# Output Formatter Utilities

class OutputFormatter:
    @staticmethod
    def format_success(message):
        return f'\033[92m{message}\033[0m'  # Green text

    @staticmethod
    def format_error(message):
        return f'\033[91m{message}\033[0m'  # Red text

    @staticmethod
    def format_warning(message):
        return f'\033[93m{message}\033[0m'  # Yellow text

    @staticmethod
    def format_info(message):
        return f'\033[94m{message}\033[0m'  # Blue text

    @staticmethod
    def format_debug(message):
        return f'\033[95m{message}\033[0m'  # Magenta text

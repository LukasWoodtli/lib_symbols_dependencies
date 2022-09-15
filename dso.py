import os


class Dso:

    def __init__(self, file_name, defined_symbols, undefined_symbols):
        self._dso_file_path = file_name
        self._defined_symbols = frozenset(defined_symbols)
        self._undefined_symbols = frozenset(undefined_symbols)

    def __eq__(self, other) -> bool:
        return self._dso_file_path == other._dso_file_path and \
                self._defined_symbols == other._defined_symbols and \
               self._undefined_symbols == other._undefined_symbols

    def get_so_name(self):
        return os.path.basename(self._dso_file_path)

    def get_defined_symbols(self):
        return self._defined_symbols

    def get_undefined_symbols(self):
        return self._undefined_symbols

    def __str__(self):
        return f"{self.get_so_name()}"

    def __repr__(self):
        ret = f"{self.get_so_name()}\n"
        ret += f"Undefined symbols: {len(self._undefined_symbols)}\n"
        ret += f"Defined symbols: {len(self._defined_symbols)}\n"
        return ret

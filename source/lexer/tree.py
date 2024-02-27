from tokens import TokenType
from scanner import Scanner


class TokenTypeTree:
    token_type: TokenType | None
    sub_dict: dict[str, 'TokenTypeTree']

    def __init__(self, tts: list[TokenType], depth: int):
        self.token_type = None
        sub_dict_prep = {}
        for tt in tts:
            if len(tt.symbol) == depth:
                # tts share suffix -> here at most once
                assert not self.token_type
                self.token_type = tt
            else:
                sub_dict_prep.setdefault(tt.symbol[depth], []).append(tt)
        self.sub_dict = {
            char: TokenTypeTree(sub_tts, depth + 1)
            for char, sub_tts in sub_dict_prep.items()
        }  # sub_dict_prep ! fst -> TokenTypeTree[snd, depth + 1] ` Map

    def walk(self, scanner: Scanner) -> TokenType:
        if scanner.peek in self.sub_dict:
            return self.sub_dict[scanner.consume()].walk(scanner)
        assert self.token_type
        return self.token_type

    def __repr__(self):
        return f'TTT | {str(self)}]'

    def __str__(self):
        return f'{self.token_type}, {self.sub_dict}'

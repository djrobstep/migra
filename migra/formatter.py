import re

class Formatter:

    def __init__(self, eager_parens: bool=True) -> None:
        # add other format wide configs
        self.eager_parens = eager_parens


    def create_policy(self, all_changes):
        if self.eager_parens:
            # only fails on check true params, so hard coding is ok
            for i, change in enumerate(all_changes):
                all_changes[i] = re.sub(r'with\s+check\s+true', 'with check (true)', change)
        return all_changes

    

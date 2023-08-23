class EntryMatcher:
    def __init__(self, entry) -> None:
        self.entry = entry

    def match(self, filters, eq_contains, and_or):
        if eq_contains:
            return self.eqmatch(filters, and_or)
        else:
            return self.containsmatch(filters, and_or)

    def eqmatch(self, filters, and_or):
        matched = False
        for field, value in filters:
            if and_or:
                matched = True
                if getattr(self.entry, field) != value:
                    matched = False
                    break
            else:
                if getattr(self.entry, field) == value:
                    matched = True
                    break
        return matched    
            
    def containsmatch(self, filters, and_or):
        matched = False
        for field, value in filters:          
            if and_or:
                matched = True
                if getattr(self.entry, field).find(value) == -1:
                    matched = False
                    break
            else:
                if getattr(self.entry, field).find(value) != -1:
                    matched = True 
                    break
        return matched
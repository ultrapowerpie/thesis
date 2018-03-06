from collections import defaultdict as dd


class ArticleCounts:

    def __init__(self, filename):
        self.counts_map = self.build_from_file(filename)

    def get_counts(self, has_keywords, tags):
        tags = tuple(sorted(tags))
        return self.get_counts(has_keywords, tags)

    @staticmethod
    def get_index(year, month):
        return (int(year)-2001)*12 + int(month) - 1

    @staticmethod
    def build_from_file(filename):
        counts_map = dd(lambda:list())
        is_tags = False
        is_keywords = False
        has_keywords = None
        with open(filename, 'rb') as f:
            for line in f:
                if is_keywords:
                    has_keywords = 'TRUE' in line
                    is_keywords = False

                elif is_tags:
                    tags = tuple(sorted(line[:-1].split(',')))
                    is_tags = False
                    counts = []

                    if 'KEYWORDS' in line:
                        is_keywords = True
                        continue

                    if 'TAGS' in line:
                        is_tags = True
                        continue

                    counts_map[has_keywords][tags].append(counts)

        return counts_map

import re


class Utils:
    @staticmethod
    def scoresaber_id_from_url(url):
        pattern = re.compile(r'(https?://scoresaber\.com/u/)?(\d{17})')
        match = re.match(pattern, url)

        if match:
            return match.group(2)

        return None

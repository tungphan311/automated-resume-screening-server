import re


github_pattern = "(?:https?://)?(?:www[.])?github[.]com/[\w-]+/?"
facebook_pattern = "(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?"
twitter_pattern = "/http(?:s)?:\/\/(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+)/"
linked_pattern = "http(s)?:\/\/([\w]+\.)?linkedin\.com\/in\/[A-z0-9_-]+\/?"
phone_pattern = r"(\+[0-9 ]{1,3})?[0-9 ]{7,}"
email_pattern = "(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}"

class RegexHelper():
    """
    Find things using regex.
    Enable first flag for returning single string, otherwise an array.
    """

    @staticmethod
    def find_github_link(text, first=True):
        RegexHelper.find(github_pattern, text, first)


    @staticmethod
    def find_fb_link(text, first=True):
        return RegexHelper.find(facebook_pattern, text, first)

    @staticmethod
    def find_twitter_link(text, first=True):
        return RegexHelper.find(twitter_pattern, text, first)

    @staticmethod
    def find_linkedin_link(text, first=True):
        return RegexHelper.find(linked_pattern, text, first)

    @staticmethod
    def find_phone_number(text, first=True):
        return RegexHelper.find(phone_pattern, text, first)

    @staticmethod
    def find_email(text, first=True):
        return RegexHelper.find(email_pattern, text, first)

    @staticmethod
    def find(pattern, text, first):
        matches = re.finditer(pattern, text)
        res = []
        for _, match in enumerate(matches, start=1):
            res.append(match.group())
        
        if len(res) == 0:   
            return None
        if first:           
            return res[0]
        return res
    
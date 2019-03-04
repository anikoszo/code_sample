class Palindrome:
    @staticmethod
    def is_palindrome(word):

        if word.lower() == word.lower()[::-1]:
            return "true"
        else:
            return "false"


word = input()
print(Palindrome.is_palindrome(word))

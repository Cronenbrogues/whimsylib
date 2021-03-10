import random


class Zalgo:
    def __init__(self):
        self.numAccentsUp = (1, 3)
        self.numAccentsDown = (1, 3)
        self.numAccentsMiddle = (1, 2)
        self.maxAccentsPerLetter = 3
        self.zalgoChance = 1
        self.dd = [
            "̖",
            " ̗",
            " ̘",
            " ̙",
            " ̜",
            " ̝",
            " ̞",
            " ̟",
            " ̠",
            " ̤",
            " ̥",
            " ̦",
            " ̩",
            " ̪",
            " ̫",
            " ̬",
            " ̭",
            " ̮",
            " ̯",
            " ̰",
            " ̱",
            " ̲",
            " ̳",
            " ̹",
            " ̺",
            " ̻",
            " ̼",
            " ͅ",
            " ͇",
            " ͈",
            " ͉",
            " ͍",
            " ͎",
            " ͓",
            " ͔",
            " ͕",
            " ͖",
            " ͙",
            " ͚",
            " ",
        ]
        self.du = [
            " ̍",
            " ̎",
            " ̄",
            " ̅",
            " ̿",
            " ̑",
            " ̆",
            " ̐",
            " ͒",
            " ͗",
            " ͑",
            " ̇",
            " ̈",
            " ̊",
            " ͂",
            " ̓",
            " ̈́",
            " ͊",
            " ͋",
            " ͌",
            " ̃",
            " ̂",
            " ̌",
            " ͐",
            " ́",
            " ̋",
            " ̏",
            " ̽",
            " ̉",
            " ͣ",
            " ͤ",
            " ͥ",
            " ͦ",
            " ͧ",
            " ͨ",
            " ͩ",
            " ͪ",
            " ͫ",
            " ͬ",
            " ͭ",
            " ͮ",
            " ͯ",
            " ̾",
            " ͛",
            " ͆",
            " ̚",
        ]
        self.dm = [
            " ̕",
            " ̛",
            " ̀",
            " ́",
            " ͘",
            " ̡",
            " ̢",
            " ̧",
            " ̨",
            " ̴",
            " ̵",
            " ̶",
            " ͜",
            " ͝",
            " ͞",
            " ͟",
            " ͠",
            " ͢",
            " ̸",
            " ̷",
            " ͡",
        ]

    def zalgofy(self, text):
        """
        Zalgofy a string
        """
        new_word = ""

        for letter in text:
            if not letter.isalpha():
                new_word += letter
                continue

            if random.random() >= self.zalgoChance:
                new_word += letter
                continue

            numU = random.randint(self.numAccentsUp[0], self.numAccentsUp[1])
            numD = random.randint(self.numAccentsDown[0], self.numAccentsDown[1])
            numM = random.randint(self.numAccentsMiddle[0], self.numAccentsMiddle[1])
            numAccents = 0
            while numAccents < self.maxAccentsPerLetter and numU + numM + numD != 0:
                randint = random.randint(0, 2)
                if randint == 0:
                    if numU > 0:
                        letter = self.combineWithDiacritic(letter, self.du)
                        numAccents += 1
                        numU -= 1
                elif randint == 1:
                    if numD > 0:
                        letter = self.combineWithDiacritic(letter, self.dd)
                        numD -= 1
                        numAccents += 1
                else:
                    if numM > 0:
                        letter = self.combineWithDiacritic(letter, self.dm)
                        numM -= 1
                        numAccents += 1

            new_word += letter

        return new_word

    def combineWithDiacritic(self, letter, diacriticList):
        """
        Combines letter and a random character from diacriticList
        """
        return (
            letter.strip()
            + diacriticList[random.randrange(0, len(diacriticList))].strip()
        )

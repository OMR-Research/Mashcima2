from enum import Enum


class TypeDuration(str, Enum):
    """
    Type-duration of a note/rest (i.e. whole, quarter, 16th).
    It encodes what the musical symbol looks like, not how much time it
    actually takes up. (e.g. a triplet will be an eighth type; a grace
    note has type but no duration)

    Based on the MusicXML <type> element.
    """
    
    thousand_twenty_fourth = "1024th"
    five_hundred_twelfth = "512th"
    two_hundred_fifty_sixth = "256th"
    sixty_fourth = "64th"
    thirty_second = "32nd"
    sixteenth = "16th"
    eighth = "eighth"
    quarter = "quarter"
    half = "half"
    whole = "whole"
    breve = "breve"
    long = "long"
    maxima = "maxima"

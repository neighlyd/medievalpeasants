# coding: utf8
import re


class CurrencyConverter:
    '''
    A class to help convert medieval English money into its various forms -
    pounds(£/l.), marks(m.), shillings(s.), denarii(d.).
    There were:
        12 denarii in a shilling.
        160 denarii in a mark.
        240 denarii in a pound.

    The input for this program is a string - type in the amount that you see in the manuscript (including finial j's if
    you wish). Case does not matter.
    The only order that matters is that:
        The currency sign MUST come after the Roman Numerals in ALL cases - e.g. xij l. vj s. iiij d.
    '''

    def __init__(self, nums):
        self.currency = self.__convert_money(nums)
        self.in_denarius = self.__to_denarius()
        self.in_marks = self.__to_marks()
        self.in_lsd = self.__to_lsd()

    def __to_denarius(self):
        # reduces currency to a single integer representing the denarii amount.
        total = 0
        for n in self.currency:
            if n == 'l':
                total += (self.currency[n][1]*240)
            elif n == 'm':
                total += (self.currency[n][1]*160)
            elif n == 's':
                total += (self.currency[n][1]*12)
            elif n == 'd':
                total += (self.currency[n][1])
        return total

    def __to_marks(self):
        # converts money to the number of marks (using floats).
        # Fun fact - there wasn't a mark coin, rather it was a unit of account.
        d = self.in_denarius
        m = d/160
        return m

    def __to_lsd(self):
        # Find out how much the amount was in £ s. d. This method is useful when a denarii or mark amount is known and you
        # want to up-convert.
        # returns value in a list.
        d = self.in_denarius
        l = d//240
        d -= l*240
        s = d//12
        d -= s*12
        # return [l, s, d]
        return '£{0} {1}s. {2}d.'.format(l, s, d)

    def __convert_numerals(self, num):
        # Method for converting from Roman to Arabic numerals.
        letter_vals = {
            'm': 1000,
            'd': 500,
            'c': 100,
            'l': 50,
            'x': 10,
            'v': 5,
            'i': 1,
        }
        total = 0
        prev_val = None
        # Because Roman Nums are influenced by those that come AFTER them, iterate through the string backwards.
        for n in reversed(num):
            # start with assumption that the value will be what it 'ought' to be.
            cur_val = letter_vals[n]
            # if the current value is not less than the previous value, we're all good. Just add it to the running sum.
            if (prev_val is None) or (prev_val <= cur_val):
                total += cur_val
            # if current value IS less than previous value (i.e. I before V - remember, we're going backwards here),
            # then subtract the current value from the total (we had 5, but we have to subtract 1 from it).
            else:
                total -= cur_val
                prev_val = cur_val
        return total

    def __convert_money(self, nums):
        # Method for extracting the money amounts from the user input.
        # the regex pattern used to find the monetary input.
        pattern = r'((\b[mdclxvij\d]+)\s*([£lmsd]))'
        # A dictionary representing each currency position with a list holding its original [Roman Num, Arabic Num]
        currency_output = {'l': [None, 0], 'm': [None, 0], 's': [None, 0], 'd': [None, 0]}
        # compile regex pattern and tell it to ignore case.
        regex = re.compile(pattern, re.IGNORECASE)
        for m in regex.findall(nums):
            # assign the first group (i.e. the roman numerals) to the first part of list in dict keyed to its currency
            # value based on index (i.e. m[2]).
            # the purpose of this is to preserve the input for later output to the user if they want to retrieve the
            # original Latin.
            currency_output[re.sub(r'£', 'l', m[2])][0] = m[1]
            # check if the entry is in Latin or is Arabic. If Arabic, convert to int and store, if not strip out
            # medieval finial j and then push through Roman Num converter to and store int for calculations.
            if m[1].isalpha():
                currency_output[re.sub(r'£', 'l', m[2])][1] = self.__convert_numerals(re.sub(r'[Jj]', 'i', m[1]))
            else:
                # will update this later to convert Arabic to Roman.
                currency_output[re.sub(r'£', 'l', m[2])][1] = int(m[1])
        return currency_output
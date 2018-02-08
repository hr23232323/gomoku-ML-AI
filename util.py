def num_to_char(num):
    return chr(ord('a') + num)

def char_to_num(letter):
    return ord(letter.lower()) - ord('a')
import hashlib
import bcrypt

# # SHA1
# m=hashlib.sha1(b"Chulalongkorn").hexdigest()
# # MD5
# m=hashlib.md5(b"Chulalongkorn").hexdigest()
# # BCRYPT
# salt = bcrypt.gensalt()
# m=bcrypt.hashpw(b"Chulalongkorn", salt)

# print("SHA1 :", m)
# print("MD5 :", m)
# print("bcrypt :", m)


with open("10k-most-common.txt", "r") as f:
    words = f.read().splitlines()

Answer = "d54cc1fe76f5186380a0939d2fc1723c44e8a5f7"

def Recursive(word, index):
    if index == len(word):
        SHA1 = hashlib.sha1(bytes(word, "utf-8")).hexdigest()
        # print("word is: ", word)
        if SHA1 == Answer:
            print("Password is : ", word)
        return
    
    # Upper case
    wordUpper = word[:index] + word[index:index+1].upper() + word[index+1:]
    Recursive(wordUpper, index + 1)
    
    # Lower case
    wordLower = word[:index] + word[index:index+1].lower() + word[index+1:]
    Recursive(wordLower, index + 1)
    
    # Special case
    if word[index].lower() == 'o':
        wordSpecial = word[:index] + '0' + word[index+1:]
        Recursive(wordSpecial, index+1)
    if word[index].lower() == 'i' or word[index].lower() == 'l':
        wordSpecial = word[:index] + '1' + word[index+1:]
        Recursive(wordSpecial, index+1)

for word in words: 
    Recursive(word, 0)
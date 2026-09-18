import datetime
ciphertext = 'PRCSOFQX FP QDR AFOPQ CZSPR LA JFPALOQSKR. QDFP FP ZK LIU BROJZK MOLTROE.'
dictionary = []
answer = dict()
with open("Dictionary.txt", "r") as file:
    dictionary = file.read().split()

for i in range(0,26):
    temp_decrypted_sentence = ''
    for word in ciphertext:
        if word.isalpha():
            temp_decrypted_sentence += chr((ord(word) - ord('A') + i) % 26 + ord('A')).lower()
        else:
            temp_decrypted_sentence += word
    freq = 0
    for word in temp_decrypted_sentence.split():
        if word in dictionary:
            freq += 1
    
    answer[temp_decrypted_sentence] = freq


answer_sorted = sorted(answer.items(), key=lambda item: item[1], reverse=True)
for i in answer_sorted:
    print(i[0], " -> freq: " + str(i[1]))
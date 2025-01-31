count_vowels=0
count_consonant=0
variable=input('Enter your string input:')
vowels='AEIOUaeiou'
for i in variable:
    if i in vowels:
        count_vowels+=1
    else:
        count_consonant+=1
print('Number of vowels:', count_vowels)
print('Number of consonants:',count_consonant)
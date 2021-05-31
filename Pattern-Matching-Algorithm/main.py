import string
import sys

n_cols = 26 #Number of Letters

lettersMap = dict(zip(string.ascii_uppercase, range(n_cols))) #Maps a letter to an index

def createDelta(string1):
    n_rows = len(string1) + 1 # Number of rows in the matrix
    delta = [[0 for i in range(n_cols)] for j in range(n_rows)] #Initialize the matrix 

    for i in range(n_rows):
        for j in range(n_rows - 1):
            if (string1[:i] + string1[j]) == string1[:(i + 1)]:
                delta[i][lettersMap[string1[j]]] = i + 1 # Map each correct input to the next state
                continue
            else: # Verify each suffix of the pattern with each prefix of the text
                new_string = string1[:i] + string1[j]
                l = 1
                r = len(new_string) - 1 # If they have the same length slice the first/last letter
                if (len(new_string) > len(string1[:(i + 1)])):
                    r = len(string1[:(i + 1)]) # If they don't slice only the bigger one
                while l < len(new_string) and r > 0:
                    if (new_string[l:] == string1[:r]): #Same as before with extra slicing
                        delta[i][lettersMap[string1[j]]] = len(new_string[l:])
                        break
                    l = l + 1
                    r = r - 1
    return delta


def stringMatching(string1, string2, delta):
    q = 0
    answerList = []
    for i in range(len(string2)):
        q = delta[q][lettersMap[string2[i]]]
        if q == len(string1): # If the current state matches the pattern length
            answerList.append(i - (len(string1) - 1)) # We found a match
    return answerList

def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f = open(input_file, "r")
    string1 = f.readline()
    string2 = f.readline()

    string1 = string1.strip()
    string2 = string2.strip()

    f.close()

    delta = createDelta(string1) # Creates the Delta Matrix

    g = open(output_file, "w")

    ans = stringMatching(string1, string2, delta) # Creates a list with the required positions in the string

    for item in range(len(ans)):
        g.write(str(ans[item]) + " ")
    g.write("\n")
    g.close()


if __name__=="__main__":
    main()

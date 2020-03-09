#!/usr/local/bin/python3.7
# Created by ioluwayo on 2017-02-14 originally at https://github.com/ioluwayo/BME-808/blob/master/LAB4/needle.py.
# Personized by Karobben on 2019-08-18

"""
This program determines the optimal global alignment of two sequences using the Nedleman-Wunsh algorithm.
Input: Base file
Output: similest sentences
"""
import sys, os, time, requests
import numpy as np
from string import digits

remove_digits = str.maketrans('', '', digits)

"""
These functions are for Data collecting and Calculating
"""
List_T = ["Wrods_All","Words","Words_Wrong","Sentence","Sentence_Wrong","Sentence_Words","Sentence_WongWords"]
List_N = np.array([0]*7)
def Word_RC(INPUT,Word_R):
    #tmp_W = open("tmp.word",'w')
    #tmp_W.write(Word_R.split(' ')[2])
    #tmp_W.close()
    if INPUT == Word_R:
        return "Correct", 1, 0
    else:
        return  "Wrong", 1, 1

def Sentence_RC(Sentence_R):
    Sentence = Sentence_R.split("\n")[2]
    Words_N = len(Sentence.split(" "))-2
    Words_Wr = 0
    if Sentence_R.split("\n")[1].replace(" ","") == "":
        Result = "Correct "
        return Result, Words_N, Words_Wr
    else:
        #counting the number of the wroing words
        for i in Sentence.split(" "):
            if "[" in i:
                Words_Wr += 1
        Result = "Wrong "
        return Result, Words_N, Words_Wr

def WorS(INPUT,Result,F_log):
    global List_N
    Result_t = np.array([0]*7)
    if len(INPUT.split(" ")) == 1:
        A,B,C = Word_RC(INPUT,Result)
        Result_t[0] += 1
        Result_t[1] += 1
        Result_t[2] += C
    elif len(INPUT.split(" ")) > 1:
        A,B,C = Sentence_RC(Result)
        D = 0
        if C != 0:
            D=1
        Result_t[0] += B
        Result_t[3] += 1
        Result_t[4] += D
        Result_t[5] += B
        Result_t[6] += C
    List_N += Result_t
    F_log.write(time.ctime()+"\t"+"\t".join(map(str,Result_t))+"\n")
    F_log.close()

'''
This function is for sending imput to belive
'''
#def blive_send(MSG):
    #cookie define
#    CMD = "/media/ken/Data/script/Instructor/Python/bin/Python-Send_blive.py "+ MSG +" &"
#    os.system(CMD)

"""
Done
"""
def calculatePercentIdentity(sequence1,sequence2):
    """
    This function accepts 2 sequences and calculates the percent identity and percent gaps.
    Percent identity is calculated by multiplying the number of matches in the pair by 100 and
    dividing by the length of the aligned region, including gaps.
    Identity scoring only counts perfect matches, and does not consider the degree of similarity nucleotides.
    Note that only internal gaps are included in the length, not gaps at the sequence ends.
    :param sequence1:
    :param sequence2:
    :return:
    """
    sequence1 = sequence1.rstrip("_")
    sequence2 = sequence2.rstrip("_")
    if len(sequence1)<len(sequence2):
        shorter =len(sequence1)
    else:
        shorter =len(sequence2)
    matches = 0
    gaps =0
    for i in range(shorter):
        if sequence1[i] == sequence2[i]:
            matches+=1
        elif sequence1[i] == '_' or sequence2[i]== '_':
            gaps+=1
    percentIdentity = matches*100.0/shorter
    percentgaps =  gaps *100.0/shorter
    return percentIdentity,percentgaps

def buildAlignment(seq1, seq2, direction):
    """
    This function uses a directional string of the form DHVDD... (D = Diagonal, H = horizontal, and V = vertical edge)
    to create an alignment on 2 sequences
    e.g     SEQ 1: ACT__GGTCAATCG
            SEQ 2: ACTTCAATCGGT__
    :param seq1:
    :param seq2:
    :param direction:
    :return:
    """
    l1 = 0
    l2 = 0
    align1=""
    align2 =""
    for i in range(len(direction)):
        if direction[i] == "D":
            if l1 < len(seq1):
                align1 += seq1[l1]
            if l2 < len(seq2):
                align2 += seq2[l2]
            if l1>=len(seq1):
                align1 +="_"
            if l2 >=len(seq2):
                align2+="_"
            l1+=1
            l2+=1
        elif direction[i] == "H":
            if l2 < len(seq2):
                align2+=seq2[l2]
            if l1>=0:
                align1 += "_"
            l2+=1
        else:
            if l1< len(seq1):
                align1+=seq1[l1]
            if l1>=0:
                align2+="_"
            l1+=1
    return align1,align2

def buildDirectionalString(matrix,gapScore):
    """
    This function uses a simple path finding algorithm.
    It builds a directional string based on the values in a matrix.
    It traces the path from the last cell i.e matrix[-1][-1] to the first cell i.e matrix[-1][-1] following
    the edges that led to the optimal score in each cell.
    :param matrix:
    :param gapScore:
    :return:
    """
    currentRow = len(matrix)-1
    currentCol = len(matrix[0])-1
    direction = ""
    # start from the end and build a string with either D, H, V based on edges leading optimal score
    while currentRow or currentCol:#
        if currentRow == 0:
            # then we have a horizontal gap. use horizontal only. gaps for the vertical sequence
            direction = "H"+direction
            currentCol -= 1
        elif currentCol == 0:
            # then we us the vertical sequence only.. gaps for the horizontal sequence
            direction = "V"+direction
            currentRow -= 1
        elif matrix[currentRow-1][currentCol]+gapScore == matrix[currentRow][currentCol]:
            #then we use the vertical sequence...gap for the horizontal sequence
            direction = "V"+direction
            currentRow -= 1
        elif matrix[currentRow][currentCol-1]+gapScore == matrix[currentRow][currentCol]:
            # then we use the horizontal sequence.. gap for the vertical sequence
            direction = "H"+direction
            currentCol -=1
        else:
            # for sure its from the diagonal
            direction = "D"+ direction
            currentRow -= 1
            currentCol -= 1
    return direction

def find_global_alignment(pathToSequence1, patheTosequence2, match = 5, mismatch = -1, gap = -1.9):
    """
    This function accepts the relative path to 2 files containing DNA sequences(FASTA format) as input and find the
     global alignment of the sequences in the files. It prints out the score, alignment, percent identity & percent gaps
    The scoring function can also be specified by passing the match, mismatch and gap scores to the function.
    :param pathToSequence1:
    :param patheTosequence2:
    :param match: (optional) default = 1
    :param mismatch: (optional) default = 0
    :param gap: (optional) default = -1
    :return: alignment1, alignment2, score, percentIdentity, percentGap
    """
    sequence1 = pathToSequence1
    sequence2 = patheTosequence2
    lengthOfSeq1 = len(sequence1)
    lengthOfSeq2 = len(sequence2)
    matrix = [[0 for x in range(lengthOfSeq2 + 1)] for y in range(lengthOfSeq1 + 1)] # initialize matrix with zeros
    # now we initialize 1st row with 0.-1.-2.-3....-n
    for i in range(lengthOfSeq1 + 1):
        matrix[i][0] = i * -1  # columns of row 0
    for i in range(lengthOfSeq2 + 1):
        matrix[0][i] = i * -1  # rows of column 0
    # now we fill the matrix boxes with the highest of the value based on scoring rule
    for i in range(1, lengthOfSeq1 + 1):  # for each element in the row
        for j in range(1, lengthOfSeq2 + 1):  # for each element in the column
            if sequence1[i - 1] == sequence2[j - 1]:
                # there is a match
                matchScore = match + matrix[i - 1][j - 1]
            else:
                # no match
                matchScore = mismatch + matrix[i - 1][j - 1]
            # always have to calculate the gap scores.
            hGapScore = gap + matrix[i - 1][j]  # horizontal gap
            vGapScore = gap + matrix[i][j - 1]  # vertical gap
            matrix[i][j] = max(matchScore, hGapScore, vGapScore)
    # now we've got the matrix filled up. matrix[N][M] has the final score:
    score = matrix[-1][-1] # the global alignment score is the value of the last cell of the matrix
    direction = buildDirectionalString(matrix, gapScore = gap)
    alignment1, alignment2 = buildAlignment(sequence1,sequence2,direction)
    percentIdentity, percentGap = calculatePercentIdentity(alignment1, alignment2)
    return alignment1, alignment2, score, percentIdentity, percentGap

def Mark(Seq1,Seq2):
    Seq1 = list(Seq1)
    Seq2 = list(Seq2)
    Mark = list(" " * len(Seq1))
    for i in range(len(Seq1)):
        if Seq1[i] != Seq2[i]:
            Mark[i] = "X"
            Seq2[i] = Seq2[i]
        if "_" == Seq1[i] or "_" == Seq2[i]:
            Mark[i] = "."
    return " "*7 + "".join(Mark) , "SEQ 2: "+"".join(Seq2)

def Campare(Seq1,Seq2):
    alignment1, alignment2, score, percentIdentity, percentGap = find_global_alignment(Seq1,Seq2)
    A = "-----OPTIMAL GLOBAL ALIGNMENT-----" + "\n"
    B = "Score = " + str(score) + "\n"
    C = "SEQ 1: "+ alignment1 + "\n"
    D,E = Mark(alignment1,alignment2)
    #E = "SEQ 2: " + alignment2 + "\n"
    F = "Only aligned region is used to calculate percentage.\n"
    G = "Percent identity =" + str(percentIdentity) + "%\n"
    H = "Percent Gap ="+ str(percentGap)+"%\n"
    #Print = A+B+C+D+E+F+G+H
    Print = C+D+"\n"+E
    return alignment2 ,Print , score

def read_DB(f):
    DB = f.read()
    DB = list(set(DB.split("\n")))
    DB.remove("")
    return DB

def run(Seq,DB):
    Result = []
    Scores = []
    for i in  DB:
        alignment1, String,score = Campare(i, Seq)
        Result += [String]
        Scores += [score]
    return alignment1, Result[Scores.index(max(Scores))]

DB = read_DB(open(sys.path[0] +'/Needlman/Word',"r"))

Num = 0

def main(Seq,DB,Num):
    Result1 =Seq
    Result2 =""
    ResultT ="False"
    if Seq != "":
        Seq = Seq.lower().strip()
        Seq = Seq.translate(remove_digits)
        F_log = open(sys.path[0]+"/Needlman/En.log","a")
        if Seq in DB:
            Num +=1
            ResultT ="True"
            #rint("You Are Right!!",Num,"\n\n")
            Result2 = Seq
            F_log.write(time.ctime()+"\t"+"\t".join(map(str,np.array([1]*2+[0]*5)))+"\n")
            F_log.close()
        else:
            Num = 0
            alignment1, Result = run(Seq,DB)
            #print(run(Seq,DB))
            WorS(alignment1,Result,F_log)
            Result1 = Result.split('\n')[-1].replace("SEQ 2: ",'')
            Result2 = Result.split('\n')[0].replace("SEQ 1: ",'')
    return Num,Result1, Result2, ResultT

#Num, Result = main("biolog",DB,Num)

"""
Run the RSA for 100 times with a string size of 30 with
p = 41, q = 43, e = 167, d = 503 and record the result of each run.
"""
import RSA
import RSA_1
from Elgamal import Elgamal
import random
import string
import xlwt

# All variables
p = 41  # large prime
q = 43  # large prime
a = 37
l = [5, 10, 15, 20, 25, 30]   # string length
n = 100  # number of runs

wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Sheet 1')
row = 0
sheet1.write(row, 0, 'RSA')
row += 1
sheet1.write(row, 0, 'Variables')
sheet1.write(row, 1, 'p={}'.format(p))
sheet1.write(row, 2, 'q={}'.format(q))
sheet1.write(row, 3, 'a={}'.format(a))
sheet1.write(row, 4, 'Fixed e & d:')
sheet1.write(row, 5, 'e=167')
sheet1.write(row, 6, 'd=503')
row += 1
sheet1.write(row, 0, 'string length')
sheet1.write(row, 1, 'RSA random e & d')
sheet1.write(row, 2, 'RSA fixed e & d')
sheet1.write(row, 3, 'Elgamal')

rsa = RSA.RSA((p, q))
rsa_1 = RSA_1.RSA((p, q))

for i in range(len(l)):
    x = [''.join(random.choice(string.ascii_letters)
                 for _ in range(l[i])) for _ in range(n)]
    row += 1
    t = rsa.run_n(x)
    sheet1.write(row, 0, l[i])
    sheet1.write(row, 1, round(t, 4))

    t = rsa_1.run_n(x)
    sheet1.write(row, 2, round(t, 4))

    elgamal = Elgamal((p, a))
    t = elgamal.run_n(x)
    sheet1.write(row, 3, round(t, 4))

wb.save('./Results/fixed_RSA_result_2.xls')

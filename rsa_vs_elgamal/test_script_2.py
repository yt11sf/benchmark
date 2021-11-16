"""
Run the RSA for 100 times with a string size of [20, 30] 
with p = 41, q = 43 and record the result of each run.
"""
from RSA import RSA
import random
import string
import xlwt

# All variables
p = 41  # large prime
q = 43  # large prime
l = [20, 30]   # string length
n = 100  # number of runs

wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Sheet 1')

row = 0
sheet1.write(row, 0, 'RSA')
row += 1
sheet1.write(row, 0, 'Variables')
sheet1.write(row, 1, 'p={}'.format(p))
sheet1.write(row, 2, 'q={}'.format(q))
row += 1
sheet1.write(row, 0, 'string')
sheet1.write(row, 1, 'x1')
rsa = RSA((p, q))
for i in range(n):
    row += 1
    x1 = ''.join(random.choice(string.ascii_letters) for _ in range(l[0]))
    t = rsa.run_1(x1)
    sheet1.write(row, 0, x1)
    sheet1.write(row, 1, round(t, 4))


row = 2
sheet1.write(row, 3, 'string')
sheet1.write(row, 4, 'x2')
rsa = RSA((p, q))
for i in range(n):
    row += 1
    x2 = ''.join(random.choice(string.ascii_letters) for _ in range(l[1]))
    t = rsa.run_1(x2)
    sheet1.write(row, 3, x2)
    sheet1.write(row, 4, round(t, 4))

wb.save('./Results/run_1_result_1.xls')

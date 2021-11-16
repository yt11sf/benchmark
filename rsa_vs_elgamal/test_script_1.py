"""
Run the algorithms for 100 times with a string size of [5, 10, 15, 20, 25, and 30] 
with p = [7, 41, 241], q = [5, 43, 251], a = [2, 37, 211] and record the results.
"""
from RSA import RSA
from Elgamal import Elgamal
import random
import string
import xlwt

# All variables
p = [7, 41, 241]  # large prime
q = [5, 43, 251]  # large prime
a = [2, 37, 211]  # ∈ Z^*_p
l = [5, 10, 15, 20, 25, 30]   # string length
n = 100  # number of runs

assert len(p) == len(q) == len(a), 'check length of p, q, a'
wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Sheet 1')

row = 0
for j in range(len(p)):
    sheet1.write(row, 0, 'Variables')
    sheet1.write(row, 1, 'p={}'.format(p[j]))
    sheet1.write(row, 2, 'q={}'.format(q[j]))
    sheet1.write(row, 3, 'a={}'.format(a[j]))
    row += 1
    sheet1.write(row, 0, 'String length')
    sheet1.write(row, 1, 'RSA')
    sheet1.write(row, 2, 'Elgamal')
    row += 1
    for i in range(len(l)):
        x = [''.join(random.choice(string.ascii_letters)
                     for _ in range(l[i])) for _ in range(n)]
        print('Time consumed for ', n, ' runs with ',
              l[i], 'string length with p=', p[j], ' q=', q[j], ' a=', a[j])
        sheet1.write(row, 0, l[i])

        rsa = RSA((p[j], q[j]))
        t = rsa.run_n(x)
        print('RSA\t: {:.4f} milliseconds'.format(t))
        sheet1.write(row, 1, round(t, 4))

        elgamal = Elgamal((p[j], a[j]))
        t = elgamal.run_n(x)
        print('Elgamal\t: {:.4f} milliseconds'.format(t))
        sheet1.write(row, 2, round(t, 4))
        row += 1
    row += 1

wb.save('run_n_result.xls')

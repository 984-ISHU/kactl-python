"""
 * Author: Simon Lindholm
 * Date: 2016-09-06
 * License: CC0
 * Source: me
 * Description: Extension to SolveLinear to get all uniquely determined values.
 * Status: tested on kattis:equationsolverplus
"""

# See SolveLinear.py - to get uniquely determined values:
# In the elimination loop, change:
#   for j in range(i + 1, n):
# to:
#   for j in range(n):
#       if j != i:
#
# Then at the end, add:
# undefined = float('nan')
# x[:] = [undefined] * m
# for i in range(rank):
#     unique = True
#     for j in range(rank, m):
#         if abs(A[i][j]) > EPS:
#             unique = False
#             break
#     if unique:
#         x[col[i]] = b[i] / A[i][i]

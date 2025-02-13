import pandas as pd
from collections import Counter

# Data setup
data = """
DrawDate,Ball 1,Ball 2,Ball 3,Ball 4,Ball 5,Thunderball
11-Jan-25,1,20,39,33,15,5
10-Jan-25,27,37,16,18,23,13
08-Jan-25,14,35,2,30,16,13
07-Jan-25,27,35,26,10,3,4
04-Jan-25,14,17,5,11,35,8
03-Jan-25,35,1,2,31,39,13
01-Jan-25,6,18,5,32,36,4
31-Dec-24,9,38,18,29,33,10
28-Dec-24,27,17,21,34,6,3
27-Dec-24,27,6,20,30,29,5
25-Dec-24,36,39,13,32,9,8
24-Dec-24,6,19,13,1,8,13
21-Dec-24,26,31,38,13,7,6
20-Dec-24,13,26,16,10,39,12
18-Dec-24,19,37,15,7,28,4
17-Dec-24,17,31,36,32,16,6
14-Dec-24,16,9,33,3,23,14
13-Dec-24,18,17,3,16,28,11
11-Dec-24,30,15,8,9,16,7
10-Dec-24,39,9,36,17,11,13
07-Dec-24,13,8,25,5,29,12
06-Dec-24,29,30,11,10,32,14
04-Dec-24,10,4,20,1,33,13
03-Dec-24,38,22,13,2,32,9
30-Nov-24,29,12,13,23,8,13
29-Nov-24,21,9,35,32,25,13
27-Nov-24,8,3,34,21,33,6
26-Nov-24,8,22,6,18,24,14
23-Nov-24,37,39,5,17,27,13
22-Nov-24,25,7,17,19,13,2
20-Nov-24,12,39,4,26,29,7
19-Nov-24,16,3,4,22,20,5
16-Nov-24,3,26,31,22,1,3
15-Nov-24,14,5,24,19,12,1
13-Nov-24,30,38,4,34,28,11
12-Nov-24,39,27,30,26,3,6
09-Nov-24,28,15,33,8,22,12
08-Nov-24,29,31,25,3,39,4
06-Nov-24,20,12,19,39,6,11
05-Nov-24,8,11,4,30,10,11
02-Nov-24,11,29,6,31,23,12
01-Nov-24,13,1,35,18,21,8
30-Oct-24,10,15,12,25,20,3
29-Oct-24,8,38,23,12,17,5
26-Oct-24,9,6,32,38,15,7
25-Oct-24,33,30,8,20,2,14
23-Oct-24,19,13,34,38,36,5
22-Oct-24,32,33,14,23,27,5
19-Oct-24,13,2,37,25,26,1
18-Oct-24,27,19,37,31,39,8
16-Oct-24,17,37,24,9,28,5
15-Oct-24,13,1,23,17,36,13
12-Oct-24,10,33,19,12,34,3
11-Oct-24,31,39,29,30,27,8
09-Oct-24,10,1,25,18,3,2
08-Oct-24,19,17,10,27,35,2
05-Oct-24,26,23,22,2,14,4
04-Oct-24,19,25,23,30,39,11
02-Oct-24,21,26,7,15,32,5
01-Oct-24,15,5,17,1,32,9
28-Sep-24,36,22,12,11,9,5
27-Sep-24,16,8,14,3,4,5
25-Sep-24,18,30,33,13,15,7
24-Sep-24,22,10,19,33,13,11
21-Sep-24,21,12,39,3,10,1
20-Sep-24,38,5,16,37,3,9
18-Sep-24,18,29,37,16,27,5
17-Sep-24,30,23,13,32,28,7
14-Sep-24,21,22,14,4,29,9
13-Sep-24,11,32,27,4,10,8
11-Sep-24,32,24,22,10,16,4
10-Sep-24,12,18,24,27,32,7
07-Sep-24,36,35,10,34,32,12
06-Sep-24,29,12,36,10,22,14
04-Sep-24,23,6,30,26,25,7
03-Sep-24,7,24,23,17,28,3
31-Aug-24,19,36,33,11,27,12
30-Aug-24,34,38,31,19,4,13
28-Aug-24,16,4,6,13,28,3
27-Aug-24,3,5,9,34,6,4
24-Aug-24,14,34,16,5,39,10
23-Aug-24,5,11,33,20,6,13
21-Aug-24,2,1,22,17,6,11
20-Aug-24,12,28,37,19,15,10
17-Aug-24,12,10,24,18,3,13
16-Aug-24,29,13,30,33,9,13
14-Aug-24,17,16,11,15,28,10
13-Aug-24,2,9,7,3,24,4
10-Aug-24,12,10,25,21,4,13
09-Aug-24,14,21,36,24,13,2
07-Aug-24,30,15,33,18,3,6
06-Aug-24,38,35,18,22,19,14
03-Aug-24,2,12,11,24,23,7
02-Aug-24,13,27,33,26,38,10
31-Jul-24,28,34,1,19,20,7
30-Jul-24,22,2,19,15,35,3
27-Jul-24,11,18,6,33,38,13
26-Jul-24,3,22,15,2,25,7
24-Jul-24,24,1,3,34,33,5
23-Jul-24,31,9,38,11,33,11
20-Jul-24,13,18,16,12,14,3
19-Jul-24,18,31,13,20,32,11
17-Jul-24,11,39,32,16,14,7
16-Jul-24,21,25,15,20,28,5
"""

# Load data into a dataframe
df = pd.read_csv(pd.compat.StringIO(data))

# Combine all balls into one list
all_numbers = df.iloc[:, 1:-1].values.flatten()

# Count frequency of each number
frequency = Counter(all_numbers)

# Separate into most and least frequent numbers
most_frequent = [num for num, count in frequency.most_common(5)]
least_frequent = [num for num, count in frequency.most_common()[-5:]]

# Combine into a prediction pool
prediction_pool = set(most_frequent + least_frequent)

most_frequent, least_frequent, prediction_pool

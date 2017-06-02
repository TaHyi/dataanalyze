import datetime
import time
file_name = "meeeeXXXXXXe05-31_06-01.csv"
# string1.replace(string2,'')

name_hashtag = file_name[:-15]
file_name1 = file_name.replace(name_hashtag, "")
startday = file_name1[:5]
print(name_hashtag)
print(file_name1)
print(startday)
print(file_name1[6:11])
# print(start_day[-10:]-start_day[-5:])

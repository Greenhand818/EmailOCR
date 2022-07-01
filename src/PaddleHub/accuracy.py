import pymysql

db = pymysql.connect(host='localhost',
                      user='root',
                      password='Xujiachen@123456',
                      database='tryocr1')

cursor = db.cursor()

sql1 = "select count(*) from new_data, new_paddle_rec_result where new_data.newpic_name = new_paddle_rec_result.new_pic_name"
sql2 = "update new_paddle_rec_result set new_email = null where new_email = \"无\""
sql3 = "select count(*) from new_data, new_paddle_rec_result where new_data.newpic_name = new_paddle_rec_result.new_pic_name " \
       "and (new_paddle_rec_result.new_email = new_data.newpic_raw_label)"

cursor.execute(sql1)
count1 = cursor.fetchone()
print(count1[0])

cursor.execute(sql2)
db.commit()

cursor.execute(sql3)
count2 = cursor.fetchone()
print(count2[0])

cursor.close()
db.close()

accuracy = count2[0] / count1[0] * 100
print("%f%%" % accuracy)

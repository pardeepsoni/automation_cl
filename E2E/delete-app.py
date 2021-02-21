from automation_cl.E2E import webapp
import os
import time


#os.remove("data.txt")
app = webapp.WebApp(profile_name='pardeepsoni')

d = {}
with open("//Users/soni/PycharmProjects/LearnPython/AWS/E2E/data.txt") as f:
    for line in f:
        a = line.split(' ')
        key, val = a[0], a[1]
        d[key] = val


app.ec2_instance_delete()
app.delete_asg()
app.delete_launch_template()
app.db_deletion('webappdbinstance')
app.delete_alb(d['alb_arn'].strip('\n'))
print("waiting to delete target group...")
time.sleep(5)
app.delete_tg(d['tg_arn'].strip('\n'))
print("waiting to delete security groups...")
time.sleep(60)
app.delete_sg(d['sg_id3'].strip('\n'))
app.delete_sg(d['sg_id2'].strip('\n'))
app.delete_sg(d['sg_id1'].strip('\n'))


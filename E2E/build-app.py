from AWS.E2E import webapp
import os


os.remove("data.txt")
app = webapp.WebApp(profile_name='pardeepsoni')

sg_id1 = app.create_sg('elb-security-group')
app.attach_sg_inbound_rule_http_rule(sg_id1)
app.write_data_tofile(f"sg_id1 {sg_id1}\n")

sg_id2 = app.create_sg('server-sg')
app.attach_ref_sgrule(sg_id2,'elb-security-group')
app.write_data_tofile(f"sg_id2 {sg_id2}\n")

sg_id3 = app.create_sg('db_server_sg')
app.attach_ref_sgrule(sg_id3,'server-sg')
app.write_data_tofile(f"sg_id3 {sg_id3}\n")

alb_arn = app.create_alb(sg_id1)
app.write_data_tofile(f"alb_arn {alb_arn}\n")

tg_arn = app.create_tg()
app.create_listner(tg_arn,alb_arn)
app.write_data_tofile(f"tg_arn {tg_arn}\n")

lt_id = app.create_launch_template(sg_id1)
app.write_data_tofile(f"lt_id {lt_id}\n")

app.create_asg(tg_arn, lt_id)

app.create_rds_mysql_db(sg_id3)

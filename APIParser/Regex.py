import re

line = "int alarm_schedule_after_delay(app_control_h app_control, int delay, int period, int *alarm_id);"


# matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
matchObj = re.match(r'(.*)(\s)(.*)[(](.*)[)](.*)[;]', line, re.M | re.I)

if matchObj:
   print("matchObj.group() :", matchObj.group())
   print("matchObj.group(1) :", matchObj.group(1))
   print("matchObj.group(2) :", matchObj.group(2))
   print("matchObj.group(3) :", matchObj.group(3))


else:
   print("No match!!")



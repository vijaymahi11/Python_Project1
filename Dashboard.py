@app.route('/chart_user',methods=['POST'])
def chart_user():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print(data)
        str2="SELECT  date_format(date,'%m') as date, Month(date) as Month,( select count(*)  from user_attendance p where status='p' and month(date)=month) as Present,( select count(*)  from user_attendance a where status='a' and month(date)=month) as Absent,(select count(*)  from user_attendance o where status='o' and month(date)=month) as Off from user_attendance c  where date_format(date,'%Y')='2023'group by DATE_FORMAT(date,'%m')"
        str3="select   DATE_FORMAT(date,'%d') AS date,userid ,( select count(*)  from user_attendance p where status='p' and p.date=c.date and p.userid=c.userid ) as Present,( select count(*)  from user_attendance a where status='a' and a.date=c.date  and a.userid=c.userid) as Absent,(select count(*)  from user_attendance o where status='o' and o.date=c.date and o.userid=c.userid) as Off from user_attendance c where DATE_FORMAT(date,'%m')=03 and  DATE_FORMAT(date,'%d')=01"
        
        cur.execute(str2)
        item2 = cur.fetchall()
        conn.commit()
        print(item2)
        days_in_months = (1,12)
       
        a=[]
        size=len(item2)
        print(size)
    for month, num_days in enumerate(days_in_months, start=1):
        x=[*range(num_days)]
        if(month==2):
            for day in x :
                if size != 0 :
                    
                    day2=day+1
                    print(day2)
                    if(day2<10):
                        day2='0'+str(day2)
                        
                    else:
                        day2=day2    
                    arr=[item for item in item2 if item.get('date')== str(day2)]
                    
                    if len(arr) == 0:
                            attendance = {'date':str(day2),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                else :
                    day1=int(day)+1
                    if day1 < 10:
                        day1='0'+str(day1)
                        
                    else:
                        day1=day1
                           
                    if int(day1):
                        attendance = {'date':str(day1),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
                            
                     
                    
    if len(item2) == 0 :                
        item2=a
    print(f'data {item2}')
    # item2.sort(key=attrgetter('date'))
    print(type(item2))
    item2 = sorted(item2, key=lambda x: x['date'])
    
    return jsonify({'data': item2})
@app.route('/date_picker',methods=['POST'])
def datewise_picker():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print(data)
        str2="SELECT COUNT(DISTINCT(userid))as count FROM  emp_register.user_attendance"
        cur.execute(str2)
        item1 = cur.fetchall()
        conn.commit()
        print(item1)
        user_limit = item1[0]['count']
        print(user_limit)
        date_picker=data['date_picker']
        Month=data['Month']
        Pass=data['year_pass']
        str_month= str(Month[0])
        str_year= str(Pass[0])
        int_month=int(str_month)
        int_year=int(str_year)
        select_month=int_month+1
        
        select_strmonth='0'+str(select_month)
        if(date_picker==''):
            str3="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,(select count(*)  from emp_register.user_attendance p where status='p' and  month(date)=month and p.userid=a.userid  ) as Present,( select count(*)  from emp_register.user_attendance v where status='a' and  month(date)=month and v.userid=a.userid) as Absent,(select count(*)  from emp_register.user_attendance o where status='o' and month(date)=month  and o.userid=a.userid) as Off from emp_register.user_attendance   as a left join emp_register.employee_data as b on a.userid = b.id where DATE_FORMAT(date,'%m')='"+select_strmonth+"' group by userid  "
        else:
            date_object = datetime.strptime(date_picker, '%Y-%m-%dT%H:%M:%S.%fZ')
            just_date = date_object.date()
            just_date_string = str(just_date)
            print(just_date_string)
            str3="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,( select count(*)  from emp_register.user_attendance p where status='p' and p.date=a.date and p.userid=a.userid ) as Present,( select count(*)  from emp_register.user_attendance v where status='a' and v.date=a.date  and v.userid=a.userid) as Absent,(select count(*)  from emp_register.user_attendance o where status='o' and o.date=a.date and o.userid=a.userid) as Off from emp_register.user_attendance as a left join emp_register.employee_data as b on a.userid = b.id   where date='"+ just_date_string +"'  "
        str4="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,year(date) as year,( select count(*)  from emp_register.user_attendance p where status='p'  and p.userid=a.userid  ) as Present,( select count(*)  from emp_register.user_attendance v where status='a'  and v.userid=a.userid) as Absent,(select count(*)  from emp_register.user_attendance o where status='o'    and o.userid=a.userid) as Off from emp_register.user_attendance   as a left join emp_register.employee_data as b on a.userid = b.id group by userid"    
        cur.execute(str3)
        item2 = cur.fetchall()
        conn.commit()
        days_in_months = (1,user_limit)
        a=[]
        size=len(item2)
        print(size)
    for month, num_days in enumerate(days_in_months, start=1):
        x=[*range(num_days)]
        if(month==2):
            for day in x :
                
                  if size != 0 :
                    day=day+1  
                    arr=[item for item in item2 if item.get('userid')== (day)]
                    
                    if len(arr) == 0:
                       attendance = {'userid':str(day),'Present':0,'Absent':0,'Off':0,'firstname':str(day)}
                       item2.append(attendance)
                  else :
                    day1=int(day)+1
                    
                           
                    if int(day1):
                        attendance = {'userid':str(day1),'Present':0,'Absent':0,'Off':0,'firstname':str(day1)}
                        a.append(attendance)
               
                            
                            
                     
                    
    if len(item2) == 0 :                
        item2=a
    print(f'data {item2}')
    # item2.sort(key=attrgetter('userid'))
    print(type(item2))
    # item2 = sorted(item2, key=lambda x: x['userid'])
    
    return jsonify({'data': item2})

@app.route('/year_userwise',methods=['POST'])
def yearly_userwise():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print(data)
        str2="SELECT COUNT(DISTINCT(userid))as count FROM  emp_register.user_attendance"
        cur.execute(str2)
        item1 = cur.fetchall()
        conn.commit()
        print(item1)
        user_limit = item1[0]['count']
        print(user_limit)
        str4="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,year(date) as year,( select count(*)  from emp_register.user_attendance p where status='p'  and p.userid=a.userid  ) as Present,( select count(*)  from emp_register.user_attendance v where status='a'  and v.userid=a.userid) as Absent,(select count(*)  from emp_register.user_attendance o where status='o'    and o.userid=a.userid) as Off from emp_register.user_attendance   as a left join emp_register.employee_data as b on a.userid = b.id group by userid"    
        cur.execute(str4)
        item2 = cur.fetchall()
        conn.commit()
        days_in_months = (1,user_limit)
        a=[]
        size=len(item2)
        print(size)
    for month, num_days in enumerate(days_in_months, start=1):
        x=[*range(num_days)]
        if(month==2):
            for day in x :
                
                  if size != 0 :
                    day=day+1  
                    arr=[item for item in item2 if item.get('userid')== (day)]
                    
                    if len(arr) == 0:
                       attendance = {'userid':str(day),'Present':0,'Absent':0,'Off':0,'firstname':str(day)}
                       item2.append(attendance)
                  else :
                    day1=int(day)+1
                    
                           
                    if int(day1):
                        attendance = {'userid':str(day1),'Present':0,'Absent':0,'Off':0,'firstname':str(day1)}
                        a.append(attendance)
               
                            
                            
                     
                    
    if len(item2) == 0 :                
        item2=a
    print(f'data {item2}')
    # item2.sort(key=attrgetter('userid'))
    print(type(item2))
    # item2 = sorted(item2, key=lambda x: x['userid'])
    
    return jsonify({'data': item2})

   
@app.route('/summary', methods=['POST'])
def month():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print(data)
        User = data['User']
        Month=data['Month']
        Pass=data['year_pass']
        print(User)
        str_user= str(User[0])
        str_month= str(Month[0])
        str_year= str(Pass[0])
        int_month=int(str_month)
        int_user=int(str_user)
        int_year=int(str_year)
        select_month=int_month+1
        select_strmonth='0'+str(select_month)
        select_user=int_user
        employee=str(select_user)
        print(select_strmonth)
        year_of_select=str(str_year)
        if(employee=='0'):
            str1 = "SELECT  DATE_FORMAT(date,'%d') AS date,(select count(*) from  user_attendance p where status='p' and p.date=c.date )as Present,(select count(*)  from user_attendance a where status='a' and a.date=c.date ) as Absent,(select count(*)  from user_attendance o where status='o' and o.date=c.date  ) as Off  from user_attendance c  where date_format(date,'%m')='"+select_strmonth+"' and date_format(date,'%Y')='"+year_of_select+"'  group by date"
        else:
            str1= "SELECT  DATE_FORMAT(date,'%d') AS date,userid,(select count(*) from  user_attendance p where status='p' and p.date=c.date and p.userid=c.userid )as Present,(select count(*)  from user_attendance a where status='a' and a.date=c.date and a.userid=c.userid) as Absent,(select count(*)  from user_attendance o where status='o' and o.date=c.date and o.userid=c.userid) as Off  from user_attendance c  where date_format(date,'%m')='"+select_strmonth+"' and date_format(date,'%Y')='"+year_of_select+"' and userid='"+employee+"'  group by date"
    
    
    cur.execute(str1)
    item2 = cur.fetchall()
    conn.commit()
    after_add= select_month
    year1=int_year
    days_in_months = calendar.monthrange(year1,after_add)
    a=[]
    size=len(item2)
    print(item2)
    print(size)
    for month, num_days in enumerate(days_in_months, start=1):
        x=[*range(num_days)]
        print(x)
        if(month==2):
            for day in x :
                
                  if size != 0 :
                    arr=[item for item in item2 if item.get('date')== str(day)]
                    
                    if len(arr) == 0:
                        if day < 10:
                            attendance = {'date':'0'+str(day),'Present':0,'Absent':0,'Off':0}
                        else:   
                            attendance = {'date':str(day),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                  else :
                    day1=int(day)+1
                    if day1 < 10:
                        day1='0'+str(day1)
                        
                    else:
                        day1=day1
                           
                    if int(day1):
                        attendance = {'date':str(day1),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
                            
                     
                    
    if len(item2) == 0 :                
        item2=a
    print(f'data {item2}')
    # item2.sort(key=attrgetter('date'))
    print(type(item2))
    item2 = sorted(item2, key=lambda x: x['date'])
    
    return jsonify({'data': item2})

  
@app.route('/bar_click', methods=['POST'])
def barchart():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print(data)
        User = data['popup_date']
        Month=data['Month']
        Pass=data['year_pass']
        print(User)
        str_user= str(User[0])
        str_month= str(Month[0])
        str_year= str(Pass[0])
        int_month=int(str_month)
        int_user=int(str_user)
        int_year=int(str_year)
        select_month=int_month+1
        select_strmonth='0'+str(select_month)
        select_user=int_user
        employee=str(select_user)
        print(select_strmonth)
        year_of_select=str(str_year)
        str1="SELECT a.id,a.userid,a.status,b.firstname,b.lastname ,Month(date) as Month from user_attendance   as a left join employee_data as b on a.userid = b.id where date_format(date,'%m')='"+select_strmonth+"' and date_format(date,'%d')='"+str(User)+"'  "
        cur.execute(str1)
        item2 = cur.fetchall()
        conn.commit()
        newdict={}
        pre=[]
        absents=[]
        offf=[]
        for i in item2:
           
            if i['status']=='p':
                pre.append(i['firstname'])
            elif i['status']=='a':
                absents.append(i['firstname'])
            else:
                offf.append(i['firstname'])
        newdict={
                'Present':pre,
                'Absent':absents,
                'Off':offf
    
        }     
        print(newdict)
        item2=newdict
       
    
        return jsonify({'data': item2})

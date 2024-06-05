from django.shortcuts import render, redirect, HttpResponse
from app.models import *
from django.db import connection
from django import forms
import os
# Create your views here.

def login(request):
    if 'error_msg' in request.session:
        error_msg = request.session['error_msg']
        del request.session['error_msg']
        return render(request, "login.html", {"error_msg":error_msg, 'title':'用户', 'action':'/userinfo/'})
    else:
        return render(request, "login.html", {'title':'用户', 'action':'/userinfo/'})

sql = "select distinct app_lesson.id as id, lname, teacher, credit, hour, app_major.mname as mname from app_lesson, app_major "+\
        "where app_lesson.major_id = app_major.id and not exists "+\
        "(select lesson_id from app_sl where stu_id = %s and lesson_id = app_lesson.id)"
def user_info(request):
    if request.method == "GET":
        return redirect('/login/')
    if request.POST.get("action") == "retake":
        with connection.cursor() as cursor:
            cursor.execute("select retake_chances from app_stu where id = %s", [request.POST.get("retake_sid")])
            retake_chances = cursor.fetchone()[0]
            cursor.execute("select count(*) from app_sl where stu_id = %s and is_retaking = 1", [request.POST.get("retake_sid")])
            retaking = cursor.fetchone()[0]
            if retake_chances <= retaking:
                msg = "重修机会不足"
            else:
                cursor.execute("update app_sl set is_retaking = 1 where stu_id = %s and lesson_id = %s", [request.POST.get("retake_sid"), request.POST.get("retake_lid")])
                msg = "重修成功"
            sinfo = stu_info.objects.filter(id = request.POST.get("retake_sid")).first()
            ginfo = grade_info.objects.filter(id = request.POST.get("retake_sid"))
            cursor.execute(sql,[request.POST.get("retake_sid")])
            linfo = cursor.fetchall()
            cursor.execute("select * from grade_info where id = %s and grade is not null and is_retaking = 0", [request.POST.get("retake_sid")])
            rinfo = cursor.fetchall()
            return render(request, "user_info.html", {"sinfo":sinfo, "ginfo":ginfo, "linfo":linfo, "rinfo":rinfo, "msg":msg})
    if request.POST.get("action") == "delete":
        with connection.cursor() as cursor:
            cursor.callproc('retake', [request.POST.get("delete_sid"), request.POST.get("delete_lid"), 1, 0])
            cursor.execute("SELECT @state;")
            state = cursor.fetchone()[0]
            sinfo = stu_info.objects.filter(id = request.POST.get("delete_sid")).first()
            ginfo = grade_info.objects.filter(id = request.POST.get("delete_sid"))
            cursor.execute(sql,[request.POST.get("delete_sid")])
            linfo = cursor.fetchall()
            cursor.execute("select * from grade_info where id = %s and grade is not null and is_retaking = 0", [request.POST.get("delete_sid")])
            rinfo = cursor.fetchall()
            if state == 0:
                return render(request, "user_info.html", {"sinfo":sinfo, "ginfo":ginfo, "linfo":linfo, "rinfo":rinfo, "msg":"放弃课程成功"})
            elif state == -1000:
                return render(request, "user_info.html", {"sinfo":sinfo, "ginfo":ginfo, "linfo":linfo, "rinfo":rinfo, "msg":"重修机会不足"})
            else:
                return render(request, "user_info.html", {"sinfo":sinfo, "ginfo":ginfo, "linfo":linfo, "rinfo":rinfo, "msg":"意料之外的错误"})
    if request.POST.get("action") == "select":
        with connection.cursor() as cursor:
            try:
                cursor.execute('insert into app_sl(stu_id, lesson_id, is_retaking, grade) values(%s, %s, 0, null)', [request.POST.get("select_sid"), request.POST.get("select_lid")])
                msg = '选课成功'
            except Exception as e:
                msg = '选课失败'
            sinfo = stu_info.objects.filter(id = request.POST.get("select_sid")).first()
            ginfo = grade_info.objects.filter(id = request.POST.get("select_sid"))
            cursor.execute(sql,[request.POST.get("select_sid")])
            linfo = cursor.fetchall()
            cursor.execute("select * from grade_info where id = %s and grade is not null and is_retaking = 0", [request.POST.get("select_sid")])
            rinfo = cursor.fetchall()
            return render(request, "user_info.html", {"sinfo":sinfo, "ginfo":ginfo, "linfo":linfo, "rinfo":rinfo, "msg":msg})
    id = request.POST.get("id")
    password = request.POST.get("password")
    valid = len(Stu.objects.filter(id = id, password = password))
    if not valid:
        request.session['error_msg']='用户名或密码错误'
        return redirect('/login/')
    sinfo = stu_info.objects.filter(id = id).first()
    ginfo = grade_info.objects.filter(id = id)
    with connection.cursor() as cursor:
        cursor.execute(sql,[id])
        linfo = cursor.fetchall()
        cursor.execute("select * from grade_info where id = %s and grade is not null and is_retaking = 0",[id])
        rinfo = cursor.fetchall()
    return render(request, "user_info.html", {"sinfo":sinfo, "ginfo":ginfo, "linfo":linfo, "rinfo":rinfo})

class editForm(forms.Form):
    old_id_ = forms.CharField(label='旧学号', widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False)
    id_ = forms.CharField(label='学号', max_length=10, min_length=10, 
                         error_messages={"min_length": "id必须为10位", "required": "该字段不能为空!"},
                         widget=forms.TextInput(attrs={'class':'form-control'}))
    password_ = forms.CharField(label='密码', max_length=16, min_length=6, 
                               error_messages={"min_length": "长度必须不能小于6", "max_length": "长度必须不能大于16", "required": "该字段不能为空!"},
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))
    img_ = forms.ImageField(label='照片', max_length=32, required=False, 
                         error_messages={"max_length": "输入太长了"},
                         widget=forms.FileInput(attrs={'class':'form-control'}))
    sname_ = forms.CharField(label='姓名', max_length=32,
                           error_messages={"max_length": "名字太长了", "required": "该字段不能为空!"},
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    gender_ = forms.BooleanField(label='性别', required=False,
                                widget=forms.RadioSelect(choices=((True, "男"), (False, "女"))))
    status_ = forms.IntegerField(label='学业状态', error_messages={"required": "该字段不能为空!"},
                                widget=forms.Select(choices=((0, "学业正常"), (1, "警告"), (2, "已毕业")),attrs={'class':'form-control'}))
    retake_chances_ = forms.IntegerField(label='重修机会', error_messages={"required": "该字段不能为空!"},
                                        widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}))
    birthday_ = forms.DateField(label='生日', error_messages={"required": "该字段不能为空!"},
                               widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    data_in_ = forms.DateField(label='入学时间', error_messages={"required": "该字段不能为空!"},
                              widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    major_id_ = forms.CharField(label='专业', max_length=3, 
                               error_messages={"max_length": "长度必须不能大于3","required": "该字段不能为空!"},
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    prize_ = forms.CharField(label='奖项', max_length=256, required=False,
                            error_messages={"max_length": "输入太长了"},
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    punishment_ = forms.CharField(label='惩罚', max_length=256, required=False,
                                 error_messages={"max_length": "输入太长了"},
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    action_ = forms.CharField(label='操作', max_length=10,
                             widget=forms.TextInput(attrs={'readonly':'readonly'}))
    


def root(request):
    if request.method == 'GET':
        return render(request, "login.html", {'title':'管理员', 'action':'/root/'})
    id = request.POST.get("id")
    password = request.POST.get("password")
    emptyform = editForm()
    if request.POST.get("action") == "delete":
        try:
            info = Stu.objects.filter(id=id).first()
            if info.img.name is not None and len(info.img.name) > 0 and os.path.exists('media/'+info.img.name):
                os.remove('media/'+info.img.name)
            with connection.cursor() as cursor:
                cursor.callproc('delete_stu', [id])
            info = stu_info.objects.all()
            return render(request, 'root.html',{'info':info, 'msg':"删除成功", 'form':emptyform})
        except Exception as e:
            info = stu_info.objects.all()
            return render(request, 'root.html',{'info':info, 'msg':"删除失败", 'form':emptyform})
    form = editForm(request.POST, request.FILES)
    if request.POST.get("action_") == "create":
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                if len(Stu.objects.filter(id=data['id_'])) > 0:
                    info = stu_info.objects.all()
                    return render(request, 'root.html',{'info':info, 'msg':"添加失败请检查输入参数与当前数据是否冲突", 'form':form})
                info = Stu(id=data['id_'], password=data['password_'], sname=data['sname_'], img=data['img_'],
                           gender=data['gender_'], major_id=data['major_id_'], prize=data['prize_'], punishment=data['punishment_'],
                            status=data['status_'], retake_chances=data['retake_chances_'], birthday=data['birthday_'], data_in=data['data_in_'])
                info.save()
                info = stu_info.objects.all()
                return render(request, 'root.html',{'info':info, 'msg':"添加成功", 'form':form})
            except Exception as e:
                info = stu_info.objects.all()
                return render(request, 'root.html',{'info':info, 'msg':"编辑失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = stu_info.objects.all()
        return render(request, 'root.html',{'info':info, 'msg':"添加失败请检查输入参数", 'form':form})
    if request.POST.get("action_") == "edit":
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                info = Stu.objects.filter(id=data['old_id_']).first()
                if info.img.name is not None and len(info.img.name) > 0 and os.path.exists('media/'+info.img.name):
                    os.remove('media/'+info.img.name)
                for key in data:
                    if key != 'old_id_' and key != 'action_' and key != 'id_':
                        info.__dict__[key[0:-1]] = data[key]
                info.__dict__['img'] = data['img_']
                info.save()
                with connection.cursor() as cursor:
                    cursor.callproc('edit_stu_id', [data['old_id_'], data['id_']])
                info = stu_info.objects.all()
                return render(request, 'root.html',{'info':info, 'msg':"编辑成功", 'form':form})
            except Exception as e:
                info = stu_info.objects.all()
                return render(request, 'root.html',{'info':info, 'msg':"编辑失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = stu_info.objects.all()
        return render(request, 'root.html',{'info':info, 'msg':"编辑失败请检查输入参数", 'form':form})
    if(id == "root" and password == "123456"):
        info = stu_info.objects.all()
        return render(request, 'root.html',{'info':info, 'form':emptyform})
    else:
        return render(request, "login.html", {'title':'管理员', 'action':'/root/', 'error_msg':'用户名或密码错误'})


class lesform(forms.Form):
    old_id = forms.CharField(label='旧课程编号', widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False)
    id = forms.CharField(label='课程编号', max_length=10,
                         error_messages={"max_length": "id不能超过10位", "required": "该字段不能为空!"},
                         widget=forms.TextInput(attrs={'class':'form-control'}))
    lname = forms.CharField(label='课程名称', max_length=64,
                           error_messages={"max_length": "名字太长了", "required": "该字段不能为空!"},
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    teacher = forms.CharField(label='教师', max_length=64,
                             error_messages={"max_length": "名字太长了", "required": "该字段不能为空!"},
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    credit = forms.IntegerField(label='学分', error_messages={"required": "该字段不能为空!"},
                              widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}))
    major_id = forms.CharField(label='专业', max_length=3,
                             error_messages={"max_length": "长度不能超过3", "required": "该字段不能为空!"},
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    hour = forms.IntegerField(label='学时', error_messages={"required": "该字段不能为空!"},
                            widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}))
    action = forms.CharField(label='操作', max_length=10,
                             widget=forms.TextInput(attrs={'readonly':'readonly'}))
    
    
def les(request):
    if request.method == "GET":
        return redirect('/root/')
    emptyform = lesform()
    if request.POST.get("action") == "delete":
        try:
            with connection.cursor() as cursor:
                cursor.callproc('delete_les', [request.POST.get("id")])
            info = les_info.objects.all()
            return render(request, 'lesson.html', {'info':info, 'msg':"删除成功", 'form':emptyform})
        except:
            return HttpResponse("删除失败")
    if request.POST.get("action") == "create":
        form = lesform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                if len(lesson.objects.filter(id=data['id'])) > 0:
                    info = les_info.objects.all()
                    return render(request, 'lesson.html',{'info':info, 'msg':"添加失败请检查输入参数与当前数据是否冲突", 'form':form})
                info = lesson(id=data['id'], lname=data['lname'], teacher=data['teacher'], credit=data['credit'], major_id=data['major_id'], hour=data['hour'])
                info.save()
                info = les_info.objects.all()
                return render(request, 'lesson.html',{'info':info, 'msg':"添加成功", 'form':form})
            except Exception as e:
                info = les_info.objects.all()
                return render(request, 'lesson.html',{'info':info, 'msg':"添加失败请检查输入参数", 'form':form})
        info = les_info.objects.all()
        return render(request, 'lesson.html',{'info':info, 'msg':"添加失败请检查输入参数", 'form':form})
    if request.POST.get("action") == "edit":
        form = lesform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                info = lesson.objects.filter(id=data['old_id']).first()
                for key in data:
                    if key != 'id' and key != 'action' and key != 'old_id':
                        info.__dict__[key] = data[key]
                info.save()
                with connection.cursor() as cursor:
                    cursor.callproc('edit_les_id', [data['old_id'], data['id']])
                info = les_info.objects.all()
                return render(request, 'lesson.html',{'info':info, 'msg':"编辑成功", 'form':form})
            except Exception as e:
                info = les_info.objects.all()
                return render(request, 'lesson.html',{'info':info, 'msg':"编辑失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = les_info.objects.all()
        return render(request, 'lesson.html',{'info':info, 'msg':"编辑失败请检查输入参数", 'form':form})
    if request.POST.get('id') == "root" and request.POST.get('password') == "123456":
        info = les_info.objects.all()
        return render(request, 'lesson.html', {'info':info, 'form':emptyform})
    else:
        return render(request, "login.html", {'title':'管理员', 'action':'/root/', 'error_msg':'用户名或密码错误'})
    
    
class slform(forms.Form):
    sid = forms.CharField(label='学号', max_length=10,
                         error_messages={"max_length": "id不能超过10位", "required": "该字段不能为空!"})
    lid = forms.CharField(label='课程编号', max_length=10,
                            error_messages={"max_length": "id不能超过10位", "required": "该字段不能为空!"})
    is_retaking = forms.BooleanField(label='是否正在重修', required=False,
                                    widget=forms.RadioSelect(choices=((True, "是"), (False, "否"))))
    grade = forms.IntegerField(label='成绩', required=False,
                             widget=forms.NumberInput(attrs={'type':'number','class':'form-control'}))
    action = forms.CharField(label='操作', max_length=10,
                             widget=forms.TextInput(attrs={'readonly':'readonly'}))    

def stules(request):
    if request.method == "GET":
        return redirect('/root/')
    emptyform = slform()
    if request.POST.get("action") == "delete":
        try:
            with connection.cursor() as cursor:
                cursor.callproc('retake', [request.POST.get("sid"), request.POST.get("lid"), 1, 0])
                cursor.execute("SELECT @state;")
                state = cursor.fetchone()[0]
                info = sl_info.objects.all()
                if state == 0:
                    return render(request, 'stules.html', {'info':info, 'msg':"删除成功", 'form':emptyform})
                elif state == -1000:
                    return render(request, 'stules.html', {'info':info, 'msg':"重修机会不足", 'form':emptyform})
                else:
                    return render(request, 'stules.html', {'info':info, 'msg':"意料之外的错误", 'form':emptyform})
        except:
            info = sl_info.objects.all()
            return render(request, 'stules.html', {'info':info, 'msg':"删除失败", 'form':emptyform})
    if request.POST.get("action") == "create":
        form = slform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                with connection.cursor() as cursor:
                    cursor.execute("insert into app_sl(stu_id, lesson_id, is_retaking, grade) values(%s, %s, %s, %s)", [data['sid'], data['lid'], data['is_retaking'], data['grade']])
                info = sl_info.objects.all()
                return render(request, 'stules.html',{'info':info, 'msg':"添加成功", 'form':form})
            except Exception as e:
                info = sl_info.objects.all()
                return render(request, 'stules.html',{'info':info, 'msg':"添加失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = sl_info.objects.all()
        return render(request, 'stules.html',{'info':info, 'msg':"添加失败请检查输入参数", 'form':form})
    if request.POST.get("action") == "edit":
        form = slform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                info = sl.objects.filter(stu=request.POST.get('sid'), lesson=request.POST.get('lid')).first()
                info.__dict__['is_retaking'] = data['is_retaking']
                info.save()
                with connection.cursor() as cursor:
                    if(info.__dict__['grade'] is not None):
                        cursor.callproc('retake', [data['sid'], data['lid'], 0, data['grade']])
                        cursor.execute("SELECT @state;")
                        state = cursor.fetchone()[0]
                        info = sl_info.objects.all()
                        if state == 0:
                            return render(request, 'stules.html',{'info':info, 'msg':"编辑成功", 'form':form})
                        elif state == -1000:
                            return render(request, 'stules.html',{'info':info, 'msg':"重修机会不足", 'form':form})
                        else:
                            return render(request, 'stules.html',{'info':info, 'msg':"意料之外的错误", 'form':form})
                    else:
                        cursor.execute("update app_sl set grade = %s where stu_id = %s and lesson_id = %s", [data['grade'], data['sid'], data['lid']])
                        info = sl_info.objects.all()
                        return render(request, 'stules.html',{'info':info, 'msg':"编辑成功", 'form':form})
            except Exception as e:
                info = sl_info.objects.all()
                return render(request, 'stules.html',{'info':info, 'msg':"编辑失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = sl_info.objects.all()
        return render(request, 'stules.html',{'info':info, 'msg':"编辑失败请检查输入参数", 'form':form})
    if request.POST.get('id') == "root" and request.POST.get('password') == "123456":
        info = sl_info.objects.all()
        return render(request, 'stules.html', {'info':info, 'form':emptyform})
    else:
        return render(request, "login.html", {'title':'管理员', 'action':'/root/', 'error_msg':'用户名或密码错误'})

class majorform(forms.Form):
    old_id = forms.CharField(label='旧专业编号', widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False)
    id = forms.CharField(label='专业编号', max_length=3,
                         error_messages={"max_length": "id不能超过3位", "required": "该字段不能为空!"},
                         widget=forms.TextInput(attrs={'class':'form-control'}))
    mname = forms.CharField(label='专业名称', max_length=64,
                           error_messages={"max_length": "名字太长了", "required": "该字段不能为空!"},
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    did = forms.IntegerField(label='学院编号', error_messages={"required": "该字段不能为空!"},
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    action = forms.CharField(label='操作', max_length=10,
                             widget=forms.TextInput(attrs={'readonly':'readonly'}))


def mjr(request):
    if request.method == "GET":
        return redirect('/root/')
    if request.POST.get("action") == "delete":
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from app_stu where major_id = %s", [request.POST.get("id")])
                sinfo = cursor.fetchall()
                for s in sinfo:
                    if s[3] is not None and len(s[3]) > 0 and os.path.exists('media/'+s[3]):
                        os.remove('media/'+s[3])
                cursor.callproc('delete_major', [request.POST.get("id")])
            info = major.objects.all()
            return render(request, 'major.html', {'info':info, 'msg':"删除成功", 'form':majorform()})
        except Exception as e:
            info = major.objects.all()
            return render(request, 'major.html', {'info':info, 'msg':"删除失败", 'form':majorform()})
    if request.POST.get('action') == 'create':
        form = majorform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                with connection.cursor() as cursor:
                    cursor.execute("insert into app_major(id, mname, department_id) values(%s, %s, %s)", [data['id'], data['mname'], data['did']])
                info = major.objects.all()
                return render(request, 'major.html',{'info':info, 'msg':"添加成功", 'form':form})
            except Exception as e:
                info = major.objects.all()
                return render(request, 'major.html',{'info':info, 'msg':"添加失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = major.objects.all()
        return render(request, 'major.html',{'info':info, 'msg':"添加失败请检查输入参数", 'form':form})
    if request.POST.get('action') == 'edit':
        form = majorform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                info = major.objects.filter(id=data['old_id']).first()
                info.__dict__['mname'] = data['mname']
                info.__dict__['did'] = data['did']
                info.save()
                with connection.cursor() as cursor:
                    cursor.callproc('edit_major_id', [data['old_id'], data['id']])
                info = major.objects.all()
                return render(request, 'major.html',{'info':info, 'msg':"编辑成功", 'form':form})
            except Exception as e:
                info = major.objects.all()
                return render(request, 'major.html',{'info':info, 'msg':"编辑失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = major.objects.all()
        return render(request, 'major.html',{'info':info, 'msg':"编辑失败请检查输入参数", 'form':form})
    id = request.POST.get('id')
    password = request.POST.get('password')
    if id == "root" and password == "123456":
        info = major.objects.all()
        return render(request, 'major.html', {'info':info, 'form':majorform()})
    else:
        return render(request, "login.html", {'title':'管理员', 'action':'/root/', 'error_msg':'用户名或密码错误'})
    
    
class depform(forms.Form):
    old_id = forms.CharField(label='旧学院编号', widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False)
    id = forms.CharField(label='学院编号', max_length=3,
                         error_messages={"max_length": "id不能超过3位", "required": "该字段不能为空!"},
                         widget=forms.TextInput(attrs={'class':'form-control'}))
    dname = forms.CharField(label='学院名称', max_length=64,
                           error_messages={"max_length": "名字太长了", "required": "该字段不能为空!"},
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    action = forms.CharField(label='操作', max_length=10,
                             widget=forms.TextInput(attrs={'readonly':'readonly'}))

def dep(request):
    if request.method == "GET":
        return redirect('/root/')
    if request.POST.get('action') == 'delete':
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from app_major where department_id = %s", [request.POST.get("id")])
                minfo = cursor.fetchall()
                for m in minfo:
                    cursor.execute("select * from app_stu where major_id = %s", [m[0]])
                    sinfo = cursor.fetchall()
                    for s in sinfo:
                        if s[3] is not None and len(s[3]) > 0 and os.path.exists('media/'+s[3]):
                            os.remove('media/'+s[3])
                cursor.callproc('delete_dep', [request.POST.get("id")])
            info = department.objects.all()
            return render(request, 'department.html', {'info':info, 'msg':"删除成功", 'form':depform()})
        except Exception as e:
            info = department.objects.all()
            return render(request, 'department.html', {'info':info, 'msg':"删除失败", 'form':depform()})
    if request.POST.get('action') == 'create':
        form = depform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                with connection.cursor() as cursor:
                    cursor.execute("insert into app_department(id, dname) values(%s, %s)", [data['id'], data['dname']])
                info = department.objects.all()
                return render(request, 'department.html',{'info':info, 'msg':"添加成功", 'form':form})
            except Exception as e:
                info = department.objects.all()
                return render(request, 'department.html',{'info':info, 'msg':"添加失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = department.objects.all()
        return render(request, 'department.html',{'info':info, 'msg':"添加失败请检查输入参数", 'form':form})
    if request.POST.get('action') == 'edit':
        form = depform(data=request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data
                data = cleaned_data
                info = department.objects.filter(id=data['old_id']).first()
                info.__dict__['dname'] = data['dname']
                info.save()
                with connection.cursor() as cursor:
                    cursor.callproc('edit_dep_id', [data['old_id'], data['id']])
                info = department.objects.all()
                return render(request, 'department.html',{'info':info, 'msg':"编辑成功", 'form':form})
            except Exception as e:
                info = department.objects.all()
                return render(request, 'department.html',{'info':info, 'msg':"编辑失败请检查输入参数与当前数据是否冲突", 'form':form})
        info = department.objects.all()
        return render(request, 'department.html',{'info':info, 'msg':"编辑失败请检查输入参数", 'form':form})
    id = request.POST.get('id')
    password = request.POST.get('password')
    if id == "root" and password == "123456":
        info = department.objects.all()
        return render(request, 'department.html', {'info':info, 'form':depform()})
    else:
        return render(request, "login.html", {'title':'管理员', 'action':'/root/', 'error_msg':'用户名或密码错误'})
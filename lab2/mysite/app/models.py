from django.db import models

# Create your models here.

class department(models.Model):
    id = models.CharField(verbose_name='学院编号',max_length=3, primary_key=True)
    dname = models.CharField(verbose_name='学院',max_length=64, null=False, unique=True)

class major(models.Model):
    id = models.CharField(verbose_name='专业编号',max_length=3, primary_key=True)
    mname = models.CharField(verbose_name='专业',max_length=64, null=False, unique=True)
    department = models.ForeignKey(to="department", to_field="id", on_delete=models.DO_NOTHING)

class Stu(models.Model):
    id = models.CharField(verbose_name='学号',max_length=10, primary_key=True)
    password = models.CharField(verbose_name='密码',max_length=16, null=False)
    sname = models.CharField(verbose_name='姓名',max_length=32, null=False)
    img = models.ImageField(verbose_name='头像',max_length=32, null=True, upload_to='photos')
    gender_choices = (
        (True, "男"),
        (False, "女"),
    )
    gender = models.BooleanField(verbose_name='性别',default=True, choices=gender_choices)
    major = models.ForeignKey(to="major", to_field="id", on_delete=models.DO_NOTHING)
    prize = models.CharField(verbose_name='奖项',max_length=256, null=True, default='')
    punishment = models.CharField(verbose_name='惩罚',max_length=256, null=True,default='')
    status_choices = (
        (0, "学业正常"),
        (1, "警告"),
        (2, "已毕业"),
    )
    status = models.SmallIntegerField(verbose_name='学业状态',default=0, choices=status_choices, null=False)
    retake_chances = models.SmallIntegerField(verbose_name='重修机会',default=2, null=False)
    birthday = models.DateField(verbose_name='生日',null=False)
    data_in = models.DateField(verbose_name='入学时间',null=False)

class lesson(models.Model):
    id = models.CharField(verbose_name='课程编号',max_length=10, primary_key=True)
    lname = models.CharField(verbose_name='课程名称',max_length=64, null=False)
    teacher = models.CharField(verbose_name='教师',max_length=64, null=False)
    credit = models.SmallIntegerField(verbose_name='学分',null=False)
    major = models.ForeignKey(to="major", to_field="id", on_delete=models.DO_NOTHING) 
    hour = models.SmallIntegerField(verbose_name='学时',null=False)  
    
class sl(models.Model):
    stu = models.ForeignKey(to="Stu", to_field="id", on_delete=models.DO_NOTHING)
    lesson = models.ForeignKey(to="lesson", to_field="id", on_delete=models.DO_NOTHING)
    is_retaking = models.BooleanField(verbose_name='是否正在重修',default=False, null = False)
    grade = models.SmallIntegerField(verbose_name='成绩',null=True)
    class Meta:
        unique_together=("stu","lesson")
        

class stu_info(models.Model):
    id = models.CharField(verbose_name='学号',max_length=10, primary_key=True)
    password = models.CharField(verbose_name='密码',max_length=16, null=False)
    img = models.ImageField(verbose_name='照片',max_length=32, null=True, upload_to='photos')
    name = models.CharField(verbose_name='姓名',max_length=32, null=False)
    gender = models.BooleanField(verbose_name='性别',default=True)
    prize = models.CharField(verbose_name='奖项',max_length=256, null=True)
    punishment = models.CharField(verbose_name='惩罚',max_length=256, null=True)
    status = models.SmallIntegerField(verbose_name='学业状态',default=0, null=False)
    retake_chances = models.SmallIntegerField(verbose_name='重修机会',default=2, null=False)
    birthday = models.DateField(verbose_name='生日',null=False)
    data_in = models.DateField(verbose_name='入学时间',null=False)
    major = models.CharField(verbose_name='专业',max_length=64, null=False)
    department = models.CharField(verbose_name='学院',max_length=64, null=False)
    avg_gpa = models.FloatField(verbose_name='绩点',null=True)
    class Meta:
        managed = False
        db_table = 'stu_info'
        verbose_name = '学生信息'
        
class grade_info(models.Model):
    id = models.CharField(verbose_name='学号',max_length=10, primary_key=True)
    sname = models.CharField(verbose_name='姓名',max_length=32, null=False)
    lid = models.CharField(verbose_name='课程编号',max_length=10)
    lname = models.CharField(verbose_name='课程名称',max_length=64, null=False)
    grade = models.SmallIntegerField(verbose_name='成绩',null=True)
    is_retaking = models.BooleanField(verbose_name='是否正在重修',default=False, null = False)
    class Meta:
        managed = False
        db_table = 'grade_info'
        verbose_name = '成绩信息'
        
class les_info(models.Model):
    id = models.CharField(verbose_name='课程编号',max_length=10, primary_key=True)
    lname = models.CharField(verbose_name='课程名称',max_length=64, null=False)
    teacher = models.CharField(verbose_name='教师',max_length=64, null=False)
    credit = models.SmallIntegerField(verbose_name='学分',null=False)
    hour = models.SmallIntegerField(verbose_name='学时',null=False)
    mname = models.CharField(verbose_name='专业',max_length=64, null=False)
    dname = models.CharField(verbose_name='学院',max_length=64, null=False)
    class Meta:
        managed = False
        db_table = 'les_info'
        verbose_name = '课程信息'
        
class sl_info(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    sid = models.CharField(verbose_name='学号',max_length=10)
    sname = models.CharField(verbose_name='姓名',max_length=32, null=False)
    lid = models.CharField(verbose_name='课程编号',max_length=10)
    lname = models.CharField(verbose_name='课程名称',max_length=64, null=False)
    teacher = models.CharField(verbose_name='教师',max_length=64, null=False)
    credit = models.SmallIntegerField(verbose_name='学分',null=False)
    hour = models.SmallIntegerField(verbose_name='学时',null=False)
    is_retaking = models.BooleanField(verbose_name='是否正在重修',default=False, null = False)
    grade = models.SmallIntegerField(verbose_name='成绩',null=True)
    class Meta:
        managed = False
        db_table = 'sl_info'
        verbose_name = '选课信息'
# Generated by Django 4.2.13 on 2024-05-23 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="department",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=3,
                        primary_key=True,
                        serialize=False,
                        verbose_name="学院编号",
                    ),
                ),
                (
                    "dname",
                    models.CharField(max_length=64, unique=True, verbose_name="学院"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="major",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=3,
                        primary_key=True,
                        serialize=False,
                        verbose_name="专业编号",
                    ),
                ),
                (
                    "mname",
                    models.CharField(max_length=64, unique=True, verbose_name="专业"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="app.department",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Stu",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=10,
                        primary_key=True,
                        serialize=False,
                        verbose_name="学号",
                    ),
                ),
                ("password", models.CharField(max_length=16, verbose_name="密码")),
                ("sname", models.CharField(max_length=32, verbose_name="姓名")),
                ("img", models.CharField(max_length=32, null=True, verbose_name="头像")),
                (
                    "gender",
                    models.BooleanField(
                        choices=[(True, "男"), (False, "女")],
                        default=True,
                        verbose_name="性别",
                    ),
                ),
                (
                    "prize",
                    models.CharField(max_length=256, null=True, verbose_name="奖项"),
                ),
                (
                    "punishment",
                    models.CharField(max_length=256, null=True, verbose_name="惩罚"),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(0, "学业正常"), (1, "警告"), (2, "已毕业")],
                        default=0,
                        verbose_name="学业状态",
                    ),
                ),
                (
                    "retake_chances",
                    models.SmallIntegerField(default=2, verbose_name="重修机会"),
                ),
                ("birthday", models.DateField(verbose_name="生日")),
                ("data_in", models.DateField(verbose_name="入学时间")),
                (
                    "major",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.major"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="lesson",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=10,
                        primary_key=True,
                        serialize=False,
                        verbose_name="课程编号",
                    ),
                ),
                ("lname", models.CharField(max_length=64, verbose_name="课程名称")),
                ("teacher", models.CharField(max_length=64, verbose_name="教师")),
                ("credit", models.SmallIntegerField(verbose_name="学分")),
                ("hour", models.SmallIntegerField(verbose_name="学时")),
                (
                    "major",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.major"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="sl",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_retaking",
                    models.BooleanField(default=False, verbose_name="是否正在重修"),
                ),
                ("grade", models.SmallIntegerField(null=True, verbose_name="成绩")),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.lesson"
                    ),
                ),
                (
                    "stu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.stu"
                    ),
                ),
            ],
            options={
                "unique_together": {("stu", "lesson")},
            },
        ),
    ]

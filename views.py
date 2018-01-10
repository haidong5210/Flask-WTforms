from flask import Flask,render_template,request,Blueprint
from wtforms import Form,widgets,validators
from wtforms.fields import simple
from .pool import POOL
_login = Blueprint('login',__name__)
import wtforms

#WTform解析
class Login(Form):
    #第一步执行
    #name = UnboundField()  creation_counter=1 根据他排序
    name = simple.StringField(

        label='用户名',
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message='内容不能为空！'),
            validators.length(min=3,max=10,message='密码最短%(min)d最长%(max)d')
        ],
        render_kw={'class':'form-control'}
    )
    # password = UnboundField()  creation_counter=2 根据他排序
    password = simple.PasswordField(
        label='密码',
        widget=widgets.PasswordInput(),
        validators=[
            validators.DataRequired(message='内容不能为空'),
            #自定义规则，写一个类  类名(message='asdhkasdhkad')
        ]
        )

    class Meta:
        pass




@_login.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        #第二部实例化
        #执行type的__call__方法

        #执行自己或基类的__new__方法
        #执行自己或基类的__init__方法
        form = Login()
        '''
        为什么form.name对应的是StringField()返回的确实标签字符串呢？我们要看StringField()！！
        Login(formdata=request.form)的值是如何在获取的呢？答案在：在执行自己或基类的__init__方法的最后
        
        '''


        return render_template('login.html',form=form)
    else:
        form=Login(formdata=request.form)
        # formdata=request.form的值是如何在获取的呢？
        # 在执行自己或基类的__init__方法的最后
        if form.validate():
            conn = POOL.connection()
            cursor = conn.cursor()
            sql = 'select * from userinfo where name=%s and password=%s;'
            name = form.name.data
            pwd = form.password.data
            rows = cursor.execute(sql, [name, pwd])
            conn.close()
            if rows:
                return '登陆成功！'
            else:
                return '登陆失败'
        else:
            return render_template('login.html', form=form)

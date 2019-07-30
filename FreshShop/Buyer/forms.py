from django import forms
# 买家
class BuyerForm(forms.Form):
    username = forms.CharField(max_length=20,label='用户名')
    password = forms.CharField(max_length=20,label='密码')
    email = forms.EmailField(label='邮箱')






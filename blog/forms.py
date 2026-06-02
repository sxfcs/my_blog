from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Topic, Reply


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'article']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入主题标题'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '请输入主题内容（支持Markdown）'}),
            'article': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '主题标题',
            'content': '内容',
            'article': '关联文章（可选）',
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '请输入回复内容'}),
        }
        labels = {
            'content': '回复内容',
        }


# ========== 新增：用户注册表单 ==========

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为字段添加CSS样式
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': '请输入用户名'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': '请输入密码'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': '请再次输入密码'
        })
        
        # 设置帮助文本
        self.fields['username'].help_text = '必填。150个字符或更少。字母、数字和@/./+/-/_'
        self.fields['password1'].help_text = '密码不能太简单，至少8位，不能全是数字'
        self.fields['password2'].help_text = '请输入相同的密码'
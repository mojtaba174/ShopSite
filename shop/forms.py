from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """فرم کامنت برای ثبت نظر و امتیاز"""

    class Meta:
        model = Comment
        fields = ['content', 'rating']
        labels = {
            'content': 'متن نظر',
            'rating': 'امتیاز (1 تا 5)',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...'
            }),
            'rating': forms.Select(attrs={'class': 'form-control'}, choices=[(i, f"{i} ⭐️") for i in range(1, 6)])
        }

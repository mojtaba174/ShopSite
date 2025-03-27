from .models import DigitCategory  # یا هر نامی که برای مدل دسته‌بندی‌ها داری

def categories_context(request):
    digit_categories = DigitCategory.objects.all()  # همه دسته‌بندی‌ها رو بگیر
    return {'digit_categories': digit_categories}
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

## 这是蓑鲉公司的股价数据模型
class StockPrice(models.Model):
    date = models.DateField(verbose_name="Date")
    company_code = models.CharField(max_length=16, verbose_name="Company Code")
    company_name = models.CharField(max_length=32, verbose_name="Company Name")
    stock_price = models.FloatField(verbose_name="Stock Price")

    class Meta:
        verbose_name = "Stock Price Record"
        verbose_name_plural = "Stock Price Records"
        ordering = ['company_code', '-date'] 
        unique_together = [['date', 'company_code']]  

    def __str__(self):
        return f"{self.date} - {self.company_code} ({self.stock_price})"
    

class CustomUserManager(BaseUserManager):
    """自定义用户管理器"""
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('必须提供电子邮箱'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)
    
class User(AbstractUser):
    """扩展的用户模型"""
    email = models.EmailField(_('电子邮箱'), unique=True)
    profile_image = models.ImageField(
        _('用户头像'),
        upload_to='user_profiles/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    email_verified = models.BooleanField(_('邮箱验证'), default=False)

    objects = CustomUserManager()

    # 使用邮箱作为主要标识字段
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __str__(self):
        return self.username








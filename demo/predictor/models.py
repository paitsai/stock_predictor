from django.db import models

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
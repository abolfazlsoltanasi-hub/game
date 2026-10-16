# 🎯 حدس کلمه | Word Guess

نسخهٔ اندرویدی بازی فارسی اصلی که در فایل HTML ارائه شده بود.

## پروژه چگونه کار می‌کند؟

- `assets/game.html` فایل اصلی بازی است و کد HTML، CSS و JavaScript آن حفظ شده است.
- `main.py` پوستهٔ برنامه با **Flet** است که فایل محلی بازی را در WebView اندروید نمایش می‌دهد.
- این روش جایگزین‌کردن بازی با یک بازی دیگر نیست و منطق اصلی، رابط فارسی، بانک کلمه‌ها و رفتارهای تعریف‌شده در HTML را نگه می‌دارد.
- بازی از بانک واژهٔ داخلی برای اجرای آفلاین استفاده می‌کند. ویژگی‌های Gemini و فونت آنلاین، در صورت استفاده، به اینترنت نیاز دارند.

## امکانات موجود در بازی اصلی

- بازی گروهی یا انفرادی با بازیکن‌های انسانی و هوش مصنوعی
- انتخاب موضوع و واژه از بانک کلمات فارسی
- حدس حرف یا کل کلمه، زمان‌سنج و محدودیت خطا
- سیستم امتیاز، سررسید نوبت‌ها، نتایج، تاریخچه و جدول امتیازات
- راهنمایی‌های امتیازدار، صدا و بازخورد لرزشی در دستگاه‌های پشتیبانی‌شده
- ذخیرهٔ تنظیمات و بازی در حال اجرا با `localStorage`
- حالت آفلاین و امکان تنظیم کلید API برای قابلیت اختیاری Gemini

## اجرای محلی

Python 3.10 یا جدیدتر نصب کن:

```bash
python -m venv .venv
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

کنترل WebView برای macOS و Android پشتیبانی می‌شود؛ اجرای اپ دسکتاپ Windows/Linux با همین پوستهٔ WebView پشتیبانی نمی‌شود.

## ساخت APK اندروید

برای ساخت محلی، ابزارهای مورد نیاز Flet/Flutter و Android SDK لازم‌اند:

```bash
python -m pip install -r requirements.txt
flet build apk
```

### ساخت خودکار در GitHub

فایل `.github/workflows/android-apk.yml` در هر push به شاخهٔ `main` و نیز با اجرای دستی، APK را با GitHub Actions می‌سازد.

1. وارد [Actions](https://github.com/abolfazlsoltanasi-hub/game/actions) شو.
2. اجرای **Build Android APK** را باز کن.
3. پس از موفقیت، artifact با نام `word-guess-android-apk` را از قسمت **Artifacts** دریافت کن.
4. اگر artifact به صورت آرشیو دانلود شد، آن را استخراج کن و فایل APK را روی گوشی اندروید نصب کن.

وضعیت واقعی ساخت و خروجی قابل دانلود فقط پس از پایان موفق اجرای GitHub Actions مشخص است.

## ساختار

```text
.
├── main.py
├── pyproject.toml
├── requirements.txt
├── assets/
│   └── game.html
└── .github/
    └── workflows/
        └── android-apk.yml
```

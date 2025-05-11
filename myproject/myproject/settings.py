
from pathlib import Path
import environ


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-#-#48toth^dzsinxh7j#$08wzwk3wt^lbd%+cftjgy4b26n6oy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # เพิ่ม Google provider
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],  # ค้นหาจากโฟลเดอร์ templates ของโปรเจกต์หลัก
        'APP_DIRS': True,  # ให้ค้นหาจากโฟลเดอร์ templates ของแอปด้วย
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'th'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'

# บอก Django ให้สแกนโฟลเดอร์ <project_root>/static/
# (เช่นเก็บ logo.png, custom.css, custom.js)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


MEDIA_URL = '/media/'

# เก็บไฟล์จริงบนดิสก์ที่ <project_root>/media/
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # ใช้ ModelBackend สำหรับการยืนยันตัวตนปกติ
    "allauth.account.auth_backends.AuthenticationBackend",  # ใช้ Allauth สำหรับระบบล็อกอิน
)

SITE_ID = 1

ACCOUNT_SIGNUP_ENABLED = True  # เปิดให้ผู้ใช้สามารถลงทะเบียนได้
ACCOUNT_EMAIL_REQUIRED = True  # ผู้ใช้ต้องกรอกอีเมล
ACCOUNT_AUTHENTICATION_METHOD = "email"  # ใช้อีเมลสำหรับการยืนยันตัวตน
ACCOUNT_USERNAME_REQUIRED = False  # ไม่ต้องกรอกชื่อผู้ใช้ (ให้ใช้แค่ Email)
SOCIALACCOUNT_AUTO_SIGNUP = True  # อนุญาตให้ลงทะเบียนอัตโนมัติเมื่อใช้การเข้าสู่ระบบด้วยโซเชียล
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # ไม่ต้องมีการยืนยันอีเมล (กรณีการเข้าสู่ระบบด้วย Google)
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_SIGNUP = True
LOGIN_URL = "/accounts/login/"  # หน้า login เมื่อยังไม่ล็อกอิน
LOGIN_REDIRECT_URL = "/peddlecamp/"  # หลังล็อกอินจะไปที่หน้า peddlecamp
ACCOUNT_LOGOUT_REDIRECT_URL = "/peddlecamp/"  # หลังออกจากระบบจะไปที่หน้า peddlecamp
ACCOUNT_SIGNUP_REDIRECT_URL = "/accounts/login/"

# Google OAuth settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": env('GOOGLE_CLIENT_ID'),  # ต้องระบุ
            "secret":  env('GOOGLE_CLIENT_SECRET'), # ต้องระบุ
            "key": "",
        },
    }
}
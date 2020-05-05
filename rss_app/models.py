from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    ・
    ・持ってるフィールドをいくつかけしたり、大きな変更が必要な場合はAbstractBaseUserを継承
    usernameフィールドをなくし、emailフィールドをメインに扱うモデルを作成する
    """

    # email field
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    
    # 必要？
    ## first_name = models.CharField(_('first name'), max_length=30, blank=True)
    ## last_name = models.CharField(_('last name'), max_length=150, blank=True)

    # userがadminサイトにサクセスできるかどうかを指定
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    # Trueが推奨
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email

class Feed(models.Model):
    user_id = models.IntegerField()
    feed_url = models.URLField()
    feed_url_str = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.feed_url

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_article_title = models.CharField(max_length=100)
    favorite_article_url = models.URLField()

    def __str__(self):
        return self.favorite_article_title
        
"""
def signupfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return render(request, 'signup.html', {'error': 'このユーザーは登録されています'})
        except:
            # user登録ができたらログインページ移行する
            user = User.objects.create_user(email=email, password=password)
            return render(request, 'login.html')
            
    return render(request, 'signup.html')
"""
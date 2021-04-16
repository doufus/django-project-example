from src.models import BaseModel, models, _
from src.dictionary import PublicChoices as C
# Create your models here.


class BookModel(BaseModel):

    name = models.CharField(max_length=512, verbose_name=_('书名'), help_text=_('书名'))

    state = models.CharField(max_length=12, choices=C.book_state(),
                             default=C.book_state.df, blank=True,
                             verbose_name=_('状态'))
    abstract = models.TextField(default=None, verbose_name=_('摘要'))
    pub_data = models.DateField(verbose_name='出版日期')

    @classmethod
    def _resource(cls):
        return 'books'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('书籍')
        db_table = 'test_books'


class AuthorModel(BaseModel):
    name = models.CharField(max_length=24, verbose_name=_('姓名'), help_text=_('姓名'))
    email = models.EmailField(max_length=255, verbose_name=_('邮箱'), help_text=_('邮箱'))

    @classmethod
    def _resource(cls):
        return 'authors'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('作者')
        db_table = 'test_authors'

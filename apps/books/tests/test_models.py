
from django.utils import timezone
from django.utils.text import slugify
from django.test import TestCase
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import Account
from apps.accounts.factories import factory_accounts, Factory_Account
from apps.tags.factories import factory_tags
from apps.badges.factories import factory_badges
from apps.web_links.factories import factory_web_links
from apps.replies.factories import Factory_Reply
from apps.scopes.factories import Factory_Scope
from apps.tags.models import Tag
from apps.web_links.models import WebLink

from apps.books.factories import Factory_Book, Factory_Writter, factory_books, factory_writters
from apps.books.models import Book, Writter


NOW_YEAR = timezone.datetime.now().year


class BookTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        factory_tags(15)
        factory_web_links(15)
        factory_badges()
        factory_accounts(15)
        factory_writters(15)

    def setUp(self):
        self.book = Factory_Book()

    def test_create_book(self):
        data = dict(
            name='Книжка о программировании на Python 3',
            description="""
In the past, adding page transitions on web pages has been a simple process.
As you click on the link it redirects you to the next page as the browser loads the next page or element.
The web has started to feel outdated if you will think about and there is plenty of room to improve.
Wouldn’t it be great to add some smooth transitions to create a more proficient user experience the next page loads?
""",
            picture='http://transcad.com/miranda.jpeg',
            pages=140,
            publishers='O`Reilly',
            isbn='4515-4579-45478-78129-454',
            year_published=2007,
        )
        book = Book(**data)
        book.full_clean()
        book.save()
        #
        book.tags.add(*Tag.objects.random_tags(3))
        book.links.add(*WebLink.objects.random_weblinks(4))
        book.accounts.add(*Writter.objects.all()[:3])
        #
        Factory_Reply(content_object=book)
        Factory_Reply(content_object=book)
        Factory_Reply(content_object=book)
        for i in range(10):
            Factory_Scope(content_object=book)
        #
        book.refresh_from_db()
        self.assertEqual(book.name, data['name'])
        self.assertEqual(book.slug, slugify(data['name'], allow_unicode=True).replace('-', '_'))
        self.assertEqual(book.description, data['description'])
        self.assertEqual(book.picture, data['picture'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])
        self.assertEqual(book.scopes.count(), 10)
        self.assertEqual(book.replies.count(), 3)
        self.assertEqual(book.tags.count(), 3)
        self.assertEqual(book.links.count(), 4)
        self.assertEqual(book.accounts.count(), 3)

    def test_update_book(self):
        data = dict(
            name='Книга рецептов JS с подробными объяснениями и красивым постраничными оформлением.',
            description="""
Yea it’s a nifty transition and great work to be honest but there is no page reload or browser reload.
Great onepager transition though.
Especially for something using flex-box or 100vh (full height – which you add via jQuery) this would be awesome.
""",
            picture='http://using.com/anaconda.png',
            pages=440,
            publishers='Express',
            isbn='785121-4512-7515-4215-784',
            year_published=2015,
        )
        book = Factory_Book()
        book.name = data['name']
        book.description = data['description']
        book.picture = data['picture']
        book.pages = data['pages']
        book.publishers = data['publishers']
        book.isbn = data['isbn']
        book.year_published = data['year_published']
        book.full_clean()
        book.save()
        self.assertEqual(book.name, data['name'])
        self.assertEqual(book.slug, slugify(data['name'], allow_unicode=True).replace('-', '_'))
        self.assertEqual(book.description, data['description'])
        self.assertEqual(book.picture, data['picture'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])

    def test_delete_book(self):
        self.book.delete()

    def test_unique_slug(self):
        same_name = 'Справочник смелого программиста решившегося пойти против течения и найти себя в жизни таким как есть.'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True).replace('-', '_')
        #
        book1 = Factory_Book()
        book2 = Factory_Book()
        book3 = Factory_Book()
        #
        book1.name = same_name_as_lower
        book2.name = same_name_as_upper
        book3.name = same_name_as_title
        #
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        #
        book1.save()
        book2.save()
        book3.save()
        #
        self.assertEqual(book1.name, same_name_as_lower)
        self.assertEqual(book1.slug, slug_same_name)
        self.assertEqual(book2.name, same_name_as_upper)
        self.assertEqual(book2.slug, slug_same_name + '-2')
        self.assertEqual(book3.name, same_name_as_title)
        self.assertEqual(book3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_rating(self):
        self.book.scopes.clear()
        Factory_Scope(content_object=self.book, scope=3)
        Factory_Scope(content_object=self.book, scope=5)
        Factory_Scope(content_object=self.book, scope=1)
        Factory_Scope(content_object=self.book, scope=2)
        Factory_Scope(content_object=self.book, scope=4)
        Factory_Scope(content_object=self.book, scope=4)
        Factory_Scope(content_object=self.book, scope=1)
        Factory_Scope(content_object=self.book, scope=5)
        self.assertEqual(self.book.get_rating(), 3.125)

    def test_is_new(self):
        #
        self.book.year_published = NOW_YEAR
        self.book.full_clean()
        self.book.save()
        #
        new_book1 = Factory_Book()
        new_book2 = Factory_Book()
        new_book3 = Factory_Book()
        new_book1.year_published = NOW_YEAR - 1
        new_book2.year_published = NOW_YEAR - 2
        new_book3.year_published = NOW_YEAR - 3
        new_book1.full_clean()
        new_book2.full_clean()
        new_book3.full_clean()
        new_book1.save()
        new_book2.save()
        new_book3.save()
        #
        self.assertTrue(self.book.is_new())
        self.assertTrue(new_book1.is_new())
        self.assertFalse(new_book2.is_new())
        self.assertFalse(new_book3.is_new())


class WritterTest(TestCase):
    """

    """

    @classmethod
    def setUpTestData(cls):
        factory_tags(15)
        factory_web_links(15)
        factory_badges()
        factory_accounts(15)
        factory_books(10)

    def setUp(self):
        self.writter = Factory_Writter()

    def test_create_writter(self):
        data = dict(
            name='Николай Левашов',
            about="""
с частицей "бы" и без нее, в начале придаточного предложения с
инфинитивом. Вместо того, чтобы (разг.). Чем на мост нам итти, поищем
лучше
броду. Крылов. Чем кумушек считать трудиться, не лучше ль на себя, кума,
оборотиться. Крылов. Чем бы помочь, он еще мешает.
  3. В сочетании с сравн.
""",
            birthyear=1960,
            deathyear=2012,
        )
        writter = Writter(**data)
        writter.full_clean()
        writter.save()
        self.assertEqual(writter.name, data['name'])
        self.assertEqual(writter.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(writter.about, data['about'])
        self.assertEqual(writter.birthyear, data['birthyear'])
        self.assertEqual(writter.deathyear, data['deathyear'])

    def test_update_writter(self):
        data = dict(
            name='Валерий Дёмин',
            about="""
  1. После сравн. ст. и слов со знач. сравн. ст. присоединяет тот
член предложения, с к-рым сравнивается что-н. лучше поздно, Чем никогда.
Пословица.
  2. с частицей "бы" и без нее, в начале придаточного предложения с
инфинитивом. Вместо того, чтобы (разг.). Чем на мост нам итти, поищем
лучше
броду. Крылов. Чем кумушек считать трудиться, не лучше ль на себя, кума,
оборотиться. Крылов. Чем бы помочь, он еще мешает.
  3. В сочетании с сравн.
ст. и при союзе "тем" в другом предложении употр. в знач. в какой
степени,
насколько. Чем дальше, тем лучше. Чем больше он говорил, тем больше
краснел.
""",
            birthyear=1950,
            deathyear=2016,
        )
        self.writter.name = data['name']
        self.writter.about = data['about']
        self.writter.birthyear = data['birthyear']
        self.writter.deathyear = data['deathyear']
        self.writter.full_clean()
        self.writter.save()
        self.assertEqual(self.writter.name, data['name'])
        self.assertEqual(self.writter.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(self.writter.about, data['about'])
        self.assertEqual(self.writter.birthyear, data['birthyear'])
        self.assertEqual(self.writter.deathyear, data['deathyear'])

    def test_delete_writter(self):
        self.writter.delete()

    def test_unique_slug(self):
        same_name = 'русский Омар Хайам'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify('Омар Хайам', allow_unicode=True).replace('-', '_')
        #
        writter1 = Factory_Writter()
        writter2 = Factory_Writter()
        writter3 = Factory_Writter()
        #
        writter1.name = same_name_as_lower
        writter2.name = same_name_as_upper
        writter3.name = same_name_as_title
        #
        writter1.full_clean()
        writter2.full_clean()
        writter3.full_clean()
        #
        writter1.save()
        writter2.save()
        writter3.save()
        #
        self.assertEqual(writter1.name, same_name_as_lower)
        self.assertEqual(writter1.slug, slug_same_name)
        self.assertEqual(writter2.name, same_name_as_upper)
        self.assertEqual(writter2.slug, slug_same_name + '-2')
        self.assertEqual(writter3.name, same_name_as_title)
        self.assertEqual(writter3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.writter.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_if_birthyear_is_in_future(self):
        self.writter.birthyear = NOW_YEAR + 1
        self.writter.full_clean()
        self.assertRaisesMessage(ValidationError, _('Year of birth can not in future.'), self.writter.full_clean)

    def test_if_deathyear_is_in_future(self):
        self.writter.dearthyear = NOW_YEAR + 1
        self.writter.full_clean()
        self.assertRaisesMessage(ValidationError, _('Year of dearth can not in future.'), self.writter.full_clean)

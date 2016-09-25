
from django.utils.text import slugify
from django.conf import global_settings


# Django-Extensions

SHELL_PLUS = 'ipython'

# additional autoload
SHELL_PLUS_PRE_IMPORTS = (
    ('django.template', ('Template', 'Context')),
    ('django.contrib', 'admin'),
    ('django.apps', 'apps'),
    ('utils', 'django'),
)

# what needn`t rename in time autoload
SHELL_PLUS_MODEL_ALIASES = {
    # 'accounts': {'Account': 'AAAA'},
}

# what needn`t autoload
SHELL_PLUS_DONT_LOAD = [
    # '',  # app name
]


# Django-AutoSlug

AUTOSLUG_SLUGIFY_FUNCTION = lambda value: slugify(value, allow_unicode=True)


# Django-Suit (admin theme)

SUIT_CONFIG = {
    'ADMIN_NAME': 'ProgramerHelperAdmin',
    'CONFIRM_UNSAVED_CHANGES': True,
    'HEADER_DATE_FORMAT': global_settings.DATE_FORMAT,
    'HEADER_TIME_FORMAT': global_settings.TIME_FORMAT,
    'LIST_PER_PAGE': 20,
    'MENU': (
        {
            'app': 'users',
            'icon': 'icon-user',
            'models': ('user', 'level', 'profile', 'auth.group', 'diaries.diary'),
        },
        {
            'app': 'actions',
            'icon': 'icon-signal',
        },
        {
            'app': 'articles',
            'icon': 'icon-pencil',
        },
        {
            'app': 'badges',
            'icon': 'icon-star',
        },
        {
            'app': 'library',
            'icon': 'icon-book',
        },
        {
            'app': 'comments',
            'icon': 'icon-comment',
        },
        {
            'app': 'courses',
            'icon': 'icon-certificate',
        },
        {
            'app': 'forums',
            'icon': 'icon-th',
        },
        {
            'app': 'notifications',
            'icon': 'icon-envelope',
        },
        {
            'app': 'newsletters',
            'icon': 'icon-info-sign',
        },
        {
            'app': 'opinions',
            'icon': 'icon-thumbs-up',
        },
        {
            'app': 'polls',
            'icon': 'icon-flag',
        },
        {
            'app': 'questions',
            'icon': 'icon-question-sign',
        },
        {
            'app': 'marks',
            'icon': 'icon-ok',
        },
        {
            'app': 'snippets',
            'icon': 'icon-tasks',
        },
        {
            'app': 'solutions',
            'icon': 'icon-file',
        },
        {
            'app': 'tags',
            'icon': 'icon-tags',
        },
        {
            'app': 'testing',
            'icon': 'icon-repeat',
        },
        {
            'app': 'utilities',
            'icon': 'icon-gift',
        },
        {
            'app': 'web_links',
            'icon': 'icon-download-alt',
        },
    ),
    'MENU_OPEN_FIRST_CHILD': True,
    # 'SEARCH_URL': 'admin:account_account_changelist',
    'SEARCH_URL': '',
    'SHOW_REQUIRED_ASTERISK': True,
    'VERSION': ''
}


# def generate_captcha(request):
#     color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     img = Image.new('RGBA', (160, 80), color)
#     imgDrawer = ImageDraw.Draw(img)
#     textImg = Image.new('RGBA', (160, 80))
#     tmpDraw = ImageDraw.Draw(textImg)
#     font = ImageFont.truetype("resources/UbuntuMono-RI.ttf", 26)
#     i = 15
#     key = []
#     for x in xrange(1, 7):
#         r = str(random.randint(0, 9))
#         key.append(r)
#         tmpDraw.text((i, random.randint(20, 30)), r,
#                      font=font, fill=(0, 0, 0))
#         i += 22
#     request.session['captcha'] = ''.join(key)
#     for o in xrange((80 * 160) / 500):
#         imgDrawer.line((random.randint(0, 160), random.randint(0, 80), random.randint(0, 160), random.randint(0, 80)),
#                        fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
#     output = StringIO.StringIO()
#     textImg = textImg.rotate(random.randint(-20, 20))
#     mask = Image.new('RGBA', (160, 80), (0, 0, 0))
#     mask.paste(textImg, (0, 0))
#     img.paste(textImg, (0, 0), mask)
#     img.save(output, format='png')
#     return StreamingHttpResponse([output.getvalue()], content_type="image/png")
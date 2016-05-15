
import collections
import functools

from django.contrib.auth import get_user_model
from django.db import models

from apps.app_badges.models import GettingBadge, Badge
from apps.app_questions.models import Question, Answer


def point_execution_in_terminal(function):
    """Decorator, what type point(.) in terminal when function execution."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        print('.')
        return function(*args, **kwargs)
    return wrapper


class BadgeManager(models.Manager):
    """
    Model manager for working with badges of account
    """
    def validate_badges(self, account_natural_key=None):
        # account = get_user_model().objects.get_by_natural_key(account_natural_key)
        GettingBadge.objects.filter().delete()
        # print('[', end='')
        self.check_badge_Favorite_Question()
        self.check_badge_Stellar_Question()
        self.check_badge_Nice_Question()
        self.check_badge_Good_Question()
        self.check_badge_Great_Question()
        self.check_badge_Popular_Question()
        self.check_badge_Notable_Question()
        self.check_badge_Famous_Question()
        self.check_badge_Schoolar()
        self.check_badge_Student()
        self.check_badge_Tumbleweed()
        self.check_badge_Enlightened()
        self.check_badge_Explainer()
        self.check_badge_Refiner()
        self.check_badge_Illuminator()
        self.check_badge_Guru()
        self.check_badge_Nice_Answer()
        self.check_badge_Good_Answer()
        self.check_badge_Great_Answer()
        self.check_badge_Reversal()
        self.check_badge_Revival()
        self.check_badge_Necromancer()
        # print(']', end='')

    def has_badge(self, account, badge):
        """Checkup presence badge in account."""

        try:
            GettingBadge.objects.get(account=account, badge=badge)
        except GettingBadge.DoesNotExist:
            return False
        else:
            return True

    def get_badges(self, account):
        """Getting all badges certain account."""

        pass

    def last_got_badges(self, count_last_getting=10):
        """Getting listing last getting badges of accounts."""

        return GettingBadge.objects.order_by('-date_getting')[:count_last_getting]

    def added_badge_to_accounts(self, accounts_pks, badge_name):
        """Add badge to accounts listing in accounts_pks as their primary keys."""

        if accounts_pks and badge_name:
            # get badge
            badge = Badge.objects.get(name__icontains=badge_name)
            # iteration on primary keys of accounts and adding badge
            for account_pk in accounts_pks:
                account = self.get(pk=account_pk)
                GettingBadge.objects.update_or_create(user=account, badge=badge)

    @point_execution_in_terminal
    def check_badge_Favorite_Question(self):
        """Question if favorited at least 5 users."""

        QUESTION_AS_FAVORITE = 5
        all_questions_with_certain_favorites = Question.objects.questions_by_min_count_favorits(
            min_count_favorits=QUESTION_AS_FAVORITE,
        )
        accounts_pks = all_questions_with_certain_favorites.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='favorite question')

    @point_execution_in_terminal
    def check_badge_Stellar_Question(self):
        """Question if favorited at least 10 users."""

        QUESTION_AS_STELLAR = 10
        all_questions_with_certain_favorites = Question.objects.questions_by_min_count_favorits(
            min_count_favorits=QUESTION_AS_STELLAR,
        )
        accounts_pks = all_questions_with_certain_favorites.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='stellar question')

    @point_execution_in_terminal
    def check_badge_Nice_Question(self):
        """Scope of question must be 5 and more."""

        SCOPE_QUESTION_AS_NICE = 5
        nices_questions = Question.objects.questions_by_scopes(min_scope=SCOPE_QUESTION_AS_NICE)
        accounts_pks = nices_questions.values_list('author', flat=True)
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='nice question')

    @point_execution_in_terminal
    def check_badge_Good_Question(self):
        """Scope of question must be 10 and more."""

        SCOPE_QUESTION_AS_GOOD = 10
        nices_questions = Question.objects.questions_by_scopes(min_scope=SCOPE_QUESTION_AS_GOOD)
        accounts_pks = nices_questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='good question')

    @point_execution_in_terminal
    def check_badge_Great_Question(self):
        """Scope of question must be 20 and more."""

        SCOPE_QUESTION_AS_GREAT = 20
        nices_questions = Question.objects.questions_by_scopes(min_scope=SCOPE_QUESTION_AS_GREAT)
        accounts_pks = nices_questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='great question')

    @point_execution_in_terminal
    def check_badge_Popular_Question(self):
        """Count views of question must be 100 and more."""

        COUNT_VIEWS_QUESTION_AS_POPULAR = 100
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_POPULAR)
        accounts_pks = questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='popular question')

    @point_execution_in_terminal
    def check_badge_Notable_Question(self):
        """Count views of question must be 500 and more."""

        COUNT_VIEWS_QUESTION_AS_NOTABLE = 500
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_NOTABLE)
        accounts_pks = questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='notable question')

    @point_execution_in_terminal
    def check_badge_Famous_Question(self):
        """Count views of question must be 1000 and more."""

        COUNT_VIEWS_QUESTION_AS_FAMOUS = 1000
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_FAMOUS)
        accounts_pks = questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='famous question')

    @point_execution_in_terminal
    def check_badge_Schoolar(self):
        """Have question with acceptabled answer."""

        accounts_pks = Answer.objects.accepted_answers().values_list('question__author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='schoolar')

    @point_execution_in_terminal
    def check_badge_Student(self):
        """Accept an answers on 5 questions."""

        NECESSARY_COUNT_ACCEPTED_ANSWERS = 5
        undistinct_account_pks = Answer.objects.accepted_answers().values_list('question__author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_accepted_answers = filter(
            lambda item: item[1] >= NECESSARY_COUNT_ACCEPTED_ANSWERS,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        accounts_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_accepted_answers)
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='student')

    @point_execution_in_terminal
    def check_badge_Tumbleweed(self):
        """Asked a question with zero score or less, no answers."""

        non_interesting_questions = Question.objects.non_interesting_questions()
        accounts_pks = non_interesting_questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='tumbleweed')

    @point_execution_in_terminal
    def check_badge_Enlightened(self):
        """Had accepted answer with score of 10 or more."""

        MIN_SCOPE_ANSWER_FOR_ENLIGHTENED = 10
        answers_with_min_scope = Answer.objects.answers_by_scopes(min_scope=MIN_SCOPE_ANSWER_FOR_ENLIGHTENED)
        accepted_answers = Answer.objects.accepted_answers()
        accepted_answers_with_min_scope = answers_with_min_scope & accepted_answers
        accounts_pks = accepted_answers_with_min_scope.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='enlightened')

    @point_execution_in_terminal
    def check_badge_Explainer(self):
        """Answer on 1 question within 24 hours and with scope > 0."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        accounts_pks = useful_quickly_answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='explainer')

    @point_execution_in_terminal
    def check_badge_Refiner(self):
        """Answer on 5 questions within 24 hours and with scope > 0."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        undistinct_account_pks = useful_quickly_answers.values_list('author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_answers = filter(
            lambda item: item[1] >= 5,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        accounts_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_answers)
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='refiner')

    @point_execution_in_terminal
    def check_badge_Illuminator(self):
        """Answer on 10 questions within 24 hours and with scope > 0."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        undistinct_account_pks = useful_quickly_answers.values_list('author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_answers = filter(
            lambda item: item[1] >= 10,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        accounts_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_answers)
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='illuminator')

    @point_execution_in_terminal
    def check_badge_Guru(self):
        """Given accepted answer with score of 5 or more."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=5)
        accepted_answers = Answer.objects.accepted_answers()
        good_accepted_answers = useful_answers & accepted_answers
        accounts_pks = good_accepted_answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='guru')

    @point_execution_in_terminal
    def check_badge_Nice_Answer(self):
        """Answer score of 5 or more."""

        answers = Answer.objects.answers_by_scopes(min_scope=5)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='nice answer')

    @point_execution_in_terminal
    def check_badge_Good_Answer(self):
        """Answer score of 10 or more."""

        answers = Answer.objects.answers_by_scopes(min_scope=10)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='good answer')

    @point_execution_in_terminal
    def check_badge_Great_Answer(self):
        """Answer score of 15 or more."""

        answers = Answer.objects.answers_by_scopes(min_scope=15)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='great answer')

    @point_execution_in_terminal
    def check_badge_Populist(self):
        """Highest scoring answer that outscored an accepted answe."""

    @point_execution_in_terminal
    def check_badge_Reversal(self):
        """Provide an answer of +1 and more score to a question of -1 and less score."""

        questions_by_max_scope = Question.objects.questions_by_scopes(max_scope=-1)
        answers_by_min_scope = Answer.objects.answers_by_scopes(min_scope=1)
        pks_answers_with_questions_by_max_scope = questions_by_max_scope.values_list('answers', flat=True).distinct()
        reversal_answers = answers_by_min_scope.filter(pk__in=pks_answers_with_questions_by_max_scope)
        accounts_pks = reversal_answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='reversal')

    @point_execution_in_terminal
    def check_badge_Revival(self):
        """Answer more than 7 days after a question was asked."""

        revival_answers = Answer.objects.revival_answers(count_days=7)
        accounts_pks = revival_answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='revival')

    @point_execution_in_terminal
    def check_badge_Necromancer(self):
        """Answer a question more than 7 days later with score of 5 or more."""

        revival_answers = Answer.objects.revival_answers(count_days=7)
        answers_by_min_scope = Answer.objects.answers_by_scopes(min_scope=5)
        revival_answers_by_min_scope = answers_by_min_scope & revival_answers
        accounts_pks = revival_answers_by_min_scope.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='necromancer')

    @point_execution_in_terminal
    def check_badge_SelfLearner(self):
        """Answer your own question with score of 1 or more."""

        answers = Answer.objects.answers_with_scopes().filter(question__author=models.F('author')).filter(scope__gte=1)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='self-learner')

    @point_execution_in_terminal
    def check_badge_Teacher(self):
        """Answer a question with score of 1 or more."""

        answers = Answer.objects.answers_with_scopes().filter(scope__gte=1)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='teacher')

    @point_execution_in_terminal
    def check_badge_Autobiograther(self):
        """Completed fill up account profile."""

        accounts_pks = list()
        filled_accounts_profiles = get_user_model().objects.get_filled_accounts_profiles()
        for account_pk, percent in filled_accounts_profiles.items():
            if percent == 100:
                accounts_pks.append(account_pk)
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='autobiograther')

    @point_execution_in_terminal
    def check_badge_Commentator(self):
        """Leave 10 comments."""

        accounts_with_count_comments = get_user_model().objects.annotate(count_comments=models.Count('comments', distinct=True))
        commentators = accounts_with_count_comments.filter(count_comments__gte=10)
        accounts_pks = commentators.values_list('pk', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='commentator')

    @point_execution_in_terminal
    def check_badge_Sociable(self):
        """Leave 20 comments."""

        accounts_with_count_comments = get_user_model().objects.annotate(count_comments=models.Count('comments', distinct=True))
        commentators = accounts_with_count_comments.filter(count_comments__gte=20)
        accounts_pks = commentators.values_list('pk', flat=True).distinct()
        self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='sociable')

    @point_execution_in_terminal
    def check_badge_Enthusiast(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Fanatic(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Assduous(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Epic(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Legendary(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Citize(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Talkative(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Outspoken(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Yearning(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Civic_Duty(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Electorate(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Citizen_Patrol(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Depute(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Marshal(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Critic(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Editor(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Organizer(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Proofreader(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Suffrage(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Vox_Populi(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Supporter(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Taxonomist(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Publicist(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Tester(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Creator_Tests(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Clear_Mind(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Clear_Head(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Closer_Questions(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Deleter_Questions(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Dispatcher(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Sage(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Have_Opinion(self):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='')

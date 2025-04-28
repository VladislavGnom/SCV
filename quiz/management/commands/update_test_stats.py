from django.core.management.base import BaseCommand
from django.db.models import Avg, Count, F, DurationField, ExpressionWrapper
from quiz.models import Test, UserTestResult, TestStatistics
from datetime import timedelta

class Command(BaseCommand):
    help = 'Обновляет статистику тестов'

    def handle(self, *args, **options):
        tests = Test.objects.annotate(
            avg_score=Avg('user_results__score'),
            completion_count=Count('user_results'),
            total_users=Count('groups__members', distinct=True),
            avg_time=Avg(
                ExpressionWrapper(
                    F('user_results__completed_at') - F('user_results__started_at'),
                    output_field=DurationField()
                )
            )
        )

        for test in tests:
            completion_rate = (test.completion_count / test.total_users) * 100 if test.total_users > 0 else 0
            
            TestStatistics.objects.update_or_create(
                test=test,
                defaults={
                    'average_score': test.avg_score or 0,
                    'completion_rate': completion_rate,
                    'average_time_spent': test.avg_time or timedelta(0)
                }
            )
        self.stdout.write(self.style.SUCCESS('Статистика успешно обновлена'))
        
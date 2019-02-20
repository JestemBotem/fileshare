from django.db import models
from django.db.models import F, Count, Q
from django.db.models.functions import TruncDate


class ProtectedResourceManager(models.Manager):
    def increase_view_count(self, resource_id):
        self.filter(id=resource_id).update(views_count=F('views_count') + 1)

    def get_access_report(self):
        q_visited_links = Count('views_count', filter=Q(uri__isnull=False))
        q_downloaded_files = Count('views_count', filter=Q(uri__isnull=True))

        report = self.all().annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            visited_links=q_visited_links,
            downloaded_files=q_downloaded_files
        ).order_by('date')

        return report

    # def get_access_report_grouped(self):
    #     access_report = self.get_access_report()
    #
    #     report = {}
    #
    #     for row in access_report:
    #         report[row['date']] = {
    #             'visited_links': row['visited_links'],
    #             'downloaded_files': row['downloaded_files'],
    #         }
    #
    #     return report

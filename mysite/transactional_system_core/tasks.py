from celery import shared_task
import time
@shared_task(bind=True)
def sleep_time_emulates(self):
    try:
        time.sleep(5)
        raise Exception("Opps. Exception occurred")
    except Exception as err:
        print("Error occurred")
        self.retry(exc=err, countdown=3, max_retries=3)

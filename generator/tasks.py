from time import sleep

from celery import shared_task
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def generate_csv(self, duration):
    progress_recorder = ProgressRecorder(self)
    for i in range(duration):
        progress_recorder.set_progress(i + 1, duration, 'Processing')
        sleep(1)
    return 'Done'

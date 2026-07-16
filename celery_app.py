from celery.schedules import crontab

def celery_init_app(app, celery):
    celery.config_from_object(app.config["CELERY"])

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask
    celery.conf.imports = ("backend.tasks",)
    celery.conf.beat_schedule = {
        "daily-reminder": {
            "task": "backend.tasks.send_daily_reminders",
            "schedule": crontab(hour=9, minute=0)
        },
        "monthly-report": {
            "task": "backend.tasks.send_monthly_report",
            "schedule": crontab(day_of_month=1, hour=8, minute=0),
        },
    }
    return celery
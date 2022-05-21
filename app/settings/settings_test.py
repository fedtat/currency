from settings.settings import *  # noqa: F403

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ()  # noqa: F405

CELERY_TASK_ALWAYS_EAGER = True

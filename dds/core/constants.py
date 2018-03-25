class CloningStatuses:
    PROCESSING = 0
    SUCCEED = 1
    FAILED = 2

    CLONING_STATUSES = (
        (PROCESSING, 'Processing is in progress'),
        (SUCCEED, 'Processing is succeed'),
        (FAILED, 'Processing is failed'),
    )

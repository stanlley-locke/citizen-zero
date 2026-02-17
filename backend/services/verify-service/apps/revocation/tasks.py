from celery import shared_task

@shared_task
def update_revocation_list():
    # Sync revocation list from blockchain or ID service
    print("Updating revocation list...")
    return "CRL Updated"

"""Auditing for fee mutations triggered by authenticated Django requests."""
from contextvars import ContextVar

from django.db.models.signals import post_delete, post_save, pre_save

_current_user = ContextVar('academy_actor', default=None)
TRACKED = {
    'FeePlan': ('name', 'amount', 'frequency', 'is_active'),
    'Invoice': ('student_id', 'description', 'amount', 'amount_paid', 'due_date', 'status'),
    'Payment': ('invoice_id', 'amount', 'payment_date', 'method'),
}


class AuditActorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        actor = request.user if request.user.is_authenticated else None
        token = _current_user.set(actor)
        try:
            return self.get_response(request)
        finally:
            _current_user.reset(token)


def _snapshot(instance):
    return {name: str(getattr(instance, name)) for name in TRACKED[type(instance).__name__]}


def record_before(sender, instance, **kwargs):
    if not instance.pk:
        instance._audit_before = None
    else:
        previous = sender.objects.filter(pk=instance.pk).first()
        instance._audit_before = _snapshot(previous) if previous else None


def record_after(sender, instance, created, **kwargs):
    actor = _current_user.get()
    if actor is None:
        return
    from .models import AuditLog
    before = getattr(instance, '_audit_before', None)
    after = _snapshot(instance)
    changed = {key: {'from': before.get(key) if before else None, 'to': value}
               for key, value in after.items() if before is None or before.get(key) != value}
    if changed:
        AuditLog.objects.create(actor=actor, action='fee_record_created' if created else 'fee_record_updated',
                                target=f'{sender.__name__} #{instance.pk}', details=changed)


def record_deleted(sender, instance, **kwargs):
    actor = _current_user.get()
    if actor is None:
        return
    from .models import AuditLog
    AuditLog.objects.create(actor=actor, action='fee_record_deleted',
                            target=f'{sender.__name__} #{instance.pk}', details=_snapshot(instance))


def install_audit_signals():
    from fees.models import FeePlan, Invoice, Payment
    for model in (FeePlan, Invoice, Payment):
        pre_save.connect(record_before, sender=model, dispatch_uid=f'audit_before_{model.__name__}')
        post_save.connect(record_after, sender=model, dispatch_uid=f'audit_after_{model.__name__}')
        post_delete.connect(record_deleted, sender=model, dispatch_uid=f'audit_delete_{model.__name__}')

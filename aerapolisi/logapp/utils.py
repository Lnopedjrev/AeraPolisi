from django.contrib.auth.mixins import AccessMixin


class NonLoginRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        return context

from django.contrib.auth.mixins import AccessMixin
from django.core.paginator import Paginator


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context



def paginate(request, qers, limit=3):
    paginated_qers = Paginator(qers, limit)
    page_num = request.GET.get('page')
    return paginated_qers.get_page(page_num)


def is_htmx(request, boost_check=True):
    hx_boost = request.headers.get('Hx-Boosted')
    hx_request = request.headers.get('Hx-Request')

    if boost_check and hx_boost:
        return False

    elif boost_check and not hx_boost and hx_request:
        return True


class NonLoginRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

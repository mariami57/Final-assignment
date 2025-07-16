from django.contrib.auth.mixins import UserPassesTestMixin


class UserIsCreatorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.pk == self.get_object().user.pk
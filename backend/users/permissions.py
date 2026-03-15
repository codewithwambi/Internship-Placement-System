from django.contrib.auth.mixins import UserPassesTestMixin

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "STUDENT"
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelTestCase(TestCase):

    def test_create_profile(self):
        # Create a user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

        # Create a profile associated with the user
        profile = Profile.objects.create(user=user)

        # Check if the profile is created successfully
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.image.path, 'profile_pics/default.jpg')  # Assuming default.jpg is uploaded

        # Check if email_verified field defaults to False
        self.assertFalse(profile.email_verified)

        # Check the string representation of the profile
        self.assertEqual(str(profile), 'testuser')
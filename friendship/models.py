# models.py

from django.db import models
from django.contrib.auth import get_user_model

class FriendRequest(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    
    from_user = models.ForeignKey(get_user_model(), related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} ({self.status})'



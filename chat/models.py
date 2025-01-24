from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True
    )  # Null for group messages
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_group_message = models.BooleanField(default=False)

    def __str__(self):
        if self.is_group_message:
            return f"Group: {self.sender.username} - {self.content[:20]}"
        else:
            return f"Private: {self.sender.username} to {self.recipient.username} - {self.content[:20]}"

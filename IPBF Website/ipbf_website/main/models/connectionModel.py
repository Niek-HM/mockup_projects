from django.db import models

class Connection(models.Model):
    """
    I wanted to use this for the board etc, but they won't be on the website.
    Maybe simplify in just the name?

    This just returns authors of books atm.
    """
    name = models.CharField(max_length=64)

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=24, null=True, blank=True)

    executive_board = models.BooleanField(default=False)
    ima_board = models.BooleanField(default=False)

    def __str__(self):
        return self.name
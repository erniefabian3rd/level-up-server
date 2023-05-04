from django.db import models

class Event(models.Model):

    description = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    time = models.TimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", related_name="attending")
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
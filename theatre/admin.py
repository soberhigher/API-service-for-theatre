from django.contrib import admin

from theatre.models import (Play,
                            Actor,
                            Genre,
                            TheatreHall,
                            Reservation,
                            Performance,
                            Ticket,
                            )

admin.site.register(Play)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(TheatreHall)
admin.site.register(Reservation)
admin.site.register(Performance)
admin.site.register(Ticket)

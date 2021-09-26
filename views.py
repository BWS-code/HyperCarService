from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')

class TicketView(View):
    table = []
    time = 0
    times = {'/get_ticket/change_oil': 2,
            '/get_ticket/inflate_tires': 5,
            '/get_ticket/diagnostic': 30}

    def get_ticket_num(self):
        return len(self.table) + 1

    def get_ticket_time(self, path):
        for service in self.times:
            self.time += self.times[service] * self.table.count(service)
            if service == path:
                self.table.append(path)
                return self.time

    def get(self, request):
        context = {
            'ticket_num': self.get_ticket_num(),
            'ticket_time': self.get_ticket_time(request.path)
        }
        return render(request, 'tickets/ticket.html', context)

class OpsView(View):
    next_ticket = [0]

    def get(self, request):
        context = {
            'oil_queue': TicketView.table.count('/get_ticket/change_oil'),
            'tires_queue': TicketView.table.count('/get_ticket/inflate_tires'),
            'diagnostic_queue': TicketView.table.count('/get_ticket/diagnostic'),
        }
        return render(request, 'tickets/processing.html', context)

    def post(self, request):
        def get_next():
            for service in TicketView.times:
                for i, e in enumerate(TicketView.table):
                    if e == service:
                        TicketView.table[i] = '-'
                        return i + 1
        self.next_ticket[0] = get_next()
        return redirect('next')

class NextView(View):
    def get(self, request):
        context = {
            'next_ticket': OpsView.next_ticket[0]
        }
        return render(request, 'tickets/next.html', context)

from django.shortcuts import render

def election_overview(request):
    return render(request, "frontend/election_overview.html")
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from polls.models import Poll,Choice
from django.core.urlresolvers import reverse
from django.template import loader,RequestContext

        
# Create your views here.
def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    context = { 'latest_poll_list':latest_poll_list}
    return render(request,'polls/index.html',context)
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, { 'latest_poll_list':latest_poll_list })
    #return HttpResponse(template.render(context))
    #output = ', '.join([p.question for p in latest_poll_list])
    #return HttpResponse(output)


def detail(request,poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
    	raise Http404
    return render(request,'polls/detail.html',{'poll':poll})

    #return HttpResponse("You're looking at poll %s"%poll_id)

def results(request,poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request,'polls/results.html',{'poll':poll})
    #return HttpResponse("You're looking at the results of the polls %s"%poll_id)

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Rediplay the poll voting form 
        return render(request, 'polls/detail.html' , { 'poll': p,'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))


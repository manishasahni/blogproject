from django.shortcuts import render_to_response
from django.template import RequestContext

#profile view renders the profile page of the user
#It displays the username and list of articles written by the logged in user
def profile(request):
    u = request.user
    article_list = u.article_set.all()
    return render_to_response("registration/profile.html", {
        'article_list':article_list}, context_instance=RequestContext(request))
        
                                    

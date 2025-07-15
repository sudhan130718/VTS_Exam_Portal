from .models import Trainer

def developer_list(request):
    developers = Trainer.objects.filter(user__role='developer', is_active=True)
    
    print('all_developers:', developers)

    return {'all_developers': developers}


from datetime import datetime

def global_greeting(request):
    now = datetime.now()

    # Dynamic greeting
    if now.hour < 12:
        greeting = "Good Morning"
    elif now.hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return {
        'greeting': greeting,
        'today': now
    }


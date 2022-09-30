import os
import pickle
from django.shortcuts import render
from SpotifySkip import settings

def predict(list):
    path=os.path.join(settings.MODEL_ROOT, 'my_model.pkl')
    model = pickle.load(open(path, 'rb'))
    result=model.predict([list])
    return result[0]

def index(request):
    if request.method=="POST" :
        X=[]
        X+=[request.POST['session_length']]
        X+=[request.POST['no_pause_before_play']]
        X+=[request.POST['hist_user_behavior_n_seekfwd']]
        X+=[request.POST['hour_of_day']]
        X+=[request.POST['context_type']]
        X+=[request.POST['hist_user_behavior_reason_start']]
        X+=[request.POST['context_switch']]
        X+=[request.POST['hist_user_behavior_reason_end']]
        X+=[request.POST['session_position']]
        X+=[request.POST['weekday']]
        X+=[request.POST['premium']]
        X+=[request.POST['hist_user_behavior_n_seekback']]
        try :
            X=[float(i) for i in X]
        except:
            return render(request,'index.html',{'prediction':"error occurred"})
        prediction=predict(X)
        if prediction==1:
            prediction='music will be skipped'
        else :
            prediction='music will not be skipped'
        return render(request,'index.html',{'prediction':prediction})
    return render(request,'index.html')

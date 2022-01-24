from django.shortcuts import render,redirect
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from rock_paper_scissor.models import Player,Result
import random
import logging

# Create your views here.
log = logging.getLogger(__name__)
def home(request):
    #home and start game logic
    if request.method=='POST':
        playername=request.POST.get('name')
        if User.objects.filter(username__iexact=playername):
            messages.warning(request,'This name is already exist,please try another one..')
            return HttpResponseRedirect(request.path_info)
        create_user = User.objects.create(first_name = playername,username=playername)
        create_player = Player.objects.create(name=playername,user= create_user)
        return redirect('start_game')
    return render(request,'index.html')


def game(request):
    #rock paper and scissor logic

    gamelist=['rock','paper','scissor']
    bot_action=random.choice(gamelist)
    user = Player.objects.all().last()
    if request.method =='POST':
        user_answer=request.POST.get('name')
        if user_answer==bot_action:
            messages.info(request,f"Both players selected.It's a tie")
            result = Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='Tie')
            log.debug('both players selected .its tie')
        elif user_answer == 'rock':
            if bot_action =='scissor':
                messages.success(request,"rock smashes scissor! you win")
                result=Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='win')
                log.debug(f"paper covers rock! you lose.Action:{bot_action} User-{user_answer}")
            else:
                result=Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='lose')
                messages.info(request,"paper covers rock ! you lose.")
                log.debug(f"scissor cuts paper! you lose. Action: Bot-{bot_action}User-{user_answer}")

        elif user_answer == 'paper':
            if bot_action =='rock':
                messages.success(request,"paper covers rock ! you lose.")
                result=Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='win')
                log.debug(f"paper covers rock! you lose.Action:{bot_action} User-{user_answer}")
            else:
                result=Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='lose')
                messages.info(request,"scissorcuts paper ! you lose.")
                log.debug(f"scissor cuts paper! you lose. Action: Bot-{bot_action}User-{user_answer}")

        elif user_answer == 'scissor':
            if bot_action =='paper':
                result=Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='win')
                messages.info(request,'scissor cuts paper! you win')
                log.debug(f"scissor cuts paper! you win.Action: Bot - {bot_action} User-{user_answer}")
            else:
                 result=Result.objects.create(player=user,bot_move=bot_action,user_move=user_answer,status='lose')
                 messages.info(request,"rock smashes scissor! you lose")
                 log.debug(f"rock smashes scissor! you lose. Action: Bot-{bot_action}User-{user_answer}")

    return render(request,'game.html',{'user':user})


def result(request):
    #all user result
    res = Result.objects.all().order_by('-id')
    context = {'res':res}
    return render(request,'result.html',context)

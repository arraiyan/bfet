
import logging
from inf import env
from telegram import *
from telegram.ext import *
import random
from time import timezone
import pandas as pd
from datetime import datetime
import time
from captcha.image import ImageCaptcha
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        user = update.effective_user
        chat_id = update.message.chat.id
        update.message.reply_text(env.start_message,parse_mode='HTML')
        u_list = list()
        for i,j in env.users_data.items():
            u_list.append(i)
        if not update.message.chat.id in u_list:
            env.users_data[chat_id]={'captcha':{'status':False,'key':str()},'step':0,'data':[str(update.message.chat.id),str(update.message.from_user.username)]}
            opts = list()#captcha list
            for i in range(4):
                opts.append(str(random.randint(0,999)))
            env.users_data[int(update.effective_chat.id)]['captcha']['key'] = str(opts[int(random.randint(0,3))])

            im = ImageCaptcha(fonts=['font/LGB.ttf']).generate(env.users_data[int(update.effective_chat.id)]['captcha']['key'] )
            context.bot.send_photo(chat_id = update.effective_chat.id,photo = im)
            time.sleep(0.3)      
            update.message.reply_text("solve the captcha")
        return
    else:
        return

def getexcel(data):
    
    df1 = pd.DataFrame(data,columns=['col 1', 'col 2','col3','col4','col5','col6','col7','col8'])
    n = str(f'static/payment{datetime.date(datetime.now())}.xlsx')
    df1.to_excel(n)
    return n 

def csv(update:Update,context:CallbackContext):
    k = list()
    for i,j in env.users_data.items():
        k.append(j['data'])
    print(f'k...{k}')
    if update.message.from_user.id in env.admins:
        
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(getexcel(k), 'rb'))
        return
    return

def login(update:Update,context:CallbackContext)->None:
    if update.message.chat.type == 'private':
        d = str(update.message.text).lstrip('/login').lstrip(' ')
        print(d)
        if d == env.password:
            env.admins.append(update.message.chat.id)
            update.message.reply_text('logged in')
            return
    return

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

def submit_info(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text('Send your transaction ID!',reply_markup=reply_markup)
    env.users_data[int(update.effective_chat.id)]['step']=1
    return

def echo(update: Update, context: CallbackContext) -> None:
    echo = update.message.text
    print(env.users_data)
    if update.message.chat.type == 'private':
        u_list = list()
        for i,j in env.users_data.items():
            u_list.append(i)
        if update.message.chat.id in u_list:
            if env.users_data[int(update.effective_chat.id)]['captcha']['status']==False:
                if str(env.users_data[int(update.effective_chat.id)]['captcha']['key'])==str(echo).lstrip(' '):
                    env.users_data[int(update.effective_chat.id)]['captcha']['status']=True
                    update.message.reply_text('Thank you for solving the cpatcha')
                    update.message.reply_text(' to buy BFET you can send any amount to one of those wallet address\n\n0x16190E0CEbBb690d428e08858e059e3cC0DB7eD6\n\nUSDT, BUSD. for every 1 USDT or 1BUSD you will get 1000 BFET')
                    reply_markup = ReplyKeyboardMarkup([['💲SubmitInfo']],resize_keyboard=True) 
                    update.message.reply_text('After making the payment click the button',reply_markup=reply_markup,parse_mode='HTML')
                else:
                    

                    opts = list()#captcha list
                    for i in range(4):
                        opts.append(str(random.randint(0,999)))
                    env.users_data[int(update.effective_chat.id)]['captcha']['key'] = str(opts[int(random.randint(0,3))])

                    im = ImageCaptcha(fonts=['font/LGB.ttf']).generate(env.users_data[int(update.effective_chat.id)]['captcha']['key'] )
                    context.bot.send_photo(chat_id = update.effective_chat.id,photo = im)
                    time.sleep(0.3)      
                    update.message.reply_text("solve the captcha")
                    update.message.reply_text('Please Solve it again')
                    return
            
            elif env.users_data[int(update.effective_chat.id)]['captcha']['status']==True:
                if env.users_data[int(update.effective_chat.id)]['step']==0:
                    update.message.reply_text(' to buy BFET you can send any amount to one of those wallet address\n\n0x16190E0CEbBb690d428e08858e059e3cC0DB7eD6\n\nUSDT, BUSD. for every 1 USDT or 1BUSD you will get 1000 BFET')
                    reply_markup = ReplyKeyboardMarkup([['💲SubmitInfo']],resize_keyboard=True) 
                    update.message.reply_text('After making the payment click the button',reply_markup=reply_markup,parse_mode='HTML')
                    return
                if env.users_data[int(update.effective_chat.id)]['step']==1:
                    env.users_data[int(update.effective_chat.id)]['data'].append(echo)
                    update.message.reply_text('Send how much you\'ve sent')
                    env.users_data[int(update.effective_chat.id)]['step']=2
                    return
                if env.users_data[int(update.effective_chat.id)]['step']==2:
                    env.users_data[int(update.effective_chat.id)]['data'].append(echo)
                    update.message.reply_text('Send your erc20 wallet address so we can send your BFET to it')
                    env.users_data[int(update.effective_chat.id)]['step']=3
                    return
                if env.users_data[int(update.effective_chat.id)]['step']==3:
                    env.users_data[int(update.effective_chat.id)]['data'].append(echo)
                    update.message.reply_text('Thank you soon you will recieve you BFETs')
                    env.users_data[int(update.effective_chat.id)]['step']='completed'
                    print(env.users_data)
                    d = env.users_data[int(update.effective_chat.id)]['data']
                    if len(env.admins)>=1:
                        for i in env.admins:
                            update.message.reply_text(f'a new user has paid \n\n his data \n {d}')
                    return
                return
        else:
            return
            
        


def main() -> None:
    updater = Updater(env.API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("csv", csv))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'💲SubmitInfo'), submit_info))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

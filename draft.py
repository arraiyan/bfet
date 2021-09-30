
from telegram import *
from telegram.ext import *
from inf import env
from PIL import Image
def start_callback(update: Update, context: CallbackContext) -> None:
    print(update.message.chat.id)
    reply_markup = ReplyKeyboardMarkup([['💲BuyTokens'],['📈About','🧰Support']],resize_keyboard=True) 
    update.message.reply_text(env.start_message,parse_mode='HTML')
    update.message.reply_text(env.start_message2,reply_markup=reply_markup,parse_mode='HTML')
def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(env.start_message,parse_mode='HTML')
    return

def support(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type=='private':
        update.message.reply_text(f'🧰 Contact support:https://twitter.com/BFEtoken\nour youtube channel\n 👉👉👉 (https://www.youtube.com/channel/UCw5YxT3TCxiQfAUyCjD4Jqw)\n\n👉👉👉     <a href="{env.Grouplink}">Join Our Telegram Group</a>   ({env.Grouplink})\nJoin telegram channel\n👉👉👉 <a href="{env.ChannelLink}">Join channel</a>   ({env.ChannelLink})\n',parse_mode='HTML')
        return
def dash(update:Update,context:CallbackContext)->None:
    reply_markup = ReplyKeyboardMarkup([['💲BuyTokens'],['📈About','🧰Support']],resize_keyboard=True) 
    update.message.reply_text(env.start_message2,reply_markup=reply_markup,parse_mode='HTML')
    return

def start_with_shipping_callback(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    title = "BFET TOKEN"
    description = env.description
    payload = "Custom-Payload"
    provider_token = env.Provider_Token
    currency = "USD"
    price = int(env.price)
    prices = [LabeledPrice("Test", price * 100)]
    context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        provider_token,
        currency,
        prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
        photo_url = 'https://www.facebook.com/photo?fbid=153389103623003&set=pcb.205105318275240'
    )

def start_without_shipping_callback(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    title = env.title
    description = env.description
    payload = "Custom-Payload"
    provider_token = "284685063:TEST:Y2M0NjQxZjUwY2Vm"
    currency = "USD"
    price = env.price
    prices = [LabeledPrice("BFET_PRICE", price * 100)]
    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices,photo_url = 'https://bfet.io/assets/assets2/images/salvia/gfx-j.png'
        ,photo_width=600, 
        photo_height=400, 
    )

def shipping_callback(update: Update, context: CallbackContext) -> None:
    query = update.shipping_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
        return
    options = [ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)])]
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)

def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)
# finally, after contacting the payment provider...
def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    update.message.reply_text("Thank you for your payment!")

def main() -> None:
 
    updater = Updater(env.API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'💲BuyTokens'), start_without_shipping_callback))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'📈About'), about))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'🧰Support'), support))
    # dispatcher.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    dispatcher.add_handler(CommandHandler("noshipping", start_without_shipping_callback))
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
    updater.start_polling()


if __name__ == '__main__':
    main()

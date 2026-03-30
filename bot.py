import telebot
import whois

# التوكن الخاص بك الذي أرسلته في الصورة
API_TOKEN = '8765623443:AAEJr8dT35qMNA7R-G57hr1IpQWvLQpNlt4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "اهلا بك في بوت فحص الدومينات! 🌐\n\n"
        "أرسل لي اسم الدومين الذي تريد فحصه (مثلاً: google.com) "
        "وسأخبرك إذا كان متاحاً للتسجيل أم لا."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def check_domain(message):
    domain = message.text.strip()
    
    # التأكد أن المستخدم أرسل نصاً صالحاً
    if "." not in domain:
        bot.reply_to(message, "يرجى إرسال اسم دومين صحيح (مثال: mysite.com)")
        return

    msg = bot.reply_to(message, f"جاري فحص الدومين: {domain} ...")
    
    try:
        w = whois.whois(domain)
        
        # إذا وجد معلومات في الـ WHOIS يعني الدومين محجوز
        if w.domain_name:
            bot.edit_message_text(f"❌ الدومين {domain} محجوز مسبقاً وغير متاح.", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text(f"✅ مبروك! الدومين {domain} متاح للتسجيل الآن.", message.chat.id, msg.message_id)
            
    except Exception as e:
        # في حال لم يجد الدومين في قاعدة البيانات غالباً يكون متاحاً
        bot.edit_message_text(f"✅ الدومين {domain} يبدو متاحاً للتسجيل (لم يتم العثور على بيانات مالك).", message.chat.id, msg.message_id)

# تشغيل البوت
print("Bot is running...")
bot.polling()

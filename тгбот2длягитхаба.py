import telebot
import math
import matplotlib.pyplot as plt
import io
b=telebot.TeleBot("8559828609:AAGDbp4AkcdpZDzgRRDGfInQe9dqAMJeLPY")
s={"воздух":1,"вода":1.33,"стекло":1.5}
@b.message_handler(commands=['start'])
def s1(m):
    t="я бот для расчета углов.\n\n"
    t+="команды:\n"
    t+="/calc - ручной ввод n\n"
    t+="/sreda - выбрать среду\n"
    t+="/help - помощь\n"
    b.send_message(m.chat.id,t)
@b.message_handler(commands=['help'])
def h(m):
    t="формула: sin(α)/n = sin(β)\n\n"
    t+="команды:\n"
    t+="/start - начало\n"
    t+="/calc - ввести n\n"
    t+="/sreda - воздух/вода/стекло\n"
    t+="/help - это\n\n"
    t+="отправка картинки с подписями"
    b.send_message(m.chat.id,t)
@b.message_handler(commands=['sreda'])
def s2(m):
    t="выбери среду:\n"
    t+="воздух (n=1)\n"
    t+="вода (n=1.33)\n"
    t+="стекло (n=1.5)\n\n"
    t+="напиши название"
    b.send_message(m.chat.id,t)
    b.register_next_step_handler(m,g1)
@b.message_handler(commands=['calc'])
def c(m):
    b.send_message(m.chat.id,"введи n:")
    b.register_next_step_handler(m,g2)
def g1(m):
    a=m.text.lower()
    if a in s:
        n=s[a]
        b.send_message(m.chat.id,f"{a}, n={n}")
        b.send_message(m.chat.id,"введи угол (0-90°):")
        b.register_next_step_handler(m,g3,n)
    else:
        b.send_message(m.chat.id,"нет такой /sreda")
def g2(m):
    p=m.text
    if p.replace('.','').isdigit():
        n=float(p)
        if n>1:
            b.send_message(m.chat.id,f"n={n} введи угол (0-90°):")
            b.register_next_step_handler(m,g3,n)
        else:
            b.send_message(m.chat.id,"n>1 /calc или /sreda")
    else:
        b.send_message(m.chat.id,"это не число /calc или /sreda")
def g3(m,n):
    u=m.text
    if u.replace('.','').isdigit():
        u=float(u)
        if 0<=u<90:
            r=math.radians(u)
            su=math.sin(r)
            sb=su/n
            if sb<=1:
                br=math.asin(sb)
                bd=math.degrees(br)
                b.send_message(m.chat.id,f"угол: {bd:.1f}°")
                r1(u,bd,n,m.chat.id)
            else:
                b.send_message(m.chat.id,"полное отражение угла")
        else:
            b.send_message(m.chat.id,"угол 0-90 /calc или /sreda")
    else:
        b.send_message(m.chat.id,"это не число /calc или /sreda")
def r1(u1,u2,n,i):
    f,a=plt.subplots(figsize=(6,4))
    a.axvline(x=0,color='black',linewidth=2)
    a.text(-0.5,0.2,'воздух',fontsize=10,ha='center')
    a.text(0.5,0.2,'среда',fontsize=10,ha='center')
    a.text(0,-0.1,f'n={n}',fontsize=10,ha='center')
    r1=math.radians(u1)
    r2=math.radians(u2)
    x1=[-2,0]
    y1=[0-2*math.tan(r1),0]
    x2=[0,2]
    y2=[0,0+2*math.tan(r2)]
    a.plot(x1,y1,'b-',linewidth=2,label='падающий')
    a.plot(x2,y2,'r-',linewidth=2,label='преломленный')
    a.plot([0,0.5],[0,0],'b--',alpha=0.3)
    a.plot([0,-0.5],[0,0],'r--',alpha=0.3)
    a.text(-0.8,0.3,f'α={u1:.0f}°',fontsize=10,color='blue')
    a.text(0.3,0.3,f'β={u2:.0f}°',fontsize=10,color='red')
    a.set_xlim(-2.5,2.5)
    a.set_ylim(-1,1.5)
    a.set_aspect('equal')
    a.grid(True,alpha=0.3)
    a.legend()
    a.set_title('преломление луча')
    buf=io.BytesIO()
    plt.savefig(buf,format='png',dpi=100,bbox_inches='tight')
    buf.seek(0)
    plt.close()
    b.send_photo(i,buf)
@b.message_handler(func=lambda m:True)
def all(m):
    t=m.text.lower()
    if t in ['считать','посчитать','расчет']:
        b.send_message(m.chat.id,"используй /calc или /sreda")
    else:
        b.send_message(m.chat.id,"не понимаю /help")
print("Бот работает...")
b.polling()

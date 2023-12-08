from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage  
bot = Bot('6319667368:AAGSv3Ubta2VSXzl_x-jA4rReyizf4S249g')
dp = Dispatcher(bot, storage=MemoryStorage())   
from sql import SQL   
from googleSheet import GoogleSheet 
class Form(StatesGroup):
    begin=State()
    reg=State()
    accCreate=State()
    signIn=State()
    checkPass=State()
    auth=State()
    checkNewTab=State()
    askBal=State()
    getBal=State()
    typesCat=State()
    cat=State()
    getCat=State()
    getAnCat=State()
    checkCatEx=State()
    catCreate=State()
    afterOper=State()
    oper=State()
    getOper=State()
    availCat=State()
    askSumm=State()
    getSumm=State()
sql=SQL('My_money.sql','users')
gs=GoogleSheet('creds_4.json')
@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    columns='id varchar(50), pass varchar(50), link varchar(150), infForBot varchar(150), link2 varchar(150)'
    sql.create(columns)
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Начать работу',callback_data='начать'))
    msFromBot=await message.answer('Привет, мой друг! Я ваш помощник по ведению финансового учёта',reply_markup=markup)
    result=sql.select('*','id',str(message.from_user.id))
    if result:
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(message.from_user.id),4,str(idOfMesToDel))
    else:
        idOfMesToDel=msFromBot.message_id
        sql.insert('id,infForBot',"'%s','%s'"%(str(message.from_user.id),("3/3///"+str(idOfMesToDel))))
    await Form.begin.set()
@dp.callback_query_handler(state=Form.begin)
async def begin(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if sql.getInfForBot(str(call.from_user.id),1)!='3':
        spreadsheetId=sql.select('*','id',str(call.from_user.id))[0][2][31:]
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Авторизоваться',callback_data=f'авторизация'))
        msFromBot=await call.message.answer('Вы уже есть в базе данных',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.signIn.set()
    else:
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Зарегистрироваться',callback_data='зарегистрироваться'))
        msFromBot=await call.message.answer('Вас ещё нет в базе данных. Зарегистрируйтесь!',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.reg.set()
@dp.callback_query_handler(state=Form.reg)
async def askingForPassword(call):
    idOfMesToDel=int(sql.getInfForBot(str(call.from_user.id),4))
    await bot.delete_message(call.from_user.id,idOfMesToDel)
    await call.message.answer('Придумайте и введите пароль\n\nP.S. Пароль должен представлять собой набор символов. Если вы введёте пароль любого другого формата, он будет игнорироваться')
    decoratorInput="accCreate"
    sql.changeInfForBot(str(call.from_user.id),3,decoratorInput)
    await Form.accCreate.set()
@dp.message_handler(state=Form.accCreate)
async def accountCreate(message:types.Message):
    if sql.getInfForBot(str(message.from_user.id),3)=="accCreate":
        decoratorInput=""
        sql.changeInfForBot(str(message.from_user.id),3,decoratorInput)
        password=message.text.strip() 
        spreadsheetId=gs.createTable()
        spreadsheetId2=gs.createTable()
        gs.updateData(spreadsheetId,"Лист номер один!A1:B2",[['Баланс','Статус категории'],['','Дата/Категория']])
        gs.widthOfColumn(spreadsheetId,2,len('Статус категории'))
        linker='https://docs.google.com/file/d/'+spreadsheetId
        linker2='https://docs.google.com/file/d/'+spreadsheetId2
        sql.update('pass',"'%s'"%(password),'id',str(message.from_user.id))
        sql.update('link',"'%s'"%(linker),'id',str(message.from_user.id))
        sql.update('link2',"'%s'"%(linker2),'id',str(message.from_user.id))
        await message.answer('Регистрация пройдена!')
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Авторизоваться',callback_data=f'авторизация'))
        msFromBot=await message.answer('Вы можете войти в систему',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(message.from_user.id),4,str(idOfMesToDel))
        await Form.signIn.set()
@dp.callback_query_handler(state=Form.signIn)
async def askingForPassword(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    await call.message.answer('Введите пароль\n\nP.S. Пароль должен представлять собой набор символов. Если вы введёте пароль любого другого формата, он будет игнорироваться')
    decoratorInput="checkPass"
    sql.changeInfForBot(str(call.from_user.id),3,decoratorInput)
    await Form.checkPass.set()
@dp.message_handler(state=Form.checkPass)
async def checkingOfPassword(message:types.Message):
    if sql.getInfForBot(str(message.from_user.id),3)=="checkPass":
        decoratorInput=""
        sql.changeInfForBot(str(message.from_user.id),3,decoratorInput)
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Войти',callback_data=f'{str(message.text.strip())}'))
        msFromBot=await message.answer('Ваш пароль принят. Попробуйте войти в систему',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(message.from_user.id),4,str(idOfMesToDel))
        await Form.auth.set()
@dp.callback_query_handler(state=Form.auth)
async def authorization(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if call.data==sql.select('pass','id',str(call.from_user.id))[0][0]:
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Проверить данные',callback_data="проверить"))
        await call.message.answer('Добро пожаловать!')
        msFromBot=await call.message.answer('Перед началом работы необходимо проверить данные на существование',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.checkNewTab.set()
    else:
        await call.message.answer('Неверный пароль. Попробуйте ещё раз')
        decoratorInput="checkPass"
        sql.changeInfForBot(str(call.from_user.id),3,decoratorInput)
        await Form.checkPass.set()
@dp.callback_query_handler(state=Form.checkNewTab)
async def checkingOfNewTable(call):
    spreadsheetId=sql.select('link','id',str(call.from_user.id))[0][0][31:]
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if gs.getData(spreadsheetId,"Лист номер один!A2")=="No data found.":
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перейти к оформлению',callback_data="оформление"))
        msFromBot=await call.message.answer('Отсутствует какая-либо информация о ваших финансах. Необходимо оформление данных',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.askBal.set()
    else:
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перейти к общим операциям',callback_data="общте опреации"))
        msFromBot=await call.message.answer('Данные найдены. Вы можете перейти к общим операциям',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))    
        await Form.oper.set()
@dp.callback_query_handler(state=Form.askBal)
async def askingForBalance(call):
    spreadsheetId=sql.select('link','id',str(call.from_user.id))[0][0][31:]
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    await call.message.answer('Напишите ваш нынешний баланс\n\nP.S. Баланс является числовым значением, не начинающимся с 0. Если вы введёте баланс любого другого формата, он будет игнорироваться')
    decoratorInput="getBal"
    sql.changeInfForBot(str(call.from_user.id),3,decoratorInput)
    await Form.getBal.set()
@dp.message_handler(state=Form.getBal)
async def gettingOfBalance(message:types.Message):
    spreadsheetId=sql.select('link','id',str(message.from_user.id))[0][0][31:]
    if sql.getInfForBot(str(message.from_user.id),3)=="getBal":
        flag=1
        for i in range(len(str(message.text.strip()))):
            flag*=str(message.text.strip())[i].isdigit()
        if flag==1 and (str(message.text.strip())[0]!="0" or len(str(message.text.strip()))==1):
            decoratorInput=""
            sql.changeInfForBot(str(message.from_user.id),3,decoratorInput)
            balance=[[str(message.text.strip())]]
            gs.updateData(spreadsheetId,"Лист номер один!A2",balance)
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Типы категорий',callback_data="типы категоий"))
            await message.answer('Ваш нынешний баланс установлен')
            msFromBot=await message.answer('Следующим шагом оформления является выбор категорий ваших расходов и доходов. Необходимо перейти к типам категорий',reply_markup=markup)
            idOfMesToDel=msFromBot.message_id
            sql.changeInfForBot(str(message.from_user.id),4,str(idOfMesToDel)) 
            await Form.typesCat.set()
@dp.callback_query_handler(state=Form.typesCat)
async def typesOfCategories(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    markup=types.InlineKeyboardMarkup(row_width=2)
    btn1=types.InlineKeyboardButton('Категории расходов', callback_data='категории расходов')
    btn2=types.InlineKeyboardButton('Категории доходов', callback_data='категории доходов')
    markup.add(btn1,btn2)
    msFromBot=await call.message.answer("Выберите тип категорий",reply_markup=markup)
    idOfMesToDel=msFromBot.message_id
    sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel)) 
    await Form.cat.set()
@dp.callback_query_handler(state=Form.cat)
async def categories(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if call.data=='категории расходов':
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn1=types.InlineKeyboardButton('Продукты', callback_data='1Продукты')
        btn2=types.InlineKeyboardButton('Коммунальные и кредитные платежи', callback_data='1Коммунальные и кредитные платежи')
        btn3=types.InlineKeyboardButton('Транспорт', callback_data='1Транспорт')
        btn4=types.InlineKeyboardButton('Образование', callback_data='1Образование')
        btn5=types.InlineKeyboardButton('Медицина', callback_data='1Медицина')
        btn6=types.InlineKeyboardButton('Другое', callback_data='1Другое')
        markup.add(btn1,btn2,btn3,btn4,btn5,btn6)
        msFromBot=await call.message.answer("Выберите категорию расходов",reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel)) 
        await Form.getCat.set()
    if call.data=='категории доходов':
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn1=types.InlineKeyboardButton('Зарплата', callback_data='2Зарплата')
        btn2=types.InlineKeyboardButton('Другое', callback_data='2Другое')
        markup.add(btn1,btn2)
        msFromBot=await call.message.answer("Выберите категорию доходов",reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel)) 
        await Form.getCat.set()
@dp.callback_query_handler(state=Form.getCat)
async def gettingCategory(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if call.data[1:]!='Другое':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Проверить категорию',callback_data=call.data))
        msFromBot=await call.message.answer(f'Необходимо проверить категорию "{call.data[1:]}" на существование',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel)) 
        await Form.checkCatEx.set()
    else:
        nameOfCategory=call.data
        sql.changeInfForBot(str(call.from_user.id),2,nameOfCategory)
        await call.message.answer("Напишите название категории")
        decoratorInput="getAnCat"
        sql.changeInfForBot(str(call.from_user.id),3,decoratorInput)
        await Form.getAnCat.set()
@dp.message_handler(state=Form.getAnCat)
async def gettingAnotherCategory(message:types.Message):
    if sql.getInfForBot(str(message.from_user.id),3)=="getAnCat":
        decoratorInput=""
        sql.changeInfForBot(str(message.from_user.id),3,decoratorInput)
        nameOfCategory=sql.getInfForBot(str(message.from_user.id),2)
        nameOfCategory=nameOfCategory[0]+message.text.strip()
        sql.changeInfForBot(str(message.from_user.id),2,nameOfCategory)
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Проверить категорию',callback_data=nameOfCategory))
        msFromBot=await message.answer(f'Необходимо проверить категорию "{nameOfCategory[1:]}" на существование',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(message.from_user.id),4,str(idOfMesToDel))
        await Form.checkCatEx.set()
@dp.callback_query_handler(state=Form.checkCatEx)
async def checkingIfCategoryExists(call):
    spreadsheetId=sql.select('link','id',str(call.from_user.id))[0][0][31:]
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    numberOfColumns=int(sql.getInfForBot(str(call.from_user.id),1))-1
    if not(call.data[1:] in gs.getData(spreadsheetId,"Лист номер один!B2:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"3").get('values',[])[0]):
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f'Создать категорию "{call.data[1:]}"',callback_data=call.data))
        msFromBot=await call.message.answer("Такой категории ещё не существует. Вы можете создать её",reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.catCreate.set()
    else:
        markup=types.InlineKeyboardMarkup()
        btn1=types.InlineKeyboardButton('Создать другую категорию', callback_data='создать категорию')
        markup.row(btn1)
        btn2=types.InlineKeyboardButton('Общие операции', callback_data='операции')
        markup.row(btn2)
        msFromBot=await call.message.answer("Такая категория уже существует. Выберите для создания другую категорию или перейдите к общим опреациям",reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.afterOper.set()
@dp.callback_query_handler(state=Form.catCreate)
async def categoryCreate(call):
    spreadsheetId=sql.select('link','id',str(call.from_user.id))[0][0][31:]
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if call.data[0]=="2":
        status="Доход"
        gs.createColumnOrRow(spreadsheetId,'COLUMNS',2)
        sql.changeInfForBot(str(call.from_user.id),1,str(int(sql.getInfForBot(str(call.from_user.id),1))+1))
        if len(call.data)>14:
            gs.widthOfColumn(spreadsheetId,3,len(call.data)-1)
        gs.updateData(spreadsheetId,"Лист номер один!C1:C2",[[status],[call.data[1:]]])
    else:
        status="Расход"
        numberOfColumns=int(int(sql.getInfForBot(str(call.from_user.id),1)))-1
        gs.createColumnOrRow(spreadsheetId,'COLUMNS',numberOfColumns)
        sql.changeInfForBot(str(call.from_user.id),1,str(int(numberOfColumns)+2))
        if len(call.data)>14:
            gs.widthOfColumn(spreadsheetId,numberOfColumns+1,len(call.data)-1)
        gs.updateData(spreadsheetId,"Лист номер один!"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"2",[[status],[call.data[1:]]])
    markup=types.InlineKeyboardMarkup(row_width=1)
    btn1=types.InlineKeyboardButton('Создать ещё одну категорию', callback_data='создать категорию')
    btn2=types.InlineKeyboardButton('Общие операции', callback_data='операции')
    markup.add(btn1,btn2)
    msFromBot=await call.message.answer("Категория создана",reply_markup=markup)
    idOfMesToDel=msFromBot.message_id
    sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
    await Form.afterOper.set()
@dp.callback_query_handler(state=Form.afterOper)
async def afterOperation(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if call.data=='создать категорию':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Типы категорий',callback_data="типы категоий"))
        msFromBot=await call.message.answer('Необходимо выбрать категории данных',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.typesCat.set()
    else:
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Список общих операций',callback_data="общие операции"))
        msFromBot=await call.message.answer('Необходимо перейти к списку общих операций',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.oper.set()
@dp.callback_query_handler(state=Form.oper)
async def operations(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    markup=types.InlineKeyboardMarkup(row_width=1)
    btn1=types.InlineKeyboardButton('Текущий баланс', callback_data='баланс')
    btn2=types.InlineKeyboardButton('Новые доходы/расходы', callback_data='доходы/расходы')
    btn3=types.InlineKeyboardButton('Создать категорию', callback_data='категория')
    btn4=types.InlineKeyboardButton('Отчёт за сегодня', callback_data='сегодня')
    btn5=types.InlineKeyboardButton('Отчёт за последние внесённые 3 дня', callback_data='последние 3 дня')
    btn6=types.InlineKeyboardButton('Отчёт за этот месяц', callback_data='месяц')
    btn7=types.InlineKeyboardButton('Отчёт за всё время (таблица)', callback_data='таблица')
    btn8=types.InlineKeyboardButton('Выйти из системы', callback_data='выход')
    markup.add(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8)
    msFromBot=await call.message.answer("Выберите операцию",reply_markup=markup)
    idOfMesToDel=msFromBot.message_id
    sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
    await Form.getOper.set()
@dp.callback_query_handler(state=Form.getOper)
async def gettingOperation(call):
    spreadsheetId=sql.select('link','id',str(call.from_user.id))[0][0][31:]
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    if call.data=='баланс':
        numberOfRows=int(int(sql.getInfForBot(str(call.from_user.id),0)))-1
        balance=gs.getData(spreadsheetId,"Лист номер один!A"+str(numberOfRows)).get('values',[])[0][0]
        await call.message.answer(f'Баланс = {balance}')
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Общие операции', callback_data='операции'))
        msFromBot=await call.message.answer('Вы можете вернуться к общим операциям',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.afterOper.set()
    elif call.data=='доходы/расходы':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Открыть список доступных категорий',callback_data="доступные категории"))
        msFromBot=await call.message.answer('Необходимо перейти к списку категорий, доступных для весения данных о новых доходах и расходах',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.availCat.set()
    elif call.data=='категория':
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Типы категорий',callback_data="типы категоий"))
        msFromBot=await call.message.answer('Необходимо выбрать категории данных',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.typesCat.set()
    elif call.data=='сегодня':
        date=call.message.date.strftime("%d.%m.%Y")
        numberOfRows=int(int(sql.getInfForBot(str(call.from_user.id),0)))-1
        numberOfColumns=int(int(sql.getInfForBot(str(call.from_user.id),1)))-1
        dateWithСategoriesWithSum=str(date)
        sumOfPlus=0
        sumOfMinus=0
        if gs.getData(spreadsheetId,"Лист номер один!B"+str(numberOfRows)).get('values',[])[0][0]!=date:
            await call.message.answer('Сегодня вы не вносили никаких данных о новых доходах/расходах')
        else:
            await call.message.answer('Отчёт за сегодня')
            categories=gs.getData(spreadsheetId,"Лист номер один!C1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"2").get('values',[])
            summs=gs.getData(spreadsheetId,"Лист номер один!C"+str(numberOfRows)+":"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+str(numberOfRows)).get('values',[])[0]
            for i in range(len(summs)):
                if summs[i]!="":
                    dateWithСategoriesWithSum+="\n"+categories[1][i]+" ("+categories[0][i]+"): "+summs[i]
                    if categories[0][i]=="Доход":
                        sumOfPlus+=int(summs[i])
                    else:
                        sumOfMinus+=int(summs[i])
            await call.message.answer(dateWithСategoriesWithSum+"\n\n"+"Сумма доходов: "+str(sumOfPlus)+"\n"+"Сумма расходов: "+str(sumOfMinus)+"\n\n"+"Общеее изменение баланса: "+str(sumOfPlus-sumOfMinus))
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Общие операции', callback_data='операции'))
        msFromBot=await call.message.answer('Вы можете вернуться к общим операциям',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.afterOper.set()
    elif call.data=='последние 3 дня':
        numberOfRows=int(int(sql.getInfForBot(str(call.from_user.id),0)))-1
        numberOfColumns=int(int(sql.getInfForBot(str(call.from_user.id),1)))-1
        if numberOfRows==2:
            await call.message.answer('Отсутствуют какие либо данные о новых доходах/расходах за последнее время')
        elif numberOfRows<5:
            await call.message.answer('Данные о новых доходах/расходах за всё последнее время:')
            result=gs.getData(spreadsheetId,"Лист номер один!B1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+f"{numberOfRows}").get('values',[])
            for i in range(numberOfRows-2):
                dateWithСategoriesWithSum=result[2+i][0]
                sumOfPlus=0
                sumOfMinus=0
                categories=result[:2]
                summs=result[2+i]
                for j in range(1,len(summs)):
                    if summs[j]!="":
                        dateWithСategoriesWithSum+="\n"+categories[1][j]+" ("+categories[0][j]+"): "+summs[j]
                        if categories[0][j]=="Доход":
                            sumOfPlus+=int(summs[j])
                        else:
                            sumOfMinus+=int(summs[j])
                await call.message.answer(dateWithСategoriesWithSum+"\n\n"+"Сумма доходов: "+str(sumOfPlus)+"\n"+"Сумма расходов: "+str(sumOfMinus)+"\n\n"+"Общеее изменение баланса: "+str(sumOfPlus-sumOfMinus))
        else:
            await call.message.answer('Отчёт за последние внесённые 3 дня')
            result=gs.getData(spreadsheetId,"Лист номер один!B"+str(numberOfRows-2)+":"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+f"{numberOfRows}").get('values',[])
            for i in range(3):
                dateWithСategoriesWithSum=result[i][0]
                sumOfPlus=0
                sumOfMinus=0
                categories=gs.getData(spreadsheetId,"Лист номер один!C1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"2").get('values',[])
                summs=result[i][1:]
                for j in range(len(summs)):
                    if summs[j]!="":
                        dateWithСategoriesWithSum+="\n"+categories[1][j]+" ("+categories[0][j]+"): "+summs[j]
                        if categories[0][j]=="Доход":
                            sumOfPlus+=int(summs[j])
                        else:
                            sumOfMinus+=int(summs[j])
                await call.message.answer(dateWithСategoriesWithSum+"\n\n"+"Сумма доходов: "+str(sumOfPlus)+"\n"+"Сумма расходов: "+str(sumOfMinus)+"\n\n"+"Общеее изменение баланса: "+str(sumOfPlus-sumOfMinus))
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Общие операции', callback_data='операции'))
        msFromBot=await call.message.answer('Вы можете вернуться к общим операциям',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.afterOper.set()
    elif call.data=='месяц':
        await call.message.answer('Отчёт за этот месяц')
        month=call.message.date.strftime("%d.%m.%Y").split(".")[1]
        numberOfRows=int(int(sql.getInfForBot(str(call.from_user.id),0)))-1
        numberOfColumns=int(int(sql.getInfForBot(str(call.from_user.id),1)))-1
        summOfEachCategory=[0]*(numberOfColumns-2) 
        sumOfPlus=0
        sumOfMinus=0
        answer=f"Доходы/расходы за {month} месяц\n"
        if numberOfRows<33:
            result=gs.getData(spreadsheetId,"Лист номер один!B1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+f"{numberOfRows}").get('values',[])
            categories=result[:2]
            dateWithSumms=result[2:]
            for i in range(numberOfRows-2):
                if dateWithSumms[i][0].split(".")[1]==month:
                    for j in range(1,len(dateWithSumms[i])):
                        if dateWithSumms[i][j]!="":
                            summOfEachCategory[j-1]+=int(dateWithSumms[i][j])
                            if categories[0][j]=="Доход":
                                sumOfPlus+=int(dateWithSumms[i][j])
                            else:
                                sumOfMinus+=int(dateWithSumms[i][j])
            for i in range(len(summOfEachCategory)):
                if summOfEachCategory[i]!=0:
                    answer+=categories[1][i+1]+" ("+categories[0][i+1]+"): "+str(summOfEachCategory[i])+"\n"
        else:
            result=gs.getData(spreadsheetId,"Лист номер один!B"+str(numberOfRows-30)+":"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+f"{numberOfRows}").get('values',[])
            categories=gs.getData(spreadsheetId,"Лист номер один!C1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"2").get('values',[])
            dateWithSumms=result
            for i in range(numberOfRows-2):
                if dateWithSumms[i][0].split(".")[1]==month:
                    for j in range(1,len(dateWithSumms[i])):
                        if dateWithSumms[i][j]!="":
                            summOfEachCategory[j-1]+=int(dateWithSumms[i][j])
                            if categories[0][j-1]=="Доход":
                                sumOfPlus+=int(dateWithSumms[i][j])
                            else:
                                sumOfMinus+=int(dateWithSumms[i][j])
            for i in range(len(summOfEachCategory)):
                if summOfEachCategory[i]!=0:
                    answer+=categories[1][i]+" ("+categories[0][i]+"): "+str(summOfEachCategory[i])+"\n"
        if answer==f"Доходы/расходы за {month} месяц\n":
            await call.message.answer('Отсутствуют какие либо данные о новых доходах/расходах в этом месяце')
        else:
            await call.message.answer(answer+"\n"+"Сумма доходов: "+str(sumOfPlus)+"\n"+"Сумма расходов: "+str(sumOfMinus)+"\n\n"+"Общеее изменение баланса: "+str(sumOfPlus-sumOfMinus))
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Общие операции', callback_data='операции'))
        msFromBot=await call.message.answer('Вы можете вернуться к общим операциям',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.afterOper.set()
    elif call.data=='таблица':
        spreadsheetId2=sql.select('link2','id',str(call.from_user.id))[0][0][31:]
        gs.copyList(spreadsheetId,spreadsheetId2)
        gs.deleteList(spreadsheetId2,gs.sheet_id(spreadsheetId2))
        markup=types.InlineKeyboardMarkup()
        btn1=types.InlineKeyboardButton('Таблица',url=sql.select('link2','id',str(call.from_user.id))[0][0])
        btn2=types.InlineKeyboardButton('Общие операции', callback_data='операции')
        markup.add(btn1,btn2)
        msFromBot=await call.message.answer('Вы можете перейти к таблице по ссылке и/или вернуться к общим операциям',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.afterOper.set()
    elif call.data=='выход':
        await call.message.answer('Вы вышли из системы')
        markup=types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Начать работу', callback_data='начать'))
        msFromBot=await call.message.answer('Для того, чтобы снова войти в систему, её необходимо презапустить',reply_markup=markup)
        idOfMesToDel=msFromBot.message_id
        sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
        await Form.begin.set()
@dp.callback_query_handler(state=Form.availCat)
async def availableCategories(call):
    spreadsheetId=sql.select('link','id',str(call.from_user.id))[0][0][31:]
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    numberOfColumns=int(int(sql.getInfForBot(str(call.from_user.id),1)))-1
    result=gs.getData(spreadsheetId,"Лист номер один!C1:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"2").get('values',[])
    markup=types.InlineKeyboardMarkup()
    for i in range(numberOfColumns-2):
        typeOfCategory="1"
        if result[0][i]=="Доход":
            typeOfCategory="2"
        markup.add(types.InlineKeyboardButton(f'{result[1][i]} ({result[0][i]})', callback_data=f'{typeOfCategory}{result[1][i]}'))
    msFromBot=await call.message.answer("Выберите одну из доступных категорий",reply_markup=markup)
    idOfMesToDel=msFromBot.message_id
    sql.changeInfForBot(str(call.from_user.id),4,str(idOfMesToDel))
    await Form.askSumm.set()
@dp.callback_query_handler(state=Form.askSumm)
async def askingForSumma(call):
    await bot.delete_message(call.from_user.id,int(sql.getInfForBot(str(call.from_user.id),4)))
    nameOfCategory=call.data
    sql.changeInfForBot(str(call.from_user.id),2,nameOfCategory)
    await call.message.answer('Напишите сумму (числовое значение изменения баланса по выбранной категории)\n\nP.S. Сумма является числовым значением, не начинающимся с 0. Если вы введёте сумму в любом другом формате, она будет игнорироваться')
    decoratorInput="getSumm"
    sql.changeInfForBot(str(call.from_user.id),3,decoratorInput)
    await Form.getSumm.set()
@dp.message_handler(state=Form.getSumm)
async def gettingOfSumma(message:types.Message):
    spreadsheetId=sql.select('link','id',str(message.from_user.id))[0][0][31:]
    if sql.getInfForBot(str(message.from_user.id),3)=="getSumm":
        flag=1
        for i in range(len(str(message.text.strip()))):
            flag*=str(message.text.strip())[i].isdigit()
        if flag==1 and (str(message.text.strip())[0]!="0" or len(str(message.text.strip()))==1):
            decoratorInput=""
            sql.changeInfForBot(str(message.from_user.id),3,decoratorInput)
            summa=str(message.text.strip())
            date=message.date.strftime("%d.%m.%Y")
            numberOfRows=int(sql.getInfForBot(str(message.from_user.id),0))-1
            numberOfColumns=int(sql.getInfForBot(str(message.from_user.id),1))-1
            nameOfCategory=sql.getInfForBot(str(message.from_user.id),2)
            if nameOfCategory[0]=="1":
                summa="-"+summa
            else:
                summa="+"+summa
            balance=int(gs.getData(spreadsheetId,"Лист номер один!A"+str(numberOfRows)).get('values',[])[0][0])
            if summa[0]=="-":
                balance-=int(summa[1:])
            else:
                balance+=int(summa[1:])
            index=gs.getData(spreadsheetId,"Лист номер один!C2:"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[numberOfColumns]+"2").get('values',[])[0].index(nameOfCategory[1:])+2
            if gs.getData(spreadsheetId,"Лист номер один!B"+str(numberOfRows)).get('values',[])[0][0]!=date:
                gs.createColumnOrRow(spreadsheetId,'ROWS',numberOfRows)
                sql.changeInfForBot(str(message.from_user.id),0,str(numberOfRows+2))
                gs.updateData(spreadsheetId,"Лист номер один!B"+str(numberOfRows+1),[[date]])
                numberOfRows+=1
            if gs.getData(spreadsheetId,"Лист номер один!"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[index]+str(numberOfRows))=="No data found.":
                lastSumma=0
            else:
                lastSumma=int(gs.getData(spreadsheetId,"Лист номер один!A"+str(numberOfRows)).get('values',[])[0][0][1:])
            newSumma=lastSumma+int(summa[1:])
            gs.updateData(spreadsheetId,"Лист номер один!"+"ABCDEFGHIJKLMNOPQRSTUVYXYZ"[index]+str(numberOfRows),[[newSumma]])
            gs.updateData(spreadsheetId,"Лист номер один!A"+str(numberOfRows),[[balance]])
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Общие операции', callback_data='операции'))
            await message.answer(f'Операция по внесению новых данных в категорию "{nameOfCategory[1:]}" выполнена!')
            msFromBot=await message.answer('Вы можете вернуться к общим операциям',reply_markup=markup)
            idOfMesToDel=msFromBot.message_id
            sql.changeInfForBot(str(message.from_user.id),4,str(idOfMesToDel))
            await Form.afterOper.set()
executor.start_polling(dp)
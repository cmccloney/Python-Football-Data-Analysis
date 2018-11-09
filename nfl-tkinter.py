import requests #used for scraping web pages
from bs4 import BeautifulSoup #BeautifulSoup is a Python library helping with using HTML pages
                              #https://www.crummy.com/software/BeautifulSoup/
import tkinter      #used for GUI
from datetime import datetime
import pandas #used for data frames and data analysis
import matplotlib
import matplotlib.pyplot as plt #provides MATLAB-like plotting framework
                                #https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
matplotlib.use("TkAgg")
from matplotlib.figure import Figure  #use these two to print plots in Tkinter GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
date = str(datetime.now())
year = date[0:4]
month = date[5:7]
day = date[8:10]

class Page(tkinter.Frame): #pages instead of scrollbar
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
    def figure(self,df,df2,name,num):
       count = len(df2['Salary'])
       df['Age'] = pandas.to_numeric(df['Age'], errors='coerce') #convert to float
       df.fillna({'Age':0}, inplace=True) #replace NA values
       df['Age'] = df['Age'].astype(int)
       df.sort_values(by=['Age']) #sort numerically
       df2['Age'] = pandas.to_numeric(df2['Age'], errors='coerce') #convert to float
       df2.fillna({'Age':0}, inplace=True) #replace NA values
       df2['Age'] = df2['Age'].astype(int)
       df2.sort_values(by=['Age']) #sort numerically
       if(num == 0):
           statement = "There are " + str(count) + " players on the " + str(name).replace('_',' ') + " making over $1,000,000."
           label = tkinter.Label(self, text=statement) #recent loss
           label.pack()

       fig = Figure(figsize=(100,100), dpi=100) #this part and below displays histogram of
                                        #salaries in Tkinter GUI
       if(num == 0): #display salary hist
           p = fig.gca()
           p.hist(df['Salary'],bins=25)
           p.set_xlabel('Salary (in $10,000,000s)', fontsize = 14)
           p.set_ylabel('Number of Players', fontsize = 14)
           p.set_title("Salary by Number of Players of " + str(name).replace('_',' '), fontsize = 16)
       else: #display age by salary
           p = fig.gca()
           p.scatter(df['Age'],df['Salary'])
           p.set_xlim([18,60])
           p.set_xlabel('Age', fontsize = 14)
           p.set_ylabel('Salary', fontsize = 14)
           p.set_title("Age by Salary of " + str(name).replace('_',' '), fontsize = 16)
           
       canvas = FigureCanvasTkAgg(fig,self)
       canvas.draw()
       canvas.get_tk_widget().pack(fill="y",expand=True)
       self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

def Destroy(p1,b_frame,container,frame): #destroy previous frames and select a new team
    p1.destroy()
    b_frame.destroy()
    container.destroy()
    frame.destroy()

def __salary_stats(name,gui,frame):
    salaries_data_frame = pandas.read_csv('datasets\\nfl_salaries.csv')
    players_data_frame = pandas.read_csv('datasets\\nfl_players.csv')
    spec_teams = {'Green_Bay_Packers': 'GNB', 'Jacksonville_Jaguars' : 'JAX', 'Los_Angeles_Rams' : 'LAR',
                  'Los_Angeles_Chargers' : 'LAC', 'New_Orleans_Saints' : 'NOR', 'New_England_Patriots' : 'NWE',
                  'New_York_Giants' : 'NYG', 'New_York_Jets' : 'NYJ', 'San_Francisco_49ers' : 'SFO'}
    full_name = name[0]
    for i in range(1,len(name)):
        full_name += "_"
        full_name += name[i]
    if(full_name in spec_teams):
        team = spec_teams[full_name]
    else:
        team = full_name[0:3].upper()
    df = pandas.DataFrame(data=0,index=range(0,1),columns=['Salary','Age'])
    df_big = pandas.DataFrame(data=0,index=range(0,1),columns=['Salary','Age']) #players making more than a million
    index = 0
    for i in range(0,len(salaries_data_frame)):
        if(salaries_data_frame.loc[i,'Tm'] == team):
            df.loc[index,'Salary'] = salaries_data_frame.loc[i,'Cap Hit'][1:].replace(',','')
            temp = salaries_data_frame.loc[i,'Player'].split("\\")
            temp2 = players_data_frame[players_data_frame['Name'] == (temp[0])].values
            if(len(temp2) > 0):
                #print(temp2[0][3])
                df.loc[index,'Age'] = temp2[0][3] #3rd entry is age
            if(int(df.loc[index,'Salary']) >= 1000000):
                df_big.loc[index,'Salary'] = salaries_data_frame.loc[i,'Cap Hit'][1:].replace(',','')
                if(len(temp2) > 0):
                    df_big.loc[index,'Age'] = temp2[0][3]
                # only for player making more than a million
            index = index + 1
    df['Salary'] = df['Salary'].astype(str).astype(int) #convert to string before converting to int, from object

    p1 = Page1(gui)
    p2 = Page2(gui)
    buttonframe = tkinter.Frame(gui)
    container = tkinter.Frame(gui)
    buttonframe.pack(side="bottom", fill="x", expand=False)
    container.pack(side="top", fill="both", expand=True)
    p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
    p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
    b1 = tkinter.Button(buttonframe, text="Page 1", command=p1.lift)
    b2 = tkinter.Button(buttonframe, text="Page 2", command=p2.lift)
    b1.pack(side="left")
    b2.pack(side="left")
    b_forget = tkinter.Button(buttonframe, text="Clear Screen", command=lambda : Destroy(p1,buttonframe,container,frame))
    b_forget.pack(side="right")
    p2.figure(df,df_big,full_name,1)
    p1.figure(df,df_big,full_name,0)
            

def __games(team,gui):
        team = team.replace(' ','_')
        frame = tkinter.Frame(gui) #frame
        frame.pack()
        url1 = "https://en.wikipedia.org/wiki/2018_"
        url2 = "_season"
        url = url1 + team + url2
        page = requests.get(url)
        name = team.split("_")
        soup = BeautifulSoup(page.content, 'html.parser')
        future_weeks = soup.find_all("tr", {"style": "background:#"})
        wins = soup.find_all("tr", {"style": "background:#cfc"})
        losses = soup.find_all("tr", {"style": "background:#fcc"})
        general_info = soup.select("table.infobox tbody tr td")
        record = general_info[4].get_text().strip()
        if(future_weeks and str(team) != "Denver_Broncos"): #Only Broncos wiki page doesn't work only here, weird
            current_week = future_weeks[0].get_text().split("\n")
            current_team = current_week[7]
            current_time = current_week[5].split("\\")[0]
            current_date = current_week[3]
            statement = "The next game of the "
            for i in range(0,len(name)):
                statement += name[i] + " "
            statement += "is "
            statement += current_team
            statement += " on "
            statement += current_date
            statement += ", "
            statement += year
            statement += " at "
            statement += current_time
            statement += " ("
            statement += record + ")"
            label = tkinter.Label(frame, text=statement) #next game
            label.pack()
        if(wins):
            recent_win = wins[len(wins)-1].get_text().split("\n")
            recent_date = recent_win[3]
            recent_time = recent_win[5].split("\\")[0]
            recent_team = recent_win[7]
            recent_score = recent_win[9]
            statement2 = "The most recent win of the "
            for i in range(0,len(name)):
                statement2 += name[i] + " "
            statement2 += "was "
            statement2 += recent_team
            statement2 += " on "
            statement2 += recent_date
            statement2 += ", "
            statement2 += year
            statement2 += ": "
            statement2 += recent_score
            label2 = tkinter.Label(frame, text=statement2) #recent win
            label2.pack()
        if(losses):
            recent_loss = losses[len(losses)-1].get_text().split("\n")
            recent_date = recent_loss[3]
            recent_time = recent_loss[5].split("\\")[0]
            recent_team = recent_loss[7]
            recent_score = recent_loss[9]
            statement3 = "The most recent loss of the "
            for i in range(0,len(name)):
                statement3 += name[i] + " "
            statement3 += "was "
            statement3 += recent_team
            statement3 += " on "
            statement3 += recent_date
            statement3 += ", "
            statement3 += year
            statement3 += ": "
            statement3 += recent_score
            label3 = tkinter.Label(frame, text=statement3) #recent loss
            label3.pack()
        __salary_stats(name,gui,frame)

teams = ["Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers",
         "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos",
         "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars",
         "Kansas City Chiefs", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
         "Minnesota Vikings", "New England Patriots","New Orleans Saints","New York Giants", "New York Jets",
         "Oakland Raiders", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
         "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Redskins"]
gui = tkinter.Tk() #window
gui.geometry("1000x750")
menuFrame = tkinter.Frame(gui) #frame for menu and analysis button
menuFrame.pack()
team = tkinter.StringVar(gui)
team.set(teams[0]) #default value
menu = tkinter.OptionMenu(menuFrame, team, *teams) #drop-down menu
menu.pack()
button = tkinter.Button(menuFrame, text="Analysis",command=lambda : __games(team.get(),gui)) #button
button.pack()
gui.mainloop()
###

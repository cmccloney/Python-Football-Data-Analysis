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


def __salary_stats(name,gui):
    salaries_data_frame = pandas.read_csv('nfl_salaries.csv')
    team = name[0][0:3].upper()
    df = pandas.DataFrame(data=[0],index=range(0,1),columns=['Salary'])
    index = 0
    for i in range(0,len(salaries_data_frame)):
        if(salaries_data_frame.loc[i,'Tm'] == team):
            #print(salaries_data_frame.loc[i,:]) #print ith row, all columns
            df.loc[index,'Salary'] = salaries_data_frame.loc[i,'Cap Hit'][1:].replace(',','')
            #print(df.loc[index])
            index = index + 1
    df['Salary'] = df['Salary'].astype(str).astype(int) #convert to string before converting to int, from object
    fig = Figure(figsize=(6,4), dpi=100) #this part and below displays histogram of
                                        #salaries in Tkinter GUI
    p = fig.gca()
    p.hist(df['Salary'])
    p.set_xlabel('Salary', fontsize = 14)
    p.set_ylabel('Number of Players', fontsize = 14)
    p.set_title("Salary by Player of " + str(name[0]), fontsize = 16)
    canvas = FigureCanvasTkAgg(fig,gui)
    canvas.get_tk_widget().pack()
    canvas.draw()
            

def __games(team,gui):
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
            label = tkinter.Label(gui, text=statement) #next game
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
            label2 = tkinter.Label(gui, text=statement2) #recent win
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
            label3 = tkinter.Label(gui, text=statement3) #recent loss
            label3.pack()
        __salary_stats(name,gui)

teams = ["Arizona_Cardinals", "Atlanta_Falcons", "Baltimore_Ravens", "Buffalo_Bills", "Carolina_Panthers",
         "Chicago_Bears", "Cincinnati_Bengals", "Cleveland_Browns", "Dallas_Cowboys", "Denver_Broncos",
         "Detroit_Lions", "Green_Bay_Packers", "Houston_Texans", "Indianapolis_Colts", "Jacksonville_Jaguars",
         "Kansas_City_Chiefs", "Los_Angeles_Chargers", "Los_Angeles_Rams", "Miami_Dolphins",
         "Minnesota_Vikings", "New_England_Patriots","New_Orleans_Saints","New_York_Giants", "New_York_Jets",
         "Oakland_Raiders", "Philadelphia_Eagles", "Pittsburgh_Steelers", "San_Francisco_49ers",
         "Seattle_Seahawks", "Tampa_Bay_Buccaneers", "Tennessee_Titans", "Washington_Redskins"]
gui = tkinter.Tk() #window
gui.geometry("1000x750")
frame = tkinter.Frame(gui) #frame
frame.pack()
team = tkinter.StringVar(gui)
team.set(teams[0]) #default value
menu = tkinter.OptionMenu(gui, team, *teams) #drop-down menu
menu.pack()
button = tkinter.Button(gui, text="Analysis",command=lambda : __games(team.get(),gui)) #button
button.pack()
gui.mainloop()
###

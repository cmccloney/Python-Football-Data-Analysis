import tkinter      #used for GUI
from datetime import datetime
date = str(datetime.now())
year = date[0:4]
month = date[5:7]
day = date[8:10]
if(int(month) < 8): # ifpast season is already over, then all games occurred were last year
    temp = int(year)
    temp2 = temp-1
    year = str(temp2)

def __last_game_played(team,gui,page):
    if(team == "Seahawks"):
        soup = BeautifulSoup(page.content, 'html.parser')
        past_scores = soup.find_all("span", {"class": "nfl-o-matchup-cards__score--points"})
        past_results = soup.find_all("span", {"class": "nfl-o-matchup-cards__score--result"})
        past_teams = soup.find_all("p", {"class": "nfl-o-matchup-cards__team-full-name"})
        past_dates = soup.find_all("span", {"class": "nfl-o-matchup-cards__date-info--date"})
        last_week_played = len(past_scores) - 4 #subtract 4 for preseason
        date = past_dates[last_week_played-1].get_text()
        statement = "The score of the Seattle Seahawks most recent game is "
        statement += past_results[last_week_played-1].get_text()
        statement += " "
        statement += past_scores[last_week_played-1].get_text()
        statement += " vs. the "
        statement += past_teams[last_week_played-1].get_text().strip()
        statement += " on "
        statement += date[2:] #ignore dot and space at beginning of string
        statement += "/"
        statement += year
        label1 = tkinter.Label(gui, text=statement) #Seahawks most recent game
        label1.pack()
    elif(team == "Grizzlies"):
        soup = BeautifulSoup(page.content, 'html.parser')
        past_scores = soup.find_all("span", {"class": "ml4"})
        past_results = soup.select("td.Table2__td div span.fw-bold")
        past_teams = soup.select("td.Table2__td div.flex span")
        past_dates = soup.select("tbody.Table2__tbody tr.filled td.Table2__td span")
        last_week_played = len(past_scores)
        statement = "The score of the Montana Grizzlies most recent game is "
        statement += past_results[last_week_played-1].get_text()
        statement += " "
        statement += past_scores[last_week_played-1].get_text().strip()
        statement += " vs. "
        statement += past_teams[last_week_played+11].get_text() #different offset due to website HTML setup
        statement += "on "
        statement += past_dates[last_week_played+14].get_text() #different offset due to website HTML setup
        statement += ", "
        statement += year
        label2 = tkinter.Label(gui, text=statement) #Grizzlies most recent game
        label2.pack()

hawks_page = requests.get("https://www.seahawks.com/schedule/")
griz_page = requests.get("http://www.espn.com/college-football/team/schedule/_/id/149/montana-grizzlies")
gui = tkinter.Tk() #window
gui.geometry("750x500")
frame = tkinter.Frame(gui) #frame
frame.pack()
seahawks_button = tkinter.Button(frame, text="Seahawks Most Recent Game",fg="blue",command=lambda : __last_game_played("Seahawks",gui,hawks_page))
griz_button = tkinter.Button(frame, text="Grizzlies Most Recent Game",fg="red",command=lambda : __last_game_played("Grizzlies",gui,griz_page))
seahawks_button.pack()
griz_button.pack()
gui.mainloop()

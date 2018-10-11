import tkinter      #used for GUI
from datetime import datetime

def last_game_played(team):
    if(team == "Seahawks"):
        page = requests.get("https://www.seahawks.com/schedule/")
        soup = BeautifulSoup(page.content, 'html.parser')
        past_scores = soup.find_all("span", {"class": "nfl-o-matchup-cards__score--points"})
        past_results = soup.find_all("span", {"class": "nfl-o-matchup-cards__score--result"})
        past_teams = soup.find_all("p", {"class": "nfl-o-matchup-cards__team-full-name"})
        last_week_played = len(past_scores) - 4 #subtract 4 for preseason
        statement = "The score of the Seattle Seahawks most recent game is "
        statement += past_results[last_week_played-1].get_text()
        statement += " "
        statement += past_scores[last_week_played-1].get_text()
        statement += " vs. the "
        statement += past_teams[last_week_played-1].get_text().strip()
        return statement
    elif(team == "Grizzlies"):
        page = requests.get("http://www.espn.com/college-football/team/schedule/_/id/149/montana-grizzlies")
        soup = BeautifulSoup(page.content, 'html.parser')
        past_scores = soup.find_all("span", {"class": "ml4"})
        past_results = soup.select("td.Table2__td div span.fw-bold")
        past_teams = soup.select("td.Table2__td div.flex span")
        last_week_played = len(past_scores)
        statement = "The score of the Montana Grizzlies most recent game is "
        statement += past_results[last_week_played-1].get_text()
        statement += " "
        statement += past_scores[last_week_played-1].get_text().strip()
        statement += " vs. "
        statement += past_teams[last_week_played+11].get_text() #different offset due to website HTML setup
        return statement
    
date = str(datetime.now())
year = date[0:4]
month = date[5:7]
day = date[8:10]
gui = tkinter.Tk()
seahawks_recent = last_game_played("Seahawks")
griz_recent = last_game_played("Grizzlies")
label1 = tkinter.Label(gui, text=seahawks_recent)
label1.pack()
label2 = tkinter.Label(gui, text=griz_recent)
label2.pack()
gui.mainloop()

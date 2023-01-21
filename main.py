import requests
from bs4 import BeautifulSoup
import csv
date = input('enter the date MM/DD/YYYY: ')

page = requests.get(f'https://www.yallakora.com/Match-Center/?date={date}')

# main


def main(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    match_details = [

    ]
    # ==> div of all matches and league details
    champions = soup.find_all('div', {'class': 'matchCard'})

    def get_match(champions):
        league = champions.contents[1].find('h2').text.strip()
        match = champions.contents[3].find_all('li')
        matches_number = len(match)
        for i in range(matches_number):
            
            # => first team
            team_a = match[i].find('div', {
                'class': 'teamA'
            }).text.strip()

            # => second team
            team_b = match[i].find('div', {
                'class': 'teamB'
            }).text.strip()

            # => match result
            result = match[i].find('div', {
                'class': 'MResult'
            }).find_all('span', {
                'class': 'score'

            })
            score = f'{result[0].text.strip()} - {result[1].text.strip()}'

            # => match time ..
            time = match[i].find('div', {'class': 'MResult'}).find(
                'span', {"class": "time"}).text.strip()

            # ==> match status
            status = match[i].find(
                'div', {'class': "matchStatus"}).text.strip()

            # => add details
            match_details.append({
                "البطولة": league,
                "الفرقة الاولة": team_a,
                "الفرقة الثانية": team_b,
                "النتيجة": score,
                "المعاد": time,
                "الحالة": status,

            })

    # => get all matches 
    try:
        for i in range(len(champions)):
            
            get_match(champions[i])

        keys = match_details[0].keys()
    except:
        print("error in get match like there is not matches </3")

# => insert data in csv file
    try: 
        with open('Desktop/match.csv', 'w') as file:
            dictWriter = csv.DictWriter(file, keys) 
            dictWriter.writeheader()
            dictWriter.writerows(match_details)
            # print(match_details)
            print('done')
            print(match_details)
    except csv.Error as error:
        print(f'error in inserting data in csv file {error}')


main(page)
# </> with instructor codezilla <3

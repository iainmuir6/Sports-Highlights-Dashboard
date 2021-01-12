# Iain Muir
# iam9ez

import json
import time
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats


def get_team_id(team):
    """ Get team ID based on player name """
    teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)

    for each in teams:
        if each['teamName'] == team:
            return each['teamId']
    return -1


def get_player_id(first, last):
    """ Get player ID based on player name """
    players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1


def create_court(ax, color):
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)

    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)


def generate_shot_chart(player, year, season_type, graph):
    shot_json = shotchartdetail.ShotChartDetail(
        team_id=team_list[i],
        player_id=players_dict[player][0],
        context_measure_simple='FGA',
        season_nullable=year,
        season_type_all_star=season_type)

    shot_data = json.loads(shot_json.get_json())['resultSets'][0]
    headers = shot_data['headers']
    rows = shot_data['rowSet']
    data = pd.DataFrame(rows, columns=headers)

    if len(data) < 1:
        # print("Not enough shots!")
        return

    clutch_shots = data[data['PERIOD'] == 4]
    clutch_shots = clutch_shots[clutch_shots['SECONDS_REMAINING'] < 60]

    if len(clutch_shots) == 0:
        # print("Not enough shots!")
        return

    clutch[player][0] += list(clutch_shots.SHOT_MADE_FLAG).count(0)
    clutch[player][1] += list(clutch_shots.SHOT_MADE_FLAG).count(1)

    # Date Filter
    # today = '20191028'
    # data = data[data['GAME_DATE'] == today]
    # data = data.reset_index()
    should_graph = True

    if should_graph:
        # General plot parameters
        mpl.rcParams['font.family'] = 'Avenir'
        mpl.rcParams['font.size'] = 18
        mpl.rcParams['axes.linewidth'] = 2
        mpl.rcParams['figure.figsize'] = 6.383, 6
        fig, ax = plt.subplots()

        team = teams_dict[team_list[i]][1]

        # Annotate player name and season
        ax.text(0, 1.05, player + " – " + team + '\n' + year + ' ' + season_type,
                transform=ax.transAxes, ha='left', va='baseline')

        # Display background image
        img = mpimg.imread('/Users/iainmuir/PycharmProjects/Desktop/Practice/shotChartProject/court.jpg')
        ax.imshow(img, extent=[-250, 250, 0, 470])

        logo = mpimg.imread("/Users/iainmuir/PycharmProjects/Desktop/Practice/theScore/Input/TeamLogos/" + team + ".png")
        height, width = logo.shape[0], logo.shape[1]
        ax.imshow(logo, extent=[0 - (width // 2), 0 + (width // 2), 430 - (height // 2), 430 + (height // 2)])

        # Create basketball court
        create_court(ax, 'black')

        # Plot hexbin of shots with logarithmic binning
        if graph == 'hex':
            ax.hexbin(data['LOC_X'], data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940),
                      bins='log', cmap='Blues')

        if graph == 'plot':
            make_miss = list(data['SHOT_MADE_FLAG'])
            markers = ["o" if shot == 0 else "X" for shot in make_miss]
            colors = ["g" if shot == 0 else "r" for shot in make_miss]

            # ax.scatter(data['LOC_X'], data['LOC_Y'] + 60, c=data.SHOT_MADE_FLAG.map({0: 'g', 1: 'r'}), marker='o')

            list(map(lambda each: ax.scatter(data['LOC_X'][each], data['LOC_Y'][each] + 60,
                                             c=colors[each], marker=markers[each]), range(len(data['LOC_X']))))

            # for i in range(len(data['LOC_X'])):
            #     ax.scatter(data['LOC_X'][i], data['LOC_Y'][i] + 60, c=colors[i], marker=markers[i])

        print("\n---- Finished graph in %s seconds ----" % round(time.time() - st, 3))

        figure = plt.gcf()
        figure.savefig("/Users/iainmuir/PycharmProjects/Desktop/Practice/shotChartProject/shotChartImages/" +
                       player + " - " + year)


if __name__ == '__main__':
    st = time.time()

    # # Get team ID based on team name
    # for team in teams:
    #     # teams_dict[team['teamName']] = (team['teamId'], team['abbreviation'])
    #     teams_dict[team['teamId']] = (team['teamName'], team['abbreviation'] + " " + team['teamName'].split()[-1])

    # # Get player ID based on player name
    # for player in players:
    #     players_dict[player['firstName'] + " " + player['lastName']] = (player['playerId'], player['teamId'])

    players_dict = {'Michael Jordan': (893, 1610612741), 'Steven Adams': (203500, 1610612760), 'Bam Adebayo': (1628389, 1610612748), 'LaMarcus Aldridge': (200746, 1610612759), 'Nickeil Alexander-Walker': (1629638, 1610612740), 'Grayson Allen': (1628960, 1610612763), 'Jarrett Allen': (1628386, 1610612751), 'Kadeem Allen': (1628443, 1610612752), 'Al-Farouq Aminu': (202329, 1610612753), 'Kyle Anderson': (203937, 1610612763), 'Ryan Anderson': (201583, 0), 'Giannis Antetokounmpo': (203507, 1610612749), 'Kostas Antetokounmpo': (1628961, 1610612747), 'Thanasis Antetokounmpo': (203648, 1610612749), 'Carmelo Anthony': (2546, 1610612757), 'OG Anunoby': (1628384, 1610612761), 'Ryan Arcidiacono': (1627853, 1610612741), 'Trevor Ariza': (2772, 1610612758), 'D.J. Augustin': (201571, 1610612753), 'Deandre Ayton': (1629028, 1610612756), 'Dwayne Bacon': (1628407, 1610612766), 'Marvin Bagley III': (1628963, 1610612758), 'Lonzo Ball': (1628366, 1610612740), 'Mo Bamba': (1628964, 1610612753), 'J.J. Barea': (200826, 1610612742), 'Harrison Barnes': (203084, 1610612758), 'RJ Barrett': (1629628, 1610612752), 'Will Barton': (203115, 1610612743), 'Keita Bates-Diop': (1628966, 1610612750), 'Nicolas Batum': (201587, 1610612766), 'Aron Baynes': (203382, 1610612756), 'Kent Bazemore': (203145, 1610612757), 'Darius Bazley': (1629647, 1610612760), 'Bradley Beal': (203078, 1610612764), 'Malik Beasley': (1627736, 1610612743), 'Marco Belinelli': (201158, 1610612759), 'Jordan Bell': (1628395, 1610612750), "DeAndre' Bembry": (1627761, 1610612737), 'Dragan Bender': (1627733, 1610612749), 'Davis Bertans': (202722, 1610612764), 'Patrick Beverley': (201976, 1610612746), 'Khem Birch': (203920, 1610612753), 'Goga Bitadze': (1629048, 1610612754), 'Bismack Biyombo': (202687, 1610612766), 'Nemanja Bjelica': (202357, 1610612758), 'Eric Bledsoe': (202339, 1610612749), 'Bogdan Bogdanovic': (203992, 1610612758), 'Bojan Bogdanovic': (202711, 1610612762), 'Bol Bol': (1629626, 1610612743), 'Jonah Bolden': (1628413, 1610612755), 'Jordan Bone': (1629648, 1610612765), 'Isaac Bonga': (1629067, 1610612764), 'Devin Booker': (1626164, 1610612756), 'Chris Boucher': (1628449, 1610612761), 'Brian Bowen II': (1628968, 1610612754), 'Ky Bowman': (1629065, 1610612744), 'Avery Bradley': (202340, 1610612747), 'Tony Bradley': (1628396, 1610612762), 'Jarrell Brantley': (1629714, 1610612762), 'Ignas Brazdeikis': (1629649, 1610612752), 'Mikal Bridges': (1628969, 1610612756), 'Miles Bridges': (1628970, 1610612766), 'Oshae Brissett': (1629052, 1610612761), 'Ryan Broekhoff': (1629151, 1610612742), 'Malcolm Brogdon': (1627763, 1610612754), 'Dillon Brooks': (1628415, 1610612763), 'Bruce Brown': (1628971, 1610612765), 'Jaylen Brown': (1627759, 1610612738), 'Moses Brown': (1629650, 1610612757), 'Sterling Brown': (1628425, 1610612749), 'Charles Brown Jr.': (1629718, 1610612737), 'Troy Brown Jr.': (1628972, 1610612764), 'Jalen Brunson': (1628973, 1610612742), 'Thomas Bryant': (1628418, 1610612764), 'Reggie Bullock': (203493, 1610612752), 'Trey Burke': (203504, 1610612755), 'Alec Burks': (202692, 1610612744), 'Deonte Burton': (1629126, 1610612760), 'Jimmy Butler': (202710, 1610612748), 'Bruno Caboclo': (203998, 1610612763), 'Kentavious Caldwell-Pope': (203484, 1610612747), 'Vlatko Cancar': (1628427, 1610612743), 'Clint Capela': (203991, 1610612745), 'DeMarre Carroll': (201960, 1610612759), 'Jevon Carter': (1628975, 1610612756), 'Vince Carter': (1713, 1610612737), 'Wendell Carter Jr.': (1628976, 1610612741), 'Michael Carter-Williams': (203487, 1610612753), 'Alex Caruso': (1627936, 1610612747), 'Willie Cauley-Stein': (1626161, 1610612744), 'Tyson Chandler': (2199, 1610612745), 'Wilson Chandler': (201163, 1610612751), 'Zylan Cheatham': (1629597, 1610612740), 'Chris Chiozza': (1629185, 1610612764), 'Marquese Chriss': (1627737, 1610612744), 'Gary Clark': (1629109, 1610612745), 'Brandon Clarke': (1629634, 1610612763), 'Jordan Clarkson': (203903, 1610612739), 'Nicolas Claxton': (1629651, 1610612751), 'Chris Clemons': (1629598, 1610612745), 'Antonius Cleveland': (1628499, 1610612742), 'Amir Coffey': (1629599, 1610612746), 'John Collins': (1628381, 1610612737), 'Zach Collins': (1628380, 1610612757), 'Mike Conley': (201144, 1610612762), 'Pat Connaughton': (1626192, 1610612749), 'Quinn Cook': (1626188, 1610612747), 'Tyler Cook': (1629076, 1610612739), 'DeMarcus Cousins': (202326, 1610612747), 'Robert Covington': (203496, 1610612750), 'Allen Crabbe': (203459, 1610612737), 'Torrey Craig': (1628470, 1610612743), 'Jae Crowder': (203109, 1610612763), 'Jarrett Culver': (1629633, 1610612750), 'Seth Curry': (203552, 1610612742), 'Stephen Curry': (201939, 1610612744), 'Troy Daniels': (203584, 1610612747), 'Anthony Davis': (203076, 1610612747), 'Ed Davis': (202334, 1610612762), 'Terence Davis': (1629056, 1610612761), 'DeMar DeRozan': (201942, 1610612759), 'Dewayne Dedmon': (203473, 1610612758), 'Matthew Dellavedova': (203521, 1610612739), 'Donte DiVincenzo': (1628978, 1610612749), 'Cheick Diallo': (1627767, 1610612756), 'Hamidou Diallo': (1628977, 1610612760), 'Gorgui Dieng': (203476, 1610612750), 'Spencer Dinwiddie': (203915, 1610612751), 'Luka Doncic': (1629029, 1610612742), 'Luguentz Dort': (1629652, 1610612760), 'Damyean Dotson': (1628422, 1610612752), 'Sekou Doumbouya': (1629635, 1610612765), 'PJ Dozier': (1628408, 1610612743), 'Goran Dragic': (201609, 1610612748), 'Andre Drummond': (203083, 1610612765), 'Jared Dudley': (201162, 1610612747), 'Kris Dunn': (1627739, 1610612741), 'Kevin Durant': (201142, 1610612751), 'Carsen Edwards': (1629035, 1610612738), 'Henry Ellenson': (1627740, 1610612751), 'Wayne Ellington': (201961, 1610612752), 'Joel Embiid': (203954, 1610612755), 'James Ennis III': (203516, 1610612755), 'Drew Eubanks': (1629234, 1610612759), 'Jacob Evans': (1628980, 1610612744), 'Dante Exum': (203957, 1610612762), 'Tacko Fall': (1629605, 1610612738), 'Derrick Favors': (202324, 1610612740), 'Cristiano Felicio': (1626245, 1610612741), 'Terrance Ferguson': (1628390, 1610612760), 'Bruno Fernando': (1628981, 1610612737), 'Yogi Ferrell': (1627812, 1610612758), 'Dorian Finney-Smith': (1627827, 1610612742), 'Bryn Forbes': (1627854, 1610612759), 'Evan Fournier': (203095, 1610612753), "De'Aaron Fox": (1628368, 1610612758), 'Robert Franks': (1629606, 1610612766), 'Michael Frazier': (1626187, 1610612745), 'Tim Frazier': (204025, 1610612765), 'Melvin Frazier Jr.': (1628982, 1610612753), 'Markelle Fultz': (1628365, 1610612753), 'Wenyen Gabriel': (1629117, 1610612758), 'Daniel Gafford': (1629655, 1610612741), 'Danilo Gallinari': (201568, 1610612760), 'Langston Galloway': (204038, 1610612765), 'Darius Garland': (1629636, 1610612739), 'Marc Gasol': (201188, 1610612761), 'Rudy Gay': (200752, 1610612759), 'Paul George': (202331, 1610612746), 'Taj Gibson': (201959, 1610612752), 'Harry Giles III': (1628385, 1610612758), 'Shai Gilgeous-Alexander': (1628983, 1610612760), 'Rudy Gobert': (203497, 1610612762), 'Brandon Goodwin': (1629164, 1610612737), 'Aaron Gordon': (203932, 1610612753), 'Eric Gordon': (201569, 1610612745), "Devonte' Graham": (1628984, 1610612766), 'Treveon Graham': (1626203, 1610612750), 'Jerami Grant': (203924, 1610612743), 'Josh Gray': (1627982, 1610612740), 'Danny Green': (201980, 1610612747), 'Draymond Green': (203110, 1610612744), 'Gerald Green': (101123, 1610612745), 'JaMychal Green': (203210, 1610612746), 'Javonte Green': (1629750, 1610612738), 'Jeff Green': (201145, 1610612762), 'Blake Griffin': (201933, 1610612765), 'Marko Guduric': (1629741, 1610612763), 'Kyle Guy': (1629657, 1610612758), 'Rui Hachimura': (1629060, 1610612764), 'Devon Hall': (1628985, 1610612760), 'Tim Hardaway Jr.': (203501, 1610612742), 'James Harden': (201935, 1610612745), 'Maurice Harkless': (203090, 1610612746), 'Jared Harper': (1629607, 1610612756), 'Montrezl Harrell': (1626149, 1610612746), 'Gary Harris': (203914, 1610612743), 'Joe Harris': (203925, 1610612751), 'Tobias Harris': (202699, 1610612755), 'Shaquille Harrison': (1627885, 1610612741), 'Josh Hart': (1628404, 1610612740), 'Isaiah Hartenstein': (1628392, 1610612745), 'Udonis Haslem': (2617, 1610612748), 'Jaxson Hayes': (1629637, 1610612740), 'Gordon Hayward': (202330, 1610612738), 'John Henson': (203089, 1610612739), 'Dewan Hernandez': (1629608, 1610612761), 'Juancho Hernangomez': (1627823, 1610612743), 'Willy Hernangomez': (1626195, 1610612766), 'Tyler Herro': (1629639, 1610612748), 'Mario Hezonja': (1626209, 1610612757), 'Buddy Hield': (1627741, 1610612758), 'Nene ': (2403, 1610612745), 'George Hill': (201588, 1610612749), 'Solomon Hill': (203524, 1610612763), 'Jaylen Hoard': (1629658, 1610612757), 'Aaron Holiday': (1628988, 1610612754), 'Jrue Holiday': (201950, 1610612740), 'Justin Holiday': (203200, 1610612754), 'Rondae Hollis-Jefferson': (1626178, 1610612761), 'Richaun Holmes': (1626158, 1610612758), 'Rodney Hood': (203918, 1610612757), 'Al Horford': (201143, 1610612755), 'Talen Horton-Tucker': (1629659, 1610612747), 'Danuel House Jr.': (1627863, 1610612745), 'Dwight Howard': (2730, 1610612747), 'Kevin Huerter': (1628989, 1610612737), "De'Andre Hunter": (1629631, 1610612737), 'Chandler Hutchison': (1628990, 1610612741), 'Serge Ibaka': (201586, 1610612761), 'Andre Iguodala': (2738, 1610612763), 'Ersan Ilyasova': (101141, 1610612749), 'Joe Ingles': (204060, 1610612762), 'Brandon Ingram': (1627742, 1610612740), 'Kyrie Irving': (202681, 1610612751), 'Jonathan Isaac': (1628371, 1610612753), 'Wes Iwundu': (1628411, 1610612753), 'Frank Jackson': (1628402, 1610612740), 'Josh Jackson': (1628367, 1610612763), 'Justin Jackson': (1628382, 1610612742), 'Reggie Jackson': (202704, 1610612765), 'Jaren Jackson Jr.': (1628991, 1610612763), 'Justin James': (1629713, 1610612758), 'LeBron James': (2544, 1610612747), 'Amile Jefferson': (1628518, 1610612753), 'DaQuan Jeffries': (1629610, 1610612758), 'Ty Jerome': (1629660, 1610612756), 'Alize Johnson': (1628993, 1610612754), 'BJ Johnson': (1629168, 1610612753), 'Cameron Johnson': (1629661, 1610612756), 'James Johnson': (201949, 1610612748), 'Keldon Johnson': (1629640, 1610612759), 'Stanley Johnson': (1626169, 1610612761), 'Tyler Johnson': (204020, 1610612756), 'Nikola Jokic': (203999, 1610612743), 'Damian Jones': (1627745, 1610612737), 'Tyus Jones': (1626145, 1610612763), 'Derrick Jones Jr.': (1627884, 1610612748), 'DeAndre Jordan': (201599, 1610612751), 'Cory Joseph': (202709, 1610612758), 'Mfiondu Kabengele': (1629662, 1610612746), 'Frank Kaminsky': (1626163, 1610612756), 'Enes Kanter': (202683, 1610612738), 'Luke Kennard': (1628379, 1610612765), 'Stanton Kidd': (1629742, 0), 'Michael Kidd-Gilchrist': (203077, 1610612766), 'Louis King': (1629663, 1610612765), 'Maxi Kleber': (1628467, 1610612742), 'Brandon Knight': (202688, 1610612739), 'Kevin Knox II': (1628995, 1610612752), 'John Konchar': (1629723, 1610612763), 'Furkan Korkmaz': (1627788, 1610612755), 'Luke Kornet': (1628436, 1610612741), 'Kyle Korver': (2594, 1610612749), 'Rodions Kurucs': (1629066, 1610612751), 'Kyle Kuzma': (1628398, 1610612747), 'Zach LaVine': (203897, 1610612741), 'Skal Labissiere': (1627746, 1610612757), 'Jeremy Lamb': (203087, 1610612754), 'Romeo Langford': (1629641, 1610612738), 'Jake Layman': (1627774, 1610612750), 'Caris LeVert': (1627747, 1610612751), 'TJ Leaf': (1628388, 1610612754), 'Jalen Lecque': (1629665, 1610612756), 'Courtney Lee': (201584, 1610612742), 'Damion Lee': (1627814, 1610612744), 'Alex Len': (203458, 1610612737), 'Kawhi Leonard': (202695, 1610612746), 'Meyers Leonard': (203086, 1610612748), 'Damian Lillard': (203081, 1610612757), 'Nassir Little': (1629642, 1610612757), 'Kevon Looney': (1626172, 1610612744), 'Brook Lopez': (201572, 1610612749), 'Robin Lopez': (201577, 1610612749), 'Kevin Love': (201567, 1610612739), 'Kyle Lowry': (200768, 1610612761), 'Timothe Luwawu-Cabarrot': (1627789, 1610612751), 'Trey Lyles': (1626168, 1610612759), 'Daryl Macon': (1629133, 1610612748), 'Josh Magette': (203705, 1610612753), 'Ian Mahinmi': (101133, 1610612764), 'Thon Maker': (1627748, 1610612765), 'Terance Mann': (1629611, 1610612746), 'Boban Marjanovic': (1626246, 1610612742), 'Lauri Markkanen': (1628374, 1610612741), 'Caleb Martin': (1628997, 1610612766), 'Cody Martin': (1628998, 1610612766), 'Kelan Martin': (1629103, 1610612750), 'Frank Mason': (1628412, 1610612749), 'Garrison Mathews': (1629726, 1610612764), 'Wesley Matthews': (202083, 1610612749), 'Patrick McCaw': (1627775, 1610612761), 'CJ McCollum': (203468, 1610612757), 'T.J. McConnell': (204456, 1610612754), 'Jalen McDaniels': (1629667, 1610612766), 'Doug McDermott': (203926, 1610612754), 'JaVale McGee': (201580, 1610612747), 'Rodney McGruder': (203585, 1610612746), 'Alfonzo McKinnie': (1628035, 1610612739), 'Jordan McLaughlin': (1629162, 1610612750), 'Ben McLemore': (203463, 1610612745), 'Jordan McRae': (203895, 1610612764), 'Nicolo Melli': (1629740, 1610612740), "De'Anthony Melton": (1629001, 1610612763), 'Chimezie Metu': (1629002, 1610612759), 'Khris Middleton': (203114, 1610612749), 'CJ Miles': (101139, 1610612764), 'Darius Miller': (203121, 1610612740), 'Malcolm Miller': (1626259, 1610612761), 'Patty Mills': (201988, 1610612759), 'Paul Millsap': (200794, 1610612743), 'Shake Milton': (1629003, 1610612755), 'Donovan Mitchell': (1628378, 1610612762), 'Naz Mitrou-Long': (1628513, 1610612754), 'Adam Mokoka': (1629690, 1610612741), 'Malik Monk': (1628370, 1610612766), "E'Twaun Moore": (202734, 1610612740), 'Ja Morant': (1629630, 1610612763), 'Juwan Morgan': (1629752, 1610612762), 'Markieff Morris': (202693, 1610612765), 'Monte Morris': (1628420, 1610612743), 'Marcus Morris Sr.': (202694, 1610612752), 'Johnathan Motley': (1628405, 1610612746), 'Emmanuel Mudiay': (1626144, 1610612762), 'Dejounte Murray': (1627749, 1610612759), 'Jamal Murray': (1627750, 1610612743), 'Dzanan Musa': (1629058, 1610612751), 'Mike Muscala': (203488, 1610612760), 'Svi Mykhailiuk': (1629004, 1610612765), 'Abdel Nader': (1627846, 1610612760), 'Larry Nance Jr.': (1626204, 1610612739), 'Shabazz Napier': (203894, 1610612750), 'Raul Neto': (203526, 1610612755), 'Georges Niang': (1627777, 1610612762), 'Nerlens Noel': (203457, 1610612760), 'Zach Norvell Jr.': (1629668, 1610612747), 'Jaylen Nowell': (1629669, 1610612750), 'Frank Ntilikina': (1628373, 1610612752), 'Kendrick Nunn': (1629134, 1610612748), 'Jusuf Nurkic': (203994, 1610612757), 'David Nwaba': (1628021, 1610612751), "Royce O'Neale": (1626220, 1610612762), "Kyle O'Quinn": (203124, 1610612755), 'Semi Ojeleye': (1628400, 1610612738), 'Jahlil Okafor': (1626143, 1610612740), 'Elie Okobo': (1629059, 1610612756), 'Josh Okogie': (1629006, 1610612750), 'KZ Okpala': (1629644, 1610612748), 'Victor Oladipo': (203506, 1610612754), 'Kelly Olynyk': (203482, 1610612748), 'Miye Oni': (1629671, 1610612762), 'Cedi Osman': (1626224, 1610612739), 'Kelly Oubre Jr.': (1626162, 1610612756), 'Jabari Parker': (203953, 1610612737), 'Chandler Parsons': (202718, 1610612737), 'Eric Paschall': (1629672, 1610612744), 'Patrick Patterson': (202335, 1610612746), 'Justin Patton': (1628383, 1610612760), 'Chris Paul': (101108, 1610612760), 'Elfrid Payton': (203901, 1610612752), 'Norvel Pelle': (203658, 1610612755), 'Theo Pinson': (1629033, 1610612751), 'Mason Plumlee': (203486, 1610612743), 'Jakob Poeltl': (1627751, 1610612759), 'Vincent Poirier': (1629738, 1610612738), 'Shamorie Ponds': (1629044, 1610612761), 'Jordan Poole': (1629673, 1610612744), 'Kevin Porter Jr.': (1629645, 1610612739), 'Michael Porter Jr.': (1629008, 1610612743), 'Otto Porter Jr.': (203490, 1610612741), 'Bobby Portis': (1626171, 1610612752), 'Kristaps Porzingis': (204001, 1610612742), 'Dwight Powell': (203939, 1610612742), 'Norman Powell': (1626181, 1610612761), 'Taurean Prince': (1627752, 1610612751), 'Ivan Rabb': (1628397, 1610612752), 'Julius Randle': (203944, 1610612752), 'Josh Reaves': (1629729, 1610612742), 'Cam Reddish': (1629629, 1610612737), 'JJ Redick': (200755, 1610612740), 'Naz Reid': (1629675, 1610612750), 'Cameron Reynolds': (1629244, 1610612749), 'Josh Richardson': (1626196, 1610612755), 'Austin Rivers': (203085, 1610612745), 'Andre Roberson': (203460, 1610612760), 'Duncan Robinson': (1629130, 1610612748), 'Jerome Robinson': (1629010, 1610612746), 'Justin Robinson': (1629620, 1610612764), 'Mitchell Robinson': (1629011, 1610612752), 'Glenn Robinson III': (203922, 1610612744), 'Isaiah Roby': (1629676, 1610612742), 'Rajon Rondo': (200765, 1610612747), 'Derrick Rose': (201565, 1610612765), 'Terrence Ross': (203082, 1610612753), 'Terry Rozier': (1626179, 1610612766), 'Ricky Rubio': (201937, 1610612756), "D'Angelo Russell": (1626156, 1610612744), 'Domantas Sabonis': (1627734, 1610612754), 'Luka Samanic': (1629677, 1610612759), 'JaKarr Sampson': (203960, 1610612754), 'Dario Saric': (203967, 1610612756), 'Tomas Satoransky': (203107, 1610612741), 'Admiral Schofield': (1629678, 1610612764), 'Dennis Schroder': (203471, 1610612760), 'Mike Scott': (203118, 1610612755), 'Thabo Sefolosha': (200757, 1610612745), 'Collin Sexton': (1629012, 1610612739), 'Landry Shamet': (1629013, 1610612746), 'Marial Shayok': (1629621, 1610612755), 'Iman Shumpert': (202697, 1610612751), 'Pascal Siakam': (1627783, 1610612761), 'Chris Silva': (1629735, 1610612748), 'Ben Simmons': (1627732, 1610612755), 'Kobi Simmons': (1628424, 1610612766), 'Anfernee Simons': (1629014, 1610612757), 'Alen Smailagic': (1629346, 1610612744), 'Marcus Smart': (203935, 1610612738), 'Ish Smith': (202397, 1610612764), 'Zhaire Smith': (1629015, 1610612755), 'Dennis Smith Jr.': (1628372, 1610612752), 'Tony Snell': (203503, 1610612765), 'Omari Spellman': (1629016, 1610612744), 'Max Strus': (1629622, 1610612741), 'Edmond Sumner': (1628410, 1610612754), 'Caleb Swanigan': (1628403, 1610612758), 'Jayson Tatum': (1628369, 1610612738), 'Jeff Teague': (201952, 1610612750), 'Garrett Temple': (202066, 1610612751), 'Daniel Theis': (1628464, 1610612738), 'Isaiah Thomas': (202738, 1610612764), 'Khyri Thomas': (1629017, 1610612765), 'Matt Thomas': (1629744, 1610612761), 'Klay Thompson': (202691, 1610612744), 'Tristan Thompson': (202684, 1610612739), 'Matisse Thybulle': (1629680, 1610612755), 'Anthony Tolliver': (201229, 1610612757), 'Karl-Anthony Towns': (1626157, 1610612750), 'Gary Trent Jr.': (1629018, 1610612757), 'Allonzo Trier': (1629019, 1610612752), 'P.J. Tucker': (200782, 1610612745), 'Evan Turner': (202323, 1610612737), 'Myles Turner': (1626167, 1610612754), 'Jonas Valanciunas': (202685, 1610612763), 'Denzel Valentine': (1627756, 1610612741), 'Fred VanVleet': (1627832, 1610612761), 'Jarred Vanderbilt': (1629020, 1610612743), 'Noah Vonleh': (203943, 1610612750), 'Nikola Vucevic': (202696, 1610612753), 'Dean Wade': (1629731, 1610612739), 'Moritz Wagner': (1629021, 1610612764), 'Dion Waiters': (203079, 1610612748), 'Kemba Walker': (202689, 1610612738), 'Lonnie Walker IV': (1629022, 1610612759), 'John Wall': (202322, 1610612764), 'Tyrone Wallace': (1627820, 1610612737), 'Derrick Walton Jr.': (1628476, 1610612746), 'Brad Wanamaker': (202954, 1610612738), 'T.J. Warren': (203933, 1610612754), 'P.J. Washington': (1629023, 1610612766), 'Yuta Watanabe': (1629139, 1610612763), 'Tremont Waters': (1629682, 1610612738), 'Quinndary Weatherspoon': (1629683, 1610612759), 'Russell Westbrook': (201566, 1610612745), 'Coby White': (1629632, 1610612741), 'Derrick White': (1628401, 1610612759), 'Hassan Whiteside': (202355, 1610612757), 'Andrew Wiggins': (203952, 1610612750), 'Grant Williams': (1629684, 1610612738), 'Kenrich Williams': (1629026, 1610612740), 'Lou Williams': (101150, 1610612746), 'Marvin Williams': (101107, 1610612766), 'Robert Williams III': (1629057, 1610612738), 'Nigel Williams-Goss': (1628430, 1610612762), 'Zion Williamson': (1629627, 1610612740), 'D.J. Wilson': (1628391, 1610612749), 'Dylan Windler': (1629685, 1610612739), 'Justise Winslow': (1626159, 1610612748), 'Christian Wood': (1626174, 1610612765), 'Delon Wright': (1626153, 1610612742), 'Justin Wright-Foreman': (1629625, 1610612762), 'Thaddeus Young': (201152, 1610612741), 'Trae Young': (1629027, 1610612737), 'Cody Zeller': (203469, 1610612766), 'Ante Zizic': (1627790, 1610612739), 'Ivica Zubac': (1627826, 1610612746)}
    teams_dict = {1610612737: ('Atlanta Hawks', 'ATL Hawks'), 1610612738: ('Boston Celtics', 'BOS Celtics'), 1610612751: ('Brooklyn Nets', 'BKN Nets'), 1610612766: ('Charlotte Hornets', 'CHA Hornets'), 1610612741: ('Chicago Bulls', 'CHI Bulls'), 1610612739: ('Cleveland Cavaliers', 'CLE Cavaliers'), 1610612742: ('Dallas Mavericks', 'DAL Mavericks'), 1610612743: ('Denver Nuggets', 'DEN Nuggets'), 1610612765: ('Detroit Pistons', 'DET Pistons'), 1610612744: ('Golden State Warriors', 'GSW Warriors'), 1610612745: ('Houston Rockets', 'HOU Rockets'), 1610612754: ('Indiana Pacers', 'IND Pacers'), 1610612746: ('Los Angeles Clippers', 'LAC Clippers'), 1610612747: ('Los Angeles Lakers', 'LAL Lakers'), 1610612763: ('Memphis Grizzlies', 'MEM Grizzlies'), 1610612748: ('Miami Heat', 'MIA Heat'), 1610612749: ('Milwaukee Bucks', 'MIL Bucks'), 1610612750: ('Minnesota Timberwolves', 'MIN Timberwolves'), 1610612740: ('New Orleans Pelicans', 'NOP Pelicans'), 1610612752: ('New York Knicks', 'NYK Knicks'), 1610612760: ('Oklahoma City Thunder', 'OKC Thunder'), 1610612753: ('Orlando Magic', 'ORL Magic'), 1610612755: ('Philadelphia 76ers', 'PHI 76ers'), 1610612756: ('Phoenix Suns', 'PHX Suns'), 1610612757: ('Portland Trail Blazers', 'POR Blazers'), 1610612758: ('Sacramento Kings', 'SAC Kings'), 1610612759: ('San Antonio Spurs', 'SAS Spurs'), 1610612761: ('Toronto Raptors', 'TOR Raptors'), 1610612762: ('Utah Jazz', 'UTA Jazz'), 1610612764: ('Washington Wizards', 'WAS Wizards')}

    clutch = {'Michael Jordan': [0, 0],
              'LeBron James': [0, 0]}

    stats_json = playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=players_dict['LeBron James'][0])
    stats = json.loads(stats_json.get_json())['resultSets'][0]
    headers = stats['headers']
    rows = stats['rowSet']
    data1 = pd.DataFrame(rows, columns=headers)
    team_list = list(data1.TEAM_ID)

    i = 0
    for yr in range(2003, 2020):
        season = str(yr) + "-" + str(yr + 1)[-2:]
        # print(i, season)
        generate_shot_chart('LeBron James', season, 'Regular Season', 'plot')
        i += 1

    exit(0)

    # print(clutch

    stats_json = playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=players_dict['Michael Jordan'][0])
    stats = json.loads(stats_json.get_json())['resultSets'][0]
    headers = stats['headers']
    rows = stats['rowSet']
    data1 = pd.DataFrame(rows, columns=headers)
    team_list = list(data1.TEAM_ID)

    i = 0
    for yr in range(1984, 2003):
        if yr in [1993, 1998, 1999, 2000]:
            continue
        season = str(yr) + "-" + str(yr + 1)[-2:]
        # print(i, season)
        generate_shot_chart('Michael Jordan', season, 'Regular Season', 'plot')
        i += 1

    print("Late-game percentages: \n\t LeBron James: " +
          str(round((clutch['LeBron James'][0] / (clutch['LeBron James'][0] + clutch['LeBron James'][1])) * 100, 3)) +
          "% \n\t Michael Jordan: " +
          str(round((clutch['Michael Jordan'][0] / (clutch['Michael Jordan'][0] +
                                                    clutch['Michael Jordan'][1])) * 100, 3)) + "% \n\n")

    print("---- Finished program in %s seconds ----" % round(time.time() - st, 3))

def getTeamUrls(filename):
    allTeams = []

    file = open(filename, "r")
    while True:
        teamName = file.readline()
        if not teamName:
            break
        teamName = teamName.replace(":", "")
        teamName = teamName.replace(" ", "_")
        teamName = teamName.replace("\n", "")
        teamName = teamName.replace("\"", "")
        teamName = teamName.lower()
        teamUrl = file.readline()
        allTeams.append([teamName, teamUrl])
    file.close()
    return allTeams

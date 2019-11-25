import sys
from single_elim import SingleElimTournament
from round_robin import RoundRobinTournament

if __name__ == "__main__":
    tournament = None
    n = int(sys.argv[2])
    if sys.argv[1] in "--cup":
        tournament = SingleElimTournament(n)
    elif sys.argv[1] in "--league":
        tournament = RoundRobinTournament(n)
    tournament.host_tournament()
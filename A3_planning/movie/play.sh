
echo "hello"
fd2 --plan-file movie_night_plan movie_night.pddl movie_night_p1.pddl --heuristic "h=ff()" --search "astar(h)"

import chess.pgn
import pandas as pd
import time
from collections import Counter

# king position at checkmate

def parse_checkmate_squares(filepath, ngames):
    

    def checkmate_generator(filepath, ngames):
        with open(filepath) as pgns:
            for _ in range(ngames):
                gm = chess.pgn.read_game(pgns)
                try:
                    end = gm.end()
                    if end.board().is_checkmate():
                        color = end.turn()
                        square = list(end.board().pieces(chess.KING, color))[0]
                        yield [color, square]
                except AttributeError: # some cases, like abandons, where no moves are ever played which causes errors
                    continue


    white_mates = Counter()
    black_mates = Counter()
    # I'm sure I don't need to be using two Counters since I just combine them later... but it feels intuitive and works so I'm sticking with it

    for checkmate in checkmate_generator(filepath, ngames):
        if checkmate[0]:
            white_mates[checkmate[1]] += 1
        else:
            black_mates[checkmate[1]] += 1

    white_mates, black_mates = pd.DataFrame([white_mates]).transpose(), pd.DataFrame([black_mates]).transpose()
    combined = white_mates.merge(black_mates, left_index=True, right_index=True)
    combined.reset_index(level=0, inplace=True)
    combined.columns = ['square','white', 'black']
    combined['total'] = combined['white'] + combined['black']
    
    return combined


def main():
    start_time = time.time()
    mates = parse_checkmate_squares('/Users/ronaldauclair/Documents/personal/chess/checkmate_squares/lichess_db_standard_rated_2017-04.pgn', 1000000)
    
    mates.to_csv('checkmate_squares.csv', index=False)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
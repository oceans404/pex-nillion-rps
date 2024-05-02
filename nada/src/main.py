from nada_dsl import *

def nada_main():
    party_computer = Party(name="Computer") 
    party_player = Party(name="Player")

    # possible choices for choice_computer and choice_player_2
    # 10 - Rock
    # 11 - Paper
    # 12 - Scissors 
    choice_computer = SecretInteger(Input(name="choice_computer", party=party_computer))
    choice_player_2 = SecretInteger(Input(name="choice_player_2", party=party_player))

    # Adjust the choices to start from 0 by subtracting 10 becuase 0 can't be the secret input
    adjusted_choice_computer = (choice_computer - Integer(10)) % Integer(3)
    adjusted_choice_player_2 = (choice_player_2 - Integer(10)) % Integer(3)

    # modular arithmetic, cyclical RPS logic
    result = (adjusted_choice_computer - adjusted_choice_player_2 + Integer(3)) % Integer(3)

    # Which player won?
    winner = (
        (result > Integer(0)).if_else(
            (result > Integer(1)).if_else(Integer(2), Integer(1)),
            Integer(0)
        )
    )

    out = Output(winner, "game_result", party_computer)

    return [out]

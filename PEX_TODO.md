# Create a RPS Nada Program

We'll use the nada tool to create a new project

https://docs.nillion.com/nada

1. Create an rps nada project

```
nada init rps
```

2. Go into the rps folder

```
cd rps
```

3. Write the RPS program in main.py (if you get stuck, check nada/src/main.py)

- Initialize 2 parties: computer and player

```
party_computer = Party(name="Computer")
party_player = Party(name="Player")
```

- Add each player's choice as a named SecretInput

```
choice_computer = SecretInteger(Input(name="choice_computer", party=party_computer))
choice_player_2 = SecretInteger(Input(name="choice_player_2", party=party_player))

```

- Adjust choice values (original secrets can't be 0 values)

```
adjusted_choice_computer = (choice_computer - Integer(10)) % Integer(3)
adjusted_choice_player_2 = (choice_player_2 - Integer(10)) % Integer(3)
```

- Compute result

```
result = (adjusted_choice_computer - adjusted_choice_player_2 + Integer(3)) % Integer(3)
```

- Determine winner

```
winner = (
    (result > Integer(0)).if_else(
        (result > Integer(1)).if_else(Integer(2), Integer(1)),
        Integer(0)
    )
)
```

- Create an output variable

```
out = Output(winner, "game_result", party_computer)
```

- Return the output

```
return [out]
```

4. Build (compile) the program

```
nada build
```

5. Generate a test file

```
nada generate-test --test-name test_r_p main
```

6. Modify and run test

```
nada test test_r_p
```

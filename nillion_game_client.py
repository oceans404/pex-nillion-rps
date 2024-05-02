import asyncio
import random
import string
import os
import py_nillion_client as nillion
from helpers.nillion_client_helper import create_nillion_client
from helpers.nillion_keypath_helper import getUserKeyFromFile, getNodeKeyFromSeed

from dotenv import load_dotenv
load_dotenv()

def map_rps_to_number(choice):
    if choice == "rock":
        return 10
    elif choice == "paper":
        return 11
    elif choice == "scissors":
        return 12
    else:
        raise ValueError("Invalid input. Choice must be 'rock', 'paper', or 'scissors'.")

def get_random_seed():
    random_seed = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return random_seed


async def determine_game_result(player_choice, callback):
    async def game_logic():
        # Simulate network delay or heavy computation
        await asyncio.sleep(2)  # Delay for 2 seconds
        computer_choice = random.choice(['rock', 'paper', 'scissors'])

        cluster_id = os.getenv("NILLION_CLUSTER_ID")
        print('cluster_id', cluster_id)
        userkey = os.getenv("NILLION_USERKEY_PATH_PARTY_1")
        print('userkey', userkey)
        client_1 = create_nillion_client(
            getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_1")), getNodeKeyFromSeed(get_random_seed())
        )
        party_id_1 = client_1.party_id()
        user_id_1 = client_1.user_id()

        program_mir_path = "./nada/target/main.nada.bin"
        program_name = "rps"

        # 1st Party stores program
        action_id = await client_1.store_program(
            cluster_id, program_name, program_mir_path
        )

        program_id = f"{user_id_1}/{program_name}"
        print('Stored program. action_id:', action_id)
        print('Stored program_id:', program_id)

        ############################# Player 1 stores choice
        stored_secret_1 = nillion.Secrets({
            "choice_computer": nillion.SecretInteger(map_rps_to_number(computer_choice))
        })

        secret_bindings_1 = nillion.ProgramBindings(program_id)
        secret_bindings_1.add_input_party('Computer', party_id_1)

        store_id_1 = await client_1.store_secrets(
            cluster_id, secret_bindings_1, stored_secret_1, None
        )

        print('store_id_1', store_id_1)

        ############################# Player 2 stores choice

        client_2 = create_nillion_client(
            getUserKeyFromFile(os.getenv("NILLION_USERKEY_PATH_PARTY_2")), getNodeKeyFromSeed(get_random_seed())
        )

        party_id_2 = client_2.party_id()
        user_id_2 = client_2.user_id()

        stored_secret_2 = nillion.Secrets({
            "choice_player_2": nillion.SecretInteger(map_rps_to_number(player_choice))
        })

        secret_bindings_2 = nillion.ProgramBindings(program_id)
        secret_bindings_2.add_input_party('Player', party_id_2)

        # Create permissions object
        permissions = nillion.Permissions.default_for_user(user_id_2)

        # Give compute permissions to the first party
        compute_permissions = {
            user_id_1: {program_id},
        }
        permissions.add_compute_permissions(compute_permissions)

        # Store the permissioned secret
        store_id_2 = await client_2.store_secrets(
            cluster_id, secret_bindings_2, stored_secret_2, permissions
        )

        print("store_id_2", store_id_2)

        compute_bindings = nillion.ProgramBindings(program_id)
        compute_bindings.add_input_party('Computer', party_id_1)
        compute_bindings.add_input_party('Player', party_id_2)
        compute_bindings.add_output_party('Computer', party_id_1)

        compute_id = await client_1.compute(
            cluster_id,
            compute_bindings,
            [store_id_1, store_id_2],
            nillion.Secrets({}),
            nillion.PublicVariables({}),
        )

        print(f"The computation was sent to the network. compute_id: {compute_id}")
        while True:
            compute_event = await client_1.next_compute_event()
            if isinstance(compute_event, nillion.ComputeFinishedEvent):
                print(f"✅  Compute complete for compute_id {compute_event.uuid}")
                print(f"🖥️  The result is {compute_event.result.value}")

                compute_result = compute_event.result.value['game_result']
                print(compute_result)
                # Determine result
                if compute_result == 0:
                    result = 'Tie'
                elif (compute_result == 1):
                    result = 'Computer Wins!'
                else:
                    result = 'Player Wins!'

                # Callback with rps game results
                callback(computer_choice, result)

    # Start the asyncio event loop
    asyncio.create_task(game_logic())

import random


def create():
    """create the initial pile"""
    pile = []
    for i in range(6 + 1):
        for j in range(6 + 1):
            if i <= j:
                pile.append([i, j])
    return pile


def check_order(computer, player):
    while len(computer) == len(player) == 0:
        game_start(create())  # referring to both player and computer do not have a pair
    if len(computer) == 0:
        status = "player to go"
    elif len(player) == 0:
        status = "computer to go"
    elif computer < player:
        status = "player to go"
    elif player < computer:
        status = "computer to go"
    return status


def check_draw(current_status_list):
    if current_status_list[0][0] == current_status_list[-1][-1] and len(current_status_list) != 0:
        count = 0
        for i in current_status_list:
            for j in i:
                if j == current_status_list[0][0]:
                    count += 1
        if count >= 8:
            return True
        else:
            return False
    elif len(current_status_list) == 0:
        return True
    else:
        return False


def switch_turn(turn):
    if turn == "player to go":
        return "computer to go"
    else:
        return "player to go"


def print_current_status(stock_pieces, computer_pieces):
    print("=" * 70)
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}")
    print()


def validate_player(pieces, index, domino_snake):
    if index > 0:
        if pieces[index - 1][0] == domino_snake[-1][-1]:
            return True
        elif pieces[index - 1][-1] == domino_snake[-1][-1]:
            return True
    elif index < 0:
        if pieces[abs(index) - 1][-1] == domino_snake[0][0]:
            return True
        elif pieces[abs(index) - 1][0] == domino_snake[0][0]:
            return True
    elif index == 0:
        return True
    return False


def validate_computer_right(element, domino_snake):
    if element[0] == domino_snake[-1][-1]:
        return 1
    elif element[-1] == domino_snake[-1][-1]:
        return 2
    return False


def validate_computer_left(element, domino_snake):
    if element[-1] == domino_snake[0][0]:
        return 1
    elif element[0] == domino_snake[0][0]:
        return 2
    return False


def computer_move(domino_snake, input_list):
    for i in input_list:
        if validate_computer_right(i, domino_snake):
            if validate_computer_right(i, domino_snake) == 1:
                pass
            else:
                i.reverse()
            return [i, "right"]
        elif validate_computer_left(i, domino_snake):
            if validate_computer_left(i, domino_snake) == 1:
                pass
            else:
                i.reverse()
            return [i, "left"]
    return False


def estimate_score(domino_snake, input_list):
    score_count = {i:0 for i in range(6 + 1)}

    for i in domino_snake:
        for j in i:
            score_count[j] += 1

    for i in input_list:
        for j in i:
            score_count[j] += 1

    temp_list = [[score_count[i], score_count[j]] for [i, j] in input_list]
    temp_list = [sum(i) for i in temp_list]

    input_list_with_score = [input_list[i] + [temp_list[i]] for i in range(len(input_list))]
    input_list_with_score = sorted(input_list_with_score, key=lambda x: x[-1], reverse=True)

    for i in input_list_with_score:
        i.pop()

    return input_list_with_score


def game_start(pile):
    # generate piles for player and computer
    random.shuffle(pile)
    domino_snake = []
    computer_pieces = pile[:7]
    player_pieces = pile[8:15]
    stock_pieces = [i for i in pile if i not in computer_pieces and i not in player_pieces]

    # define who should play first
    computer_first = sorted([i for i in computer_pieces if i[0] == i[1]], reverse=True)
    player_first = sorted([i for i in player_pieces if i[0] == i[1]], reverse=True)
    status = check_order(computer_first, player_first)

    # the side who play first will throw out the first domingo and then switch turn after that
    if status == "player to go":
        domino_snake.append(player_first[0])
        player_pieces = [i for i in player_pieces if i != player_first[0]]
    elif status == "computer to go":
        domino_snake.append(computer_first[0])
        computer_pieces = [i for i in computer_pieces if i != computer_first[0]]
    status = switch_turn(status)

    while len(computer_pieces) != 0 and len(player_pieces) != 0:
        # check draw conditions first
        if check_draw(domino_snake):
            print("Status: The game is over. It's a draw!")
            break
        else:
            # Non-draw conditions need continue
            # Print the facts first.
            print_current_status(stock_pieces, computer_pieces)

            if len(domino_snake) <= 6:
                for i in domino_snake:
                    print(i, end="")
                print()
            else:
                print(
                    f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}{domino_snake[-1]}")
            print()
            print("Your pieces:")
            for i in player_pieces:
                print(f"{player_pieces.index(i) + 1}:{i}")
            print()

            if status == "player to go":
                input_limitation = [i for i in range(1, len(player_pieces) + 1)]
                input_limitation.extend([-i for i in input_limitation])
                input_limitation = [str(i) for i in input_limitation]
                input_limitation.append("0")
                next_step = input("Status: It's your turn to make a move. Enter your command.\n")
                while next_step not in input_limitation or not validate_player(player_pieces, int(next_step), domino_snake):
                    if next_step not in input_limitation:
                        next_step = input("Invalid input. Please try again.\n")
                    else:
                        next_step = input("Illegal move. Please try again.\n")
                next_step = int(next_step)
                if next_step > 0:
                    if player_pieces[next_step - 1][0] == domino_snake[-1][-1]:
                        pass
                    else:
                        player_pieces[next_step - 1] = [player_pieces[next_step - 1][-1],
                                                        player_pieces[next_step - 1][0]]
                    domino_snake.append(player_pieces[next_step - 1])
                elif next_step == 0:
                    draw_from_pile = random.choice(stock_pieces)
                    player_pieces.append(draw_from_pile)
                    stock_pieces.remove(draw_from_pile)
                else:
                    if player_pieces[abs(next_step) - 1][-1] == domino_snake[0][0]:
                        pass
                    else:
                        player_pieces[abs(next_step) - 1] = [player_pieces[abs(next_step) - 1][-1],
                                                             player_pieces[abs(next_step) - 1][0]]
                    domino_snake.insert(0, player_pieces[abs(next_step) - 1])
                player_pieces = [i for i in player_pieces if i not in domino_snake]
                status = switch_turn(status)
            elif status == "computer to go":
                fake_input = input("Status: Computer is about to make a move. Press Enter to continue...\n")
                # change below here
                computer_pieces = estimate_score(domino_snake, computer_pieces)
                calculated_move = computer_move(domino_snake, computer_pieces)
                if calculated_move:
                    if calculated_move[-1] == "right":
                        domino_snake.append(calculated_move[0])
                    elif calculated_move[-1] == "left":
                        domino_snake.insert(0, calculated_move[0])
                    computer_pieces.remove(calculated_move[0])
                else:
                    draw_from_pile = random.choice(stock_pieces)
                    computer_pieces.append(draw_from_pile)
                    stock_pieces.remove(draw_from_pile)

                status = switch_turn(status)

    # claim victory and game over
    if len(computer_pieces) == 0 or len(player_pieces) == 0:
        print("=" * 70)
        print(f"Stock size: {len(stock_pieces)}")
        print(f"Computer pieces: {len(computer_pieces)}")
        print()
        if len(domino_snake) <= 6:
            for i in domino_snake:
                print(i, end="")
            print()
        else:
            print(
                f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}{domino_snake[-1]}")
        print()
        print("Your pieces:")
        for i in player_pieces:
            print(f"{player_pieces.index(i) + 1}:{i}")
        print()
        if len(computer_pieces) == 0:
            print("Status: The game is over. The computer won!")
        else:
            print("Status: The game is over. You won!")


game_start(create())

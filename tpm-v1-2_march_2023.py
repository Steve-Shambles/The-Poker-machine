"""
The Poker Machine V1.2,
Windows and linux compatable version
Steve Shambles Sept-Dec 2019 revisited March 2023
"""
# All imports are from the standard library.
from collections import defaultdict
from random import randrange
import sys
import time
from tkinter import Tk, Button, Label, LabelFrame, PhotoImage
from tkinter import messagebox, DISABLED, NORMAL, Menu, E, W
from tkinter import Toplevel, INSERT, scrolledtext
import webbrowser


class Pok:
    """Variables, set at defaults for global use.
       Add Pok. to each var then its effectively global."""
    btn1_held = None
    btn2_held = None
    btn3_held = None
    btn4_held = None
    btn5_held = None

    card_one = 'blank'
    card_two = 'blank'
    card_three = 'blank'
    card_four = 'blank'
    card_five = 'blank'

    high_score = 0

    hold_btn1 = None
    hold_btn2 = None
    hold_btn3 = None
    hold_btn4 = None
    hold_btn5 = None

    no_card_holding = True

    plyr_credits = 100
    plyr_winnings = 0
    plyr_stake = 1

    ranks = ''
    stake_btn = None
    suits = ''

# GUI.
root = Tk()
root.title('The Poker Machine V1.2')

# Frame for pay table display.
pay_table_frame = LabelFrame(root)
pay_table_frame.grid(row=0, column=0)

# Load in and display paytable image.
pay_table_lbl = Label(pay_table_frame)
PHOTO = PhotoImage(file=r'cards/pay-table-bg-386x200.png')
pay_table_lbl.config(image=PHOTO)
pay_table_lbl.grid(row=0, column=0, padx=2, pady=2)
pay_table_lbl.photo = PHOTO

# Frame for messages display.
msg_frame = LabelFrame(root)
msg_frame.grid(row=1, column=0)

# Startup message.
msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                text='Please choose stake, and then click Deal.')
msg_lbl.grid(row=1, column=0)

# Frame for the card images.
cards_frame = LabelFrame(root)
cards_frame.grid(row=2, column=0)

# Frame for bank display.
bank_frame = LabelFrame(root)
bank_frame.grid(row=4, column=0, sticky=W+E)

# Frame for high score display.
high_score_frame = LabelFrame(root)
high_score_frame.grid(row=5, column=0, sticky=W+E)

# Frame for result display.
result_frame = LabelFrame(root)
result_frame.grid(row=6, column=0, sticky=W+E)


def load_high_score():
    """Load back the high score variable from file
       and store in Pok.high_score."""

    with open(r'cards/high-score.txt', 'r') as contents:
        SAVED_HIGH_SCORE = contents.read()
        if SAVED_HIGH_SCORE > '':
            Pok.high_score = int(SAVED_HIGH_SCORE)

# Need to call the high score def here.
load_high_score()


def game_over():
    """play again y-n msg box."""
    quest = messagebox.askyesno('Video Poker',
                                'game over you went broke.\n'
                                'Would you like to play a new game?')

    if quest:
        # Start new game. Re-initialise hand variables.
        hand = [Pok.card_one, Pok.card_two, Pok.card_three,
                Pok.card_four, Pok.card_five]
        hand_value = check_hand(hand)
        Pok.plyr_credits = 100
        Pok.plyr_winnings = 0
        # Do not use update_high_score() here, causes problems.
        high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                               text='High Score: $'+str(Pok.high_score)+'     ')
        high_score_lbl.grid(row=4, column=0)

        start_game()
        return

    else:
        # Quit program completely.
        root.destroy()
        sys.exit()


def save_high_score():
    """Save current score to file if it beats previous highscore."""
    with open(r'cards/high-score.txt', 'w') as contents:
        if Pok.plyr_credits < Pok.high_score:
            return

        SAVE_IT = str(Pok.plyr_credits)
        contents.write(SAVE_IT)


def update_high_score():
    """Update high score label."""
    high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                           text='High Score: $'+str(Pok.high_score)+'     ')
    high_score_lbl.grid(row=4, column=0)
    save_high_score()


def update_bank():
    """Update bank label."""
    bank_lbl = Label(bank_frame, font=('Helvetica', 10, 'bold'),
                     text='Bank: $'+str(Pok.plyr_credits)+'  ')
    bank_lbl.grid(row=3, column=0)

    # Check if current bank beats highscore, if so then update.
    if Pok.plyr_credits > Pok.high_score:
        Pok.high_score = Pok.plyr_credits
        update_high_score()


# Holding cards related.
def disable_hold_btns():
    """De-activate hold buttons."""
    Pok.hold_btn1.configure(state=DISABLED)
    Pok.hold_btn2.configure(state=DISABLED)
    Pok.hold_btn3.configure(state=DISABLED)
    Pok.hold_btn4.configure(state=DISABLED)
    Pok.hold_btn5.configure(state=DISABLED)
    Pok.no_card_holding = True


def enable_hold_btns():
    """Activate hold buttons."""
    Pok.hold_btn1.configure(state=NORMAL)
    Pok.hold_btn2.configure(state=NORMAL)
    Pok.hold_btn3.configure(state=NORMAL)
    Pok.hold_btn4.configure(state=NORMAL)
    Pok.hold_btn5.configure(state=NORMAL)
    Pok.no_card_holding = False


def hold_card1():
    """Check if can hold or unhold card one, if so toogle it and update it."""
    # No holds allowed yet so return.
    if Pok.no_card_holding:
        return

    # Toggle boolean, so if held, unhold, and vice versa.
    Pok.btn1_held = not Pok.btn1_held #Cool!

    load_file = 'cards/hold-btn.png'
    if Pok.btn1_held:
        load_file = 'cards/held-btn.png'

    Pok.hold_btn1 = Button(cards_frame, width=68, height=35,
                           command=hold_card1)
    hold_image1 = PhotoImage(file=load_file)
    Pok.hold_btn1.config(image=hold_image1)
    Pok.hold_btn1.image = hold_image1
    Pok.hold_btn1.grid(row=1, column=0, padx=2, pady=2)


def hold_card2():
    """Check if can hold or unhold card 2."""
    if Pok.no_card_holding:
        return

    Pok.btn2_held = not Pok.btn2_held

    load_file = 'cards/hold-btn.png'
    if Pok.btn2_held:
        load_file = 'cards/held-btn.png'

    Pok.hold_btn2 = Button(cards_frame, width=68, height=35, command=hold_card2)
    hold_image2 = PhotoImage(file=load_file)
    Pok.hold_btn2.config(image=hold_image2)
    Pok.hold_btn2.image = hold_image2
    Pok.hold_btn2.grid(row=1, column=1, padx=2, pady=2)


def hold_card3():
    """Check if can hold or unhold card 3."""
    if Pok.no_card_holding:
        return

    Pok.btn3_held = not Pok.btn3_held

    load_file = 'cards/hold-btn.png'
    if Pok.btn3_held:
        load_file = 'cards/held-btn.png'

    Pok.hold_btn3 = Button(cards_frame, width=68, height=35, command=hold_card3)
    hold_image3 = PhotoImage(file=load_file)
    Pok.hold_btn3.config(image=hold_image3)
    Pok.hold_btn3.image = hold_image3
    Pok.hold_btn3.grid(row=1, column=2, padx=2, pady=2)


def hold_card4():
    """Check if can hold or unhold card 4."""
    if Pok.no_card_holding:
        return

    Pok.btn4_held = not Pok.btn4_held

    load_file = 'cards/hold-btn.png'
    if Pok.btn4_held:
        load_file = 'cards/held-btn.png'

    Pok.hold_btn4 = Button(cards_frame, width=68, height=35, command=hold_card4)
    hold_image4 = PhotoImage(file=load_file)
    Pok.hold_btn4.config(image=hold_image4)
    Pok.hold_btn4.image = hold_image4
    Pok.hold_btn4.grid(row=1, column=3, padx=2, pady=2)


def hold_card5():
    """Check if can hold or unhold card 5."""
    if Pok.no_card_holding:
        return

    Pok.btn5_held = not Pok.btn5_held

    load_file = 'cards/hold-btn.png'
    if Pok.btn5_held:
        load_file = 'cards/held-btn.png'

    Pok.hold_btn5 = Button(cards_frame, width=68, height=35, command=hold_card5)
    hold_image5 = PhotoImage(file=load_file)
    Pok.hold_btn5.config(image=hold_image5)
    Pok.hold_btn5.image = hold_image5
    Pok.hold_btn5.grid(row=1, column=4, padx=2, pady=2)


def reset_hold_btns():
    """If any hold buttons are in the held state, then unhold them to reset."""
    if Pok.btn1_held:
        hold_card1()
    if Pok.btn2_held:
        hold_card2()
    if Pok.btn3_held:
        hold_card3()
    if Pok.btn4_held:
        hold_card4()
    if Pok.btn5_held:
        hold_card5()


def display_cards():
    """Display images of cards using buttons."""
    # Set the pause length between dealt cards.
    deal_pause = .10

    # Dont pause between cards being dealt if dealing first 5 face down.
    if Pok.card_one == 'blank':
        deal_pause = 0

    card1 = Pok.card_one+'.png' # Card image filename.
    card2 = Pok.card_two+'.png'
    card3 = Pok.card_three+'.png'
    card4 = Pok.card_four+'.png'
    card5 = Pok.card_five+'.png'

    # Dont show card again if held, unless printing blank.
    if not Pok.btn1_held or deal_pause == 0:
        card1_btn = Button(cards_frame, command=hold_card1)
        PHOTO = PhotoImage(file=r'cards/'+str(card1))
        card1_btn.config(image=PHOTO)
        card1_btn.grid(row=0, column=0, padx=2, pady=2)
        card1_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn2_held or deal_pause == 0:
        card2_btn = Button(cards_frame, command=hold_card2)
        PHOTO = PhotoImage(file=r'cards/'+str(card2))
        card2_btn.config(image=PHOTO)
        card2_btn.grid(row=0, column=1, padx=2, pady=2)
        card2_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn3_held or deal_pause == 0:
        card3_btn = Button(cards_frame, command=hold_card3)
        PHOTO = PhotoImage(file=r'cards/'+str(card3))
        card3_btn.config(image=PHOTO)
        card3_btn.grid(row=0, column=2, padx=2, pady=2)
        card3_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn4_held or deal_pause == 0:
        card4_btn = Button(cards_frame, command=hold_card4)
        PHOTO = PhotoImage(file=r'cards/'+str(card4))
        card4_btn.config(image=PHOTO)
        card4_btn.grid(row=0, column=3, padx=2, pady=2)
        card4_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()

    if not Pok.btn5_held or deal_pause == 0:
        card5_btn = Button(cards_frame, command=hold_card5)
        PHOTO = PhotoImage(file=r'cards/'+str(card5))
        card5_btn.config(image=PHOTO)
        card5_btn.grid(row=0, column=4, padx=2, pady=2)
        card5_btn.photo = PHOTO
        time.sleep(deal_pause)
        cards_frame.update()


def check_winnings():
    """Check how much, if anything, player has won."""
    hand_value = check_hand(hand)
    Pok.plyr_credits = Pok.plyr_credits + Pok.plyr_winnings
    update_bank()


def deal_btn_clkd():
    """When deal btn is clicked. After initial game setup, program waits here
       so that stake can be changed if required. When deal is eventually
       clicked we then move onto holds and the draw btn."""

    # Make sure credits are >= to stake.
    if Pok.plyr_stake > Pok.plyr_credits:
        messagebox.showinfo('Video Poker', 'Not enough credits\n'
                            'to play this stake.\n\n'
                            'Please lower your stake to continue.')
        return
    deal_btn.configure(state=DISABLED)
    Pok.stake_btn.configure(state=DISABLED)
    clear_msg_box()

    # Choose 5 rnd cards and then show them face up.
    get_rnd_hand()
    display_cards()

    # Configure GUI.
    enable_hold_btns()
    Pok.no_card_holding = False

    # Find best hand.
    hand = [Pok.card_one, Pok.card_two, Pok.card_three, Pok.card_four, Pok.card_five]
    hand_value = check_hand(hand)
    best_hand = (hand_dict.get(hand_value))

    if not best_hand:
        best_hand = 'No Win'

    # Display what is the best available hand in msg window.
    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='You have been dealt: '+str(best_hand))
    msg_lbl.grid(row=1, column=0)

    # Remove stake from bank and update new total.
    Pok.plyr_credits = Pok.plyr_credits - Pok.plyr_stake
    update_bank()

    draw_btn.configure(state=NORMAL)


def clear_msg_box():
    """Clears msg box with 90 blank spaces."""
    msg_lbl = Label(msg_frame, text=' ' *90)
    msg_lbl.grid(row=1, column=0)


def draw_btn_clkd():
    """Bet is placed, so now only holds and draw btn can be clicked."""
    draw_btn.configure(state=DISABLED)
    clear_msg_box()
    get_rnd_card_if_not_held()
    display_cards()

    # Store all five cards in hand[] list.
    hand = [Pok.card_one, Pok.card_two, Pok.card_three, Pok.card_four, Pok.card_five]

    # Check hand for wins.
    hand_value = check_hand(hand)
    best_hand = (hand_dict.get(hand_value))

    if not best_hand:
        best_hand = 'No Win'
    # Print best hand is in msg window and check how much won, if anything.
    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='Result: '+str(best_hand))
    msg_lbl.grid(row=1, column=0)
    check_winnings()

    # Print win, or not, in mesgbox pop up.
    added_text = 'No win this time.\n\nYou lost $'+str(Pok.plyr_stake)+'\n\nPlease try again!'
    if Pok.plyr_winnings:
        winning_hand = str((hand_dict.get(hand_value)))
        added_text = 'Congratulations. You won $'  \
         +str(Pok.plyr_winnings)+'\nFor '+str(winning_hand)

    messagebox.showinfo('The Poker Machine', added_text)

    # Start new hand, reset gui, winnings ,msg area etc.
    disply_blanks()
    reset_hold_btns()
    disable_hold_btns()

    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text='Please choose stake, and then click Deal.')
    msg_lbl.grid(row=1, column=0)

    Pok.plyr_winnings = 0

    # Check there is enough in bank
    if Pok.plyr_credits <= 0:
        game_over()
        return

    deal_btn.configure(state=NORMAL)
    Pok.stake_btn.configure(state=NORMAL)


def update_stake():
    """Update stake amount image button when changed, 1-5."""
    load_file = 'cards/stake-btn'+str(Pok.plyr_stake)+'.png'

    Pok.stake_btn = Button(cards_frame, width=68, height=35, command=bet_one)
    stake_image = PhotoImage(file=load_file)
    Pok.stake_btn.config(image=stake_image)
    Pok.stake_btn.image = stake_image
    Pok.stake_btn.grid(row=2, column=0, padx=2, pady=2)


def bet_one():
    """Change stake amount, $1 to $5."""
    if Pok.plyr_stake == 5: #roll around to 1 if = 5.
        Pok.plyr_stake = 1
        update_stake()
        return

    Pok.plyr_stake += 1
    update_stake()


def get_rnd_hand():
    """Select 5 different random cards for a new game."""
    # Ranks list.
    Pok.ranks = ['2H', '2D', '2C', '2S', '3H', '3D', '3C', '3S',
                 '4H', '4D', '4C', '4S', '5H', '5D', '5C', '5S',
                 '6H', '6D', '6C', '6S', '7H', '7D', '7C', '7S',
                 '8H', '8D', '8C', '8S', '9H', '9D', '9C', '9S',
                 'TH', 'TD', 'TC', 'TS', 'JH', 'JD', 'JC', 'JS',
                 'QH', 'QD', 'QC', 'QS', 'KH', 'KD',
                 'KC', 'KS', 'AH', 'AD', 'AC', 'AS']

    # Choose a rnd card for card one.
    card_one_rank = randrange(len(Pok.ranks))
    Pok.card_one = (Pok.ranks[card_one_rank])
    # Delete the chosen card from the list so cant be picked again this hand.
    del Pok.ranks[card_one_rank]

    card_two_rank = randrange(len(Pok.ranks))
    Pok.card_two = (Pok.ranks[card_two_rank])
    del Pok.ranks[card_two_rank]

    card_three_rank = randrange(len(Pok.ranks))
    Pok.card_three = (Pok.ranks[card_three_rank])
    del Pok.ranks[card_three_rank]

    card_four_rank = randrange(len(Pok.ranks))
    Pok.card_four = (Pok.ranks[card_four_rank])
    del Pok.ranks[card_four_rank]

    card_five_rank = randrange(len(Pok.ranks))
    Pok.card_five = (Pok.ranks[card_five_rank])
    del Pok.ranks[card_five_rank]

    # Check for duplicate card, if one found do the lot again:get_rnd_hand().
    if Pok.card_one == Pok.card_two or Pok.card_one == Pok.card_three or  \
       Pok.card_two == Pok.card_three or Pok.card_one == Pok.card_four or  \
       Pok.card_two == Pok.card_four or Pok.card_three == Pok.card_four or  \
       Pok.card_one == Pok.card_five or Pok.card_two == Pok.card_five or   \
       Pok.card_three == Pok.card_five or  Pok.card_four == Pok.card_five:
        #calls itself to do this def again from start,if dup.
        get_rnd_hand()


def get_rnd_card_if_not_held():
    """If card is not held, and draw is clicked, get new rnd card."""
    if not Pok.btn1_held:
        # Choose rnd card for card one.
        card_one_rank = randrange(len(Pok.ranks))
        Pok.card_one = (Pok.ranks[card_one_rank])

    if not Pok.btn2_held:
        card_two_rank = randrange(len(Pok.ranks))
        Pok.card_two = (Pok.ranks[card_two_rank])

    if not Pok.btn3_held:
        card_three_rank = randrange(len(Pok.ranks))
        Pok.card_three = (Pok.ranks[card_three_rank])

    if not Pok.btn4_held:
        card_four_rank = randrange(len(Pok.ranks))
        Pok.card_four = (Pok.ranks[card_four_rank])

    if not Pok.btn5_held:
        card_five_rank = randrange(len(Pok.ranks))
        Pok.card_five = (Pok.ranks[card_five_rank])

    #check for duplicate card, if one found do the lot again:get_rnd_hand()
    if Pok.card_one == Pok.card_two or Pok.card_one == Pok.card_three or  \
        Pok.card_two == Pok.card_three or Pok.card_one == Pok.card_four or  \
        Pok.card_two == Pok.card_four or Pok.card_three == Pok.card_four or  \
        Pok.card_one == Pok.card_five or Pok.card_two == Pok.card_five or   \
        Pok.card_three == Pok.card_five or  Pok.card_four == Pok.card_five:
        get_rnd_card_if_not_held()


# Hand check.
# Original hand detect functions from:
# https:\briancaffey.github.io/2018/01/02/checking-poker-hands-with-python.html
# I added royal flush check and made minimum jacks or better rather than pair.
def check_royal_flush(hand):
    """My take on how to check for royal flush."""
    if check_flush(hand) and check_straight(hand):
        # Check for akqjt.
        values = [i[0] for i in hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
            if set(values) == set(['T', 'J', 'Q', 'K', 'A']):
                return True
    else:
        return False


def check_straight_flush(hand):
    """Check for straight flush."""
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False


def check_four_of_a_kind(hand):
    """Check for 4 of a kind."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 4]:
        four_of_a_kind = True
        return True
    return False


def check_full_house(hand):
    """Check for full house."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        return True
    return False


def check_flush(hand):
    """Check for flush."""
    Pok.suits = [i[1] for i in hand]
    if len(set(Pok.suits)) == 1:
        return True
    else:
        return False


def check_straight(hand):
    """Check for straight."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    rank_values = [card_order_dict[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        return True
    else:
        # Check for straight with low Ace.
        if set(values) == set(['A', '2', '3', '4', '5']):
            return True
        return False


def check_three_of_a_kind(hand):
    """Check for 3 of a kind."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if set(value_counts.values()) == set([3, 1]):
        return True
    else:
        return False


def check_two_pairs(hand):
    """Check for 2 pair."""
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 2, 2]:
        return True
    else:
        return False


def check_one_pairs(hand):
    """Check for a pair of jacks, queens, kings or aces, reject lower pairs."""
    # Reset check for winning pairs.
    pair_aces = 0
    pair_kings = 0
    pair_queens = 0
    pair_jacks = 0

    values = [i[0] for i in hand]

    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1

        if v == 'A':
            pair_aces += 1
            if pair_aces == 2:
                return True

        if v == 'K':
            pair_kings += 1
            if pair_kings == 2:
                return True

        if v == 'Q':
            pair_queens += 1
            if pair_queens == 2:
                return True

        if v == 'J':
            pair_jacks += 1
            if pair_jacks == 2:
                return True

    else:
        return False


def check_hand(hand):
    """Check hand to find best win and how much to pay out."""
    if hand[0] == 'blank':
        return

    if check_royal_flush(hand):
        Pok.plyr_winnings = Pok.plyr_stake *800
        return 10
    if check_straight_flush(hand):
        Pok.plyr_winnings = Pok.plyr_stake *50
        return 9
    if check_four_of_a_kind(hand):
        Pok.plyr_winnings = Pok.plyr_stake *25
        return 8
    if check_full_house(hand):
        Pok.plyr_winnings = Pok.plyr_stake *9
        return 7
    if check_flush(hand):
        Pok.plyr_winnings = Pok.plyr_stake *6
        return 6
    if check_straight(hand):
        Pok.plyr_winnings = Pok.plyr_stake *4
        return 5
    if check_three_of_a_kind(hand):
        Pok.plyr_winnings = Pok.plyr_stake *3
        return 4
    if check_two_pairs(hand):
        Pok.plyr_winnings = Pok.plyr_stake *2
        return 3
    if check_one_pairs(hand):
        Pok.plyr_winnings = Pok.plyr_stake #stake back
        return 2
    else:
        Pok.plyr_winnings = 0
    return 0 #high card, loser, min win is a pair


# These 2 dictionaries are used only for checking for the best hand.
card_order_dict = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
                   '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

hand_dict = {10:'Royal Flush', 9:'Straight-Flush', 8:'Four-Of-A-Kind',
             7:'Full-House', 6:'Flush', 5:'Straight',
             4:'Three-Of-A-Kind', 3:'Two-Pairs', 2:'One-Pair', 1:'High-Card'}


# One off gui build at start up, has to be placed here because the functions
# it calls need to be above it.

# Create stake, draw and deal buttons.
load_file = 'cards/stake-btn1.png'

Pok.stake_btn = Button(cards_frame, width=68, height=35, command=bet_one)
stake_image = PhotoImage(file=load_file)
Pok.stake_btn.config(image=stake_image)
Pok.stake_btn.image = stake_image
Pok.stake_btn.grid(row=2, column=0, padx=2, pady=2)

draw_btn = Button(cards_frame, width=68, height=35, command=draw_btn_clkd)
draw_image = PhotoImage(file=r'cards/draw-btn.png')
draw_btn.config(image=draw_image)
draw_btn.image = draw_image
draw_btn.grid(row=2, column=3, padx=2, pady=2)

deal_btn = Button(cards_frame, width=68, height=35, command=deal_btn_clkd)
deal_image = PhotoImage(file=r'cards/deal-btn.png')
deal_btn.config(image=deal_image)
deal_btn.image = deal_image
deal_btn.grid(row=2, column=4, padx=2, pady=2)


# Other defs that can be hidden out of the away here.
def set_hold_btns():
    """Load and display hold buttons."""
    Pok.hold_btn1 = Button(cards_frame, width=68, height=35, command=hold_card1)
    hold_image1 = PhotoImage(file='cards/hold-btn.png')
    Pok.hold_btn1.config(image=hold_image1)
    Pok.hold_btn1.image = hold_image1
    Pok.hold_btn1.grid(row=1, column=0, padx=2, pady=2)

    Pok.hold_btn2 = Button(cards_frame, width=68, height=35, command=hold_card2)
    hold_image2 = PhotoImage(file='cards/hold-btn.png')
    Pok.hold_btn2.config(image=hold_image2)
    Pok.hold_btn2.image = hold_image2
    Pok.hold_btn2.grid(row=1, column=1, padx=2, pady=2)

    Pok.hold_btn3 = Button(cards_frame, width=68, height=35, command=hold_card3)
    hold_image3 = PhotoImage(file='cards/hold-btn.png')
    Pok.hold_btn3.config(image=hold_image3)
    Pok.hold_btn3.image = hold_image3
    Pok.hold_btn3.grid(row=1, column=2, padx=2, pady=2)

    Pok.hold_btn4 = Button(cards_frame, width=68, height=35, command=hold_card4)
    hold_image4 = PhotoImage(file='cards/hold-btn.png')
    Pok.hold_btn4.config(image=hold_image4)
    Pok.hold_btn4.image = hold_image4
    Pok.hold_btn4.grid(row=1, column=3, padx=2, pady=2)

    Pok.hold_btn5 = Button(cards_frame, width=68, height=35, command=hold_card5)
    hold_image5 = PhotoImage(file='cards/hold-btn.png')
    Pok.hold_btn5.config(image=hold_image5)
    Pok.hold_btn5.image = hold_image5
    Pok.hold_btn5.grid(row=1, column=4, padx=2, pady=2)


def disply_blanks():
    """For new game start, show cards face down."""
    Pok.card_one = 'blank'
    Pok.card_two = 'blank'
    Pok.card_three = 'blank'
    Pok.card_four = 'blank'
    Pok.card_five = 'blank'
    display_cards()


def about_menu():
    """Msgbox Info about this program."""
    messagebox.showinfo('Program Information', 'The Poker Machine V1.2\n'
                        'For Windows and Linux.\n\n'
                        'Written in Python 3.\n\n'
                        'Freeware.\nBy Steve Shambles.\n\n'
                        'March 2023')


def display_help_text():
    """Show help text in a scrolled text box in a child window."""
    helptext_frame = Toplevel(root)
    helptext_frame.grid()

    help_text = scrolledtext.ScrolledText(helptext_frame, bg='skyblue',
                                          fg='black', width=78, height=30)
    help_text.grid()

    with open(r'cards/tpm-help.txt', 'r') as f:
        text_contents = f.read()
        help_text.insert(INSERT, text_contents)


def donate_me():
    """User splashes the cash here!"""
    webbrowser.open("https:\\paypal.me/photocolourizer")


def visit_github():
    """View source code and my other Python projects at GitHub."""
    webbrowser.open("https://github.com/steve-shambles")


def quit_prog():
    ask_yn = messagebox.askyesno('The Poker Machine',
                                 'Are you sure you want to exit?')
    if ask_yn:
        root.destroy()
        sys.exit()

# Drop-down menu.
MENU_BAR = Menu(root)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Menu', menu=FILE_MENU)
FILE_MENU.add_command(label='Help', command=display_help_text)
FILE_MENU.add_command(label='About', command=about_menu)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='Python source code on GitHub',
                      command=visit_github)
FILE_MENU.add_command(label='Make a small donation via PayPal',
                      command=donate_me)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='Exit', command=quit_prog)
root.config(menu=MENU_BAR)


#start game here.
def start_game():
    """Start off the whole show here."""
    load_high_score()
    disply_blanks()
    set_hold_btns()
    Pok.no_card_holding = True
    draw_btn.configure(state=DISABLED)
    disable_hold_btns()
    update_bank()
    # The program now loops, waiting for deal btn to be clicked,
    # and\or stake btn to be changed.

# Init hand variables.
hand = [Pok.card_one, Pok.card_two, Pok.card_three, Pok.card_four, Pok.card_five]
hand_value = check_hand(hand)
high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                       text='High Score: $'+str(Pok.high_score))
high_score_lbl.grid(row=4, column=0)

start_game()


root.mainloop()

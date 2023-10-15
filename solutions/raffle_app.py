# Raffle Game implementation/simulation
import random


class RaffleGame:
    def __init__(self):
        self.pot = 100
        self.status = 'Darw has not started'
        self.ticket_purchases = {}
        self.draw_initialize = False

    def show_welcome_screen(self):
        print('Welcome to My Raffle APP')
        if not self.draw_initialize:
            print('Status: Draw has not started')
        else:
            print(f'Status: Draw is ongoing. Raffle pot size is ${round(self.pot, 2)}')

        print('[1] Start a New Draw')
        print('[2] Buy Tickets')
        print('[3] Run Raffle')

    def buy_tickets(self, name, num_tickets):
        tickets = []
        # generate tickets
        for _ in range(num_tickets):
            ticket = random.sample(range(1, 15), 5)
            tickets.append(ticket)
        # check existing tickets
        purchased_tickets = self.ticket_purchases.get(name, [])
        if not purchased_tickets:
            self.ticket_purchases[name] = tickets
        else:
            _ = [purchased_tickets.append(ticket) for ticket in tickets]
            self.ticket_purchases[name] = purchased_tickets
        self.pot += num_tickets * 5

        return tickets

    def run_raffle(self):
        if not self.ticket_purchases:
            print("You must purchase ticket(s) to run the Raffle.")
            return

        self.draw_initialize = False
        user_ticket_map = self.ticket_purchases
        # generate winning ticket
        winning_ticket = random.sample(range(1, 15), 5)
        winning_ticket_str = [str(num) for num in winning_ticket]
        print('Running Raffle..')
        msg = ' '.join(winning_ticket_str)
        print(f'Winning Ticket is {msg}')
        print()

        winners = self.find_winners(user_ticket_map, winning_ticket)
        self.display_winners(winners)

    def display_winners(self, winners):
        group_list = ['2', '3', '4', '5']
        reward_percentage_map = {
            '2': 10,
            '3': 15,
            '4': 25,
            '5': 50,
        }
        total_reward = 0
        for group in group_list:
            if group == '5':
                print(f'Group {group} Winners (Jackpot):')
            else:
                print(f'Group {group} Winners:')

            group_winners = winners[group]
            if not group_winners:
                print('Nil')
                continue
            total_winners = sum(group_winners.values())
            total_group_reward = game.pot * reward_percentage_map[group] / 100
            total_reward += total_group_reward
            for winer_name, win_count in group_winners.items():
                winner_reward = total_group_reward / total_winners * win_count
                print(f'{winer_name} with {win_count} winning ticket(s) - ${round(winner_reward, 2)}')
            print()
        self.pot = self.pot - total_reward

    def find_winners(self, user_ticket_map, winning_ticket):
        winners = {'2': {}, '3': {}, '4': {}, '5': {}}

        for user, tickets in user_ticket_map.items():
            for ticket in tickets:
                ticket_matches = len(set(winning_ticket) & set(ticket))
                if ticket_matches == 2:
                    winners['2'][user] = winners['2'].setdefault(user, 0) + 1
                elif ticket_matches == 3:
                    winners['3'][user] = winners['3'].setdefault(user, 0) + 1
                elif ticket_matches == 4:
                    winners['4'][user] = winners['4'].setdefault(user, 0) + 1
                elif ticket_matches == 5:
                    winners['5'][user] = winners['5'].setdefault(user, 0) + 1
        return winners


if __name__ == '__main__':
    game = RaffleGame()
    game.show_welcome_screen()
    while True:
        choice = input()
        if choice == '1':
            if game.draw_initialize:
                print('Run the Raffle before any new Draw.')
                continue

            print(f'New Raffle draw has been started. Initial pot size: ${round(game.pot, 2)}')
            print('Press any key to return to main menu')
            game.draw_initialize = True
            game.ticket_purchases = {}

        elif choice == '2':
            if not game.draw_initialize:
                print('First, you have to start a new Draw.')
                print('Press any key to return to main menu')
                continue
            while True:
                try:
                    print('Enter your name, no of tickets to purchase')
                    name, num_of_tickets = input().split(',')
                    name = name.strip()
                    num_of_tickets = int(num_of_tickets.strip())
                    break
                except:
                    print('Invalid input. eg: James, 1')
                    continue

            # check user tickets limit
            purchased_tickets = game.ticket_purchases.get(name, [])
            if len(purchased_tickets) + num_of_tickets > 5:
                print("You cann't buy more than 5 tickets.")
                print('Press any key to return to main menu')
                continue
            if num_of_tickets < 1 or num_of_tickets > 5:
                print("You can purchase a minimum of 1 and a maximum of 5 tickets.")
                print('Press any key to return to main menu')
                continue

            print(f'Hi {name}, you have purchased {num_of_tickets} ticket(s)-')
            tickets = game.buy_tickets(name, num_of_tickets)

            for ticket_number, ticket in enumerate(tickets, start=1):
                ticket_str = [str(number) for number in ticket]
                message = f'Ticket {ticket_number}: ' + ' '.join(ticket_str)
                print(message)
                print()

            print('Press any key to return to main menu')
        elif choice == '3':
            if not game.draw_initialize:
                print('First, you have to start a new Draw.')
                print('Press any key to return to main menu')
                continue
            game.run_raffle()
            print('Press any key to return to main menu')
        else:
            game.show_welcome_screen()

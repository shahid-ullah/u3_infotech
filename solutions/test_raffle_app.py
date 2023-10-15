import pytest

from raffle_app import RaffleGame


@pytest.fixture
def raffle_game():
    game = RaffleGame()
    return game


def test_initial_pot_value(raffle_game):
    assert raffle_game.pot == 100
    assert raffle_game.draw_initialize is False


def test_buy_tickets(raffle_game):
    tickets = raffle_game.buy_tickets('James', 3)
    assert len(tickets) == 3


def test_winner_count(raffle_game):
    winning_ticket = [3, 7, 8, 11, 12]
    user_ticket_map = {
        'James': [[4, 7, 8, 13, 14]],
        'Ben': [
            [3, 6, 9, 11, 13],
            [3, 7, 8, 11, 14],
        ],
        'Romeo': [
            [3, 7, 9, 14, 15],
            [4, 5, 10, 12, 15],
            [1, 2, 7, 12, 13],
        ],
    }
    winners = raffle_game.find_winners(user_ticket_map, winning_ticket)
    assert winners['2']['James'] == 1
    assert winners['2']['Ben'] == 1
    assert winners['2']['Romeo'] == 2
    assert winners['4']['Ben'] == 1

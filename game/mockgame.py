"""
game
    turn 0
        start_game
    turn i: while player.ast_position < max_ast_position, for all players
        census:
            tax_collection
                tax_revolts?
            population_expansion
            census
        movement
            player_movement for player in players
            movement_resolution
                conflict
                city_construction
                checks
                    surplus
                    support
        trading
            trade
            calamity
            special_abilities
            checks
                surplus
                support
        civ_card_purchases
            ast_advancement
"""
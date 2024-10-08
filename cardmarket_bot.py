
class CardmarketBot:
    def __init__(
        self,
        driver_context_manager,
        ignore_signed_cards=True,
        ignore_altered_cards=True,
        ignore_bad_sellers=True,
        manual_lookup_threshold=None,
    ):
        self.driver_context_manager = driver_context_manager
        self.ignore_signed_cards = ignore_signed_cards
        self.ignore_altered_cards = ignore_altered_cards
        self.ignore_bad_sellers = ignore_bad_sellers
        self.manual_lookup_threshold = manual_lookup_threshold

    def evaluate_card(self, card):
        """Return lowest price as floating point number."""

    def evaluate_binder(self, binder):
        """Return lowest price total as floating point number."""

    def update_card_with_offers(self, card, n_offers=3):
        """Add n lowest offers to card."""

    def update_binder_with_offers(self, binder, n_offers=3):
        """Add n lowest offers to each card in binder."""

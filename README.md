
As of now, the library is still under development. While a significant part of
the functionality has already been implemented, the library is not yet ready to
be used.

-------------------------------------------------------------------------------

yugioh-vendor
=============

Welcome to **yugioh-vendor**, a Python library for effectively evaluating large
collections of Yugioh cards. The library uses `selenium` to look up card prices
on [Cardmarket](https://www.cardmarket.com/en/YuGiOh).


Intended Features
-----------------
- Enables users to read `.csv` files into `Binder` objects, which can be used
  for evaluation of large quantites of cards.
  - Seamless transitioning between `.csv`s, `Binder`s, and `pandas.DataFrame`s,
    in all directions.
- Infers, from information available from a physical copy of a card, the
  correct *Cardmarket* article.
  - Example: A DL09 Krebons with blue Rare text is automatically inferred to
    correspond to the *Cardmarket* version *Version 1*.
- Looks up prices of given cards, and allows users to export those prices to
  `.csv` files or `pandas.DataFrame`s for further analysis.

*(Written in Python 3.13.)*


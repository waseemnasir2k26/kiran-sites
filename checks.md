# Kiran Studio site checks

Every client page must pass all of these before it ships.

1. Opening hours on the page match data/<client>.json exactly.
2. Prices on the page match data/<client>.json exactly (item and PKR).
3. The only phone number shown is the placeholder +92 300 0000000.
4. No email addresses anywhere on the page.
5. The page has a viewport meta tag.
6. The price section of each page shows "Prices checked: <updated date from data>" (in the page body, not the shared footer).

Run: python scripts/check-site.py <client>

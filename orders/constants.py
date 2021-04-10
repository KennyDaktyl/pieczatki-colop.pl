ORDER_STATUS = (
    (1, "Otwarte"),
    (2, "W przygotowaniu"),
    (3, "W dostawie"),
    (4, "Zrealizowane"),
    (5, "Anulowane"),
)
ORDER_STATUS = sorted(ORDER_STATUS)

DELIVERY_TYPE = (
    (1, "Odbiór osobisty"),
    (2, "Dostawa"),
)
DELIVERY_TYPE = sorted(DELIVERY_TYPE)

PAY_METHOD = (
    (1, "gotówka"),
    (2, "karta"),
    (3, "przelew"),
)
PAY_METHOD = sorted(PAY_METHOD)

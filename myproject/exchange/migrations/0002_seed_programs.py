from django.db import migrations

# Rows from the dean's office table, copied as is. Only the deadlines are
# written in ISO format because the column is a DATE.
SEED_SQL = """
INSERT INTO exchange_exchangeprogram (university, languages, seats, deadline, description) VALUES
(
    'Uniwersytet Warszawski, Польща',
    'польська, англійська',
    '5',
    '2026-11-15',
    'Найбільший університет Польщі з потужними гуманітарними факультетами в самому центрі Варшави. Студенти обміну можуть обирати курси з історії, філології та культурології польською або англійською мовами.'
),
(
    'KU Leuven (Бельгія)',
    'English',
    '2 місця',
    '2026-12-01',
    'Один із найстаріших і найрейтинговіших університетів Європи, заснований 1425 року. Факультет мистецтв пропонує англомовні курси з філософії, історії та лінгвістики.'
),
(
    'Vilnius University, Литва',
    'англійська',
    'до 4',
    '2026-10-20',
    'Найстаріший університет країн Балтії, що поєднує історичний кампус у старому місті з сучасними програмами. Англомовні курси охоплюють історію Центрально-Східної Європи, балтистику та медієзнавство.'
),
(
    'Uniwersytet Jagielloński, Польща',
    'Польська, Англійська',
    '3',
    '2026-11-15',
    'Найстаріший університет Польщі, заснований 1364 року в Кракові. Гуманітарні факультети мають сильні школи славістики, історії мистецтва та культурології.'
),
(
    'University of Tartu - Естонія',
    'англійська, естонська',
    '2',
    '2027-01-10',
    'Провідний університет Естонії з понад трьохсотлітньою історією та міжнародним академічним середовищем. Студенти можуть обрати курси із семіотики, культурних студій та історії регіону.'
),
(
    'Masaryk University, Чехія',
    'англійська',
    '1 місце',
    '2026-09-30',
    'Другий за величиною університет Чехії, розташований у Брно. Філософський факультет пропонує широкий вибір англомовних курсів з історії, філології та мистецтвознавства.'
);
"""

# Matches by name prefix instead of the exact value: rolling back 0004 merges
# university and country back with ", ", so e.g. "KU Leuven (Бельгія)" returns
# as "KU Leuven, Бельгія" and an exact match would leave the rows behind.
UNSEED_SQL = """
DELETE FROM exchange_exchangeprogram
WHERE university LIKE 'Uniwersytet Warszawski%'
   OR university LIKE 'KU Leuven%'
   OR university LIKE 'Vilnius University%'
   OR university LIKE 'Uniwersytet Jagielloński%'
   OR university LIKE 'University of Tartu%'
   OR university LIKE 'Masaryk University%';
"""


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(SEED_SQL, reverse_sql=UNSEED_SQL),
    ]

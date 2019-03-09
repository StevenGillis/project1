select
    b.author,
    b.average_score,
    b."id",
    b.isbn,
    b.review_count,
    b.title,
    b."year"
from
    "Book" b;

select
    r.book_id,
    r."id",
    r.review_score,
    r.visitor_id
from
    review r;

select
    b.author,
    b.average_score,
    b."id",
    b.isbn,
    b.review_count,
    b.title,
    b."year"
from
    book b;

SELECT * FROM review where book_id = 3665 AND visitor_id = 9;

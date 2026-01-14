CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    tax_id VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    book_id UUID NOT NULL,
    booking_date TIMESTAMP NOT NULL DEFAULT NOW(),
    return_date TIMESTAMP,

    CONSTRAINT fk_booking_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_booking_book
        FOREIGN KEY (book_id)
        REFERENCES books(id)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_bookings_user_id ON bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_bookings_book_id ON bookings(book_id);

INSERT INTO users (name, email, tax_id) VALUES
('Mario Rossi', 'mario.rossi@example.com', 'RSSMRA80A01H501U'),
('Luigi Bianchi', 'luigi.bianchi@example.com', 'BNCLGU85B12F205Z'),
('Anna Verdi', 'anna.verdi@example.com', 'VRDNNA90C45L219X');

INSERT INTO books (title, author, genre) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Romance'),
('1984', 'George Orwell', 'Sci-Fi'),
('To Kill a Mockingbird', 'Harper Lee', 'Thriller');

INSERT INTO bookings (user_id, book_id)
VALUES (
    (SELECT id FROM users WHERE email = 'mario.rossi@example.com'),
    (SELECT id FROM books WHERE title = '1984')
);

INSERT INTO bookings (user_id, book_id)
VALUES (
    (SELECT id FROM users WHERE email = 'anna.verdi@example.com'),
    (SELECT id FROM books WHERE title = 'To Kill a Mockingbird')
);
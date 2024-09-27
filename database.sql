CREATE TABLE libraryrecords (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    book_name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE
);

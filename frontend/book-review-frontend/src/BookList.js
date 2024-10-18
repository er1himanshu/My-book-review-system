import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'; // Import Link
import './BookList.css'; // Import your CSS file for styles

const BookList = () => {
    const [books, setBooks] = useState([]);

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/books/');
                setBooks(response.data.results); // Adjust if your API returns a different structure
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        };

        fetchBooks();
    }, []);

    return (
        <div>
            <h2>Book List</h2>
            <ul className="book-list"> {/* Add a CSS class for styling */}
                {books.map(book => (
                    <li key={book.id} className="book-item"> {/* Add a CSS class for individual book items */}
                        <Link to={`/books/${book.id}`} className="book-link"> {/* Wrap the title in a Link */}
                            <strong>{book.title}</strong>
                        </Link>
                        <p className="book-info"> {/* Additional book information */}
                            by {book.author} | ISBN: {book.isbn} | Genre: {book.genre} | Published: {book.published_date}
                        </p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default BookList;

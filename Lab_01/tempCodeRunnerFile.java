// Lớp User
class User {
    private int id;
    private String name;
    private String email;

    public User(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }
}

// Lớp Book
class Book {
    private int id;
    private String title;
    private String author;
    private String publisher;

    public Book(int id, String title, String author, String publisher) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.publisher = publisher;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getPublisher() {
        return publisher;
    }
}

// Lớp Library
class Library {
    private ArrayList<Book> books;

    public Library() {
        books = new ArrayList<>();
    }

    public void addBook(Book book) {
        books.add(book);
    }

    public ArrayList<Book> searchBook(String keyword) {
        ArrayList<Book> result = new ArrayList<>();

        for (Book book : books) {
            if (book.getTitle().contains(keyword) ||
                book.getAuthor().contains(keyword) ||
                book.getPublisher().contains(keyword)) {
                result.add(book);
            }
        }

        return result;
    }

    public boolean borrowBook(int bookId) {
        for (Book book : books) {
            if (book.getId() == bookId) {
                books.remove(book);
                return true;
            }
        }

        return false;
    }
}

// Lớp Borrow
class Borrow {
    private ArrayList<Book> borrowedBooks;

    public Borrow() {
        borrowedBooks = new ArrayList<>();
    }

    public boolean borrowBook(Book book) {
        borrowedBooks.add(book);
        return true;
    }

    public boolean returnBook(Book book) {
        if (borrowedBooks.contains(book)) {
            borrowedBooks.remove(book);
            return true;
        }

        return false;
    }

    public ArrayList<Book> getBorrowedBooks() {
        return borrowedBooks;
    }
}

// Lớp Account
class Account {
    private String username;
    private String password;

    public Account(String username, String password) {
        this.username = username;
        this.password = password;
    }
}

class LibraryFacade {
    private Library library;
    private Borrow borrow;
    private Account account;
    public LibraryFacade() {
        library = new Library();
        borrow = new Borrow();
        account = new Account("", "");
    }

    public boolean register(String username, String password) {
        account = new Account(username, password);
        return true;
    }

    public boolean login(String username, String password) {
        if (account.username.equals(username) && account.password.equals(password)) {
            return true;
        }

        return false;
    }

    public ArrayList<Book> searchBook(String keyword) {
        return library.searchBook(keyword);
    }

    public boolean borrowBook(int bookId) {
        Book book = null;

        for (Book b : library.searchBook("")) {
            if (b.getId() == bookId) {
                book = b;
                break;
            }
        }

        if (book == null) {
            return false;
        }

        boolean result = borrow.borrowBook(book);

        if (result) {
            library.borrowBook(bookId);
        }

        return result;
    }

    public boolean returnBook(int bookId) {
        Book book = null;

        for (Book b : borrow.getBorrowedBooks()) {
            if (b.getId() == bookId) {
                book = b;
                break;
            }
        }

        if (book == null) {
            return false;
        }

        boolean result = borrow.returnBook(book);

        if (result) {
            library.addBook(book);
        }

        return result;
    }
}

public class Main 
{
    public static void main(String[] args) {
    LibraryFacade facade = new LibraryFacade();
        facade.register("username", "password");

        if (facade.login("username", "password")) {
            System.out.println("Login successful");
        } else {
            System.out.println("Login failed");
        }

        facade.searchBook("Harry Potter");

        facade.borrowBook(1);

        facade.returnBook(1);
    }
}

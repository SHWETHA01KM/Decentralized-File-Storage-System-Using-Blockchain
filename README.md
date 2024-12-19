Decentralized File Storage System

The Decentralized File Storage System is a secure and efficient platform that allows users to upload, store, and manage their files on a decentralized network using IPFS (InterPlanetary File System). The system also incorporates user authentication and file metadata storage using MongoDB for a seamless user experience.

Features

User Authentication: Secure signup and login functionality using email and password.
Decentralized Storage: File storage and retrieval using Pinata, an IPFS-based service.
File Management: Upload, view, and delete files with their associated metadata.
Responsive Frontend: Simple and user-friendly interface for file uploads and management.
Database Integration: Metadata and user information stored in MongoDB for efficient backend operations.
Technologies Used Backend

Python (Flask)
MongoDB
Pinata API (IPFS)
bcrypt for password hashing
Frontend

HTML5, CSS3, and JavaScript
Responsive design for cross-platform compatibility
Database

MongoDB for storing user credentials and file metadata.
Endpoints Backend API

/signup: User registration.
/login: User login.
/upload: Upload files to IPFS via Pinata.
/files: Fetch user-specific files.
/delete/<ipfs_hash>: Delete a file from IPFS and metadata from MongoDB.
Testing

Unit Testing: Verified individual components, such as user authentication and file upload functionality.
Integration Testing: Tested interaction between backend, database, and IPFS.
Functional Testing: Validated complete workflows, such as file upload, retrieval, and deletion.
Future Enhancements

Add advanced file sharing features with access control.
Introduce user roles and permissions.
Enhance the system with file search and categorization.
Provide file preview capabilities directly from the IPFS hash.
Acknowledgments

MongoDB: For providing a robust NoSQL database.
Pinata: For facilitating file storage on IPFS.
Flask: For building the backend services.
HTML, CSS, and JavaScript: For powering the frontend user interface.

    /* Custom styles for the form */
    .card {
        background-color: #ffffff;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
    }

    textarea {
        resize: vertical;
        font-size: 1rem;
        border: 2px solid #e0e0e0;
        padding: 12px;
        transition: border-color 0.3s;
    }

    textarea:focus {
        border-color: #3b82f6; /* Blue on focus */
        outline: none;
    }

    button {
        background-color: #3b82f6;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s;
    }

    button:hover {
    background-color: #2563eb;
    }

    button:focus {
        outline: none;
    }

    a.button.secondaryAction {
        background-color: #f3f4f6;
        color: #374151;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        transition: background-color 0.3s;
    }

    a.button.secondaryAction:hover {
        background-color: #d1d5db;
    }

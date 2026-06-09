from myapp import create_app

app = create_app()

# Python file that runned is named with "__main__"

if __name__ == "__main__":
    app.run(debug=True)
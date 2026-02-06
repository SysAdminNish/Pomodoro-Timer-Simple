Pomodoro Timer Simple

A minimalistic, professional Pomodoro Timer application built with Python and Tkinter, following the Model-View-Presenter (MVP) architectural pattern. Designed for productivity enthusiasts, this app features a clean white/light grey theme, selectable timer durations, motivational Pomodoro quotes, and a visually engaging spinning progress ring.

---

## Features

- **Minimalistic UI:** Clean, modern interface with white and light grey palette for distraction-free focus.
- **MVP Architecture:** Robust separation of concerns for maintainability and scalability.
- **Selectable Durations:** Choose Pomodoro and break durations (default: 25 min focus, 5 min break).
- **Spinning Progress Ring:** Animated circular timer visualization, starting at the top and spinning anticlockwise.
- **Motivational Quotes:** Displays a random Pomodoro one-liner quote from a curated set of 50, each time the app is launched.
- **Cross-Platform:** Works on Windows and macOS. Includes Windows chime notification support.


---

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually included with Python)

### Installation
1. Clone the repository:
	```bash
	git clone https://github.com/SysAdminNish/Pomodoro-Timer-Simple.git
	cd Pomodoro-Timer-Simple
	```
2. (Optional) Create a virtual environment:
	```bash
	python3 -m venv venv
	source venv/bin/activate  # macOS/Linux
	venv\Scripts\activate    # Windows
	```
3. Install dependencies (if any):
	```bash
	pip install -r requirements.txt
	```
	*(No external dependencies required for basic functionality)*

### Running the Application
```bash
python main.py
```

---

## Project Structure

```
Pomodoro-Timer-Simple/
├── main.py              # Entry point, window setup
├── model.py             # Timer state and logic
├── view.py              # UI rendering, quote display, arc drawing
├── presenter.py         # Timer logic, animation, notification
├── pomodoro_quotes.json # 50 Pomodoro motivational quotes
├── README.md            # Project documentation
```

---

## Architecture

- **Model:** Encapsulates timer state and duration logic.
- **View:** Handles UI rendering, progress ring, and quote display.
- **Presenter:** Mediates timer logic, animation, and user interactions.

---

## Customization

- **Quotes:** Add or modify quotes in `pomodoro_quotes.json`.
- **Theme:** Adjust colors in `view.py` for personal preference.
- **Durations:** Change default durations in `model.py` or via UI.

---

## Credits

- Developed by [SysAdminNish](https://github.com/SysAdminNish)
- Pomodoro quotes curated from productivity communities and open sources.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Feedback & Contributions

Feedback, issues, and pull requests are welcome! Please open an issue or submit a PR on GitHub.

---

## Acknowledgements

- Pomodoro Technique by Francesco Cirillo
- Tkinter documentation and Python community
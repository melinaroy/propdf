![WIP](https://img.shields.io/badge/status-WIP-yellow)

# ProPDF

📎 A simple tool to manipulate PDF files: merge, reorder, delete or insert pages.
I originally built this in 2020 to help teachers. It was my first real Python project, based on an actual need.

## 📖 Context

During the pandemic, I wanted to learn Python so I looked for a real project to work on. I asked my parents if there was anything they found annoying or hard to do on a computer. My mom, a teacher, told me she had no way to edit PDF files easily. Most teachers in her school board didn’t have any tool for that.

So I decided to build one.

### 📝 What my mom needed

Here’s what she asked for:

- ➕ Add blank pages to an existing PDF
- 🔗 Merge two PDF files
- 📂 Merge multiple PDF files (in folder order)
- ❌ Delete selected pages
- 📤 Extract specific pages into a new file

### 💡 What I added

While working on it, I ended up adding a few features on my own:

- 🧮 Let users chain multiple actions in one session
- ✅ Input validation so things don’t crash
- 🧭 A simple UI that made sense for someone with little tech background
- 🔐 A basic “license” system using a hidden file in `AppData`

### 📦 Packaging and distribution (DIY style)

This project was also a great way to learn how to package an app and distribute it. I wanted something really simple and assumed my users weren’t tech-savvy.

So I made a system where:

- A "license" was just a hidden text file saved in AppData
- The app would only launch if the file was present
- My mom carried everything on a USB stick
- She’d run a "license installer" to create the file, then copy the `.exe` manually

Not secure. Not clean. But it worked, and it taught me a lot.

## 🔍 Why this repo exists

I’m coming back to this project for two reasons:

1. To document the very first app I ever built
2. To see how much I’ve improved by refactoring and reworking it

## 📊 Progress Metrics

| Metric                          | Original Version                | Refactored Version |
| ------------------------------- | ------------------------------- | ------------------ |
| Number of Python files          | 2                               | TBD                |
| Number of functions             | 5                               |                    |
| Average lines per function      | 4.2                             |                    |
| Docstrings and comments present | 147 comments, 0 docstrings      |                    |
| Unit tests present              | ❌                              |                    |
| Test coverage                   | 0%                              |                    |
| Modular structure               | 2 files + icon, tightly coupled |                    |

## 📁 Project structure

```
propdf/
├── legacy/ ← Original 2020 version
├── src/ ← Refactored version
├── README.md ← This file
├── .gitignore
└── LICENSE ← To be added
```

## 🚀 What’s next

- [ ] Archive and clean up the original code
- [ ] Break down features into separate modules
- [ ] Add unit tests
- [ ] Improve the UI
- [ ] (Maybe) make a simple cross-platform installer

## 👩‍💻 Why it still matters

This little app was the first time I saw how code could solve a real problem for someone I know. It got me hooked.

Now I’m taking the time to revisit it and see how far I’ve come — in how I think, how I code, and how I build things for real people.

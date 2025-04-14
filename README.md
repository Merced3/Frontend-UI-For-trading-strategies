# Frontend UI

So I've been making trading strategies for about 2 years now and ive been wanting a UI that gives them justice. at the beginning the strategies were simple and mainly for the purpose of dipping my toes into the industry but for the singular strategy that i have on private on github, I don't have any UI for it too show how good it really is.

Hence this UI, this is more of a template for when I want too implement this UI to that strategy.

## Basic UI setup

 ___________________________________________________
|            |                                      |
|   Config   |                                      |
|  Settings  |            Actual Chart              |
|            |    *Showings How strategy works*     |
|            |                                      |
|            |                                      |
|____________|______________________________________|
|                                                   |
|                       Logs                        |
|___________________________________________________|

## Live Monitoring Tab

┌────────────────────────────────┬────────────────────────────────┐
│        Live Monitoring         │   Stock candles stick chart    │
│                                │                                │
│      ┌────────────────────┐    │                                │
│      │Threads             │    │                                │
│      ├────────────────────┤    │                                │
│      │Other columns needed│    │                                │
│      ├────────────────────┤    │                                │
│      │Data (scroll ^/⌄)   │    │                                │
│      └────────────────────┘    │                                │
│                                │                                │
│       ┌────────────────────┐   │                                │
│       │Subprocesses        │   │                                │
│       ├────────────────────┤   │                                │
│       │Other columns needed│   │                                │
│       ├────────────────────┤   │                                │
│       │Data (scroll ^/⌄)   │   │                                │
│       └────────────────────┘   │                                │
│                                │                                │
└────────────────────────────────┴────────────────────────────────┘
│                                Logs                             │
│                                                                 │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

## Running This Project

1) Make virtual envirement in folder/project terminal:

Too `Invoke` a venv folder:

```bash
python -m venv C:\path\to\new\virtual\environment
```

1) Activate virtual enviroment in terminal:

```bash
venv\Scripts\activate
```

1) Download the `requirements.txt` file into `venv`

```bash
pip install -r requirements.txt
```

1) Now run project:

```bash
python app.py
```

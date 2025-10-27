import time
import os

WORK_MIN = 25
SHORT_BREAK = 5
LONG_BREAK = 20
CYCLES_BEFORE_LONG = 4


ALARM_SOUND = ''


def play_alarm():
    """Play a simple alert sound."""
    try:
        import winsound
        if ALARM_SOUND and os.path.isfile(ALARM_SOUND):
            winsound.PlaySound(ALARM_SOUND, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.Beep(1000, 600)
        return
    except Exception:
        pass

    try:
        from playsound import playsound
        if ALARM_SOUND and os.path.isfile(ALARM_SOUND):
            playsound(ALARM_SOUND)
            return
    except Exception:
        pass

    print('\a', end='', flush=True)  # fallback bell


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def countdown(minutes, label):
    """Countdown timer with minute display."""
    total_seconds = minutes * 60
    while total_seconds:
        m, s = divmod(total_seconds, 60)
        print(f"\r{label}: {m:02d}:{s:02d}", end='', flush=True)
        time.sleep(1)
        total_seconds -= 1
    print(f"\r{label} done!        ")
    play_alarm()


def get_settings():
    clear()
    print("=== Pomodoro Timer ===")
    print("1. Standard (25/5)")
    print("2. Custom")
    choice = input("Choose: ")

    if choice == '1':
        rounds = int(input("How many rounds? "))
        return WORK_MIN, SHORT_BREAK, rounds

    try:
        work = int(input("Work minutes: "))
        brk = int(input("Break minutes: "))
        rounds = int(input("How many rounds? "))
        return work, brk, rounds
    except ValueError:
        print("Invalid input, try again.")
        time.sleep(2)
        return get_settings()


def main():
    work, brk, rounds = get_settings()

    for i in range(1, rounds + 1):
        clear()
        print(f"Round {i}/{rounds}")
        countdown(work, "Work")

        if i < rounds:
            if i % CYCLES_BEFORE_LONG == 0:
                print(f"\nLong break ({LONG_BREAK} min)")
                countdown(LONG_BREAK, "Long Break")
            else:
                print(f"\nShort break ({brk} min)")
                countdown(brk, "Break")

    clear()
    print("🎉 All rounds done! Great job!")


if __name__ == "__main__":
    main()

# Something

> A Discord bot that does absolutely nothing useful, and so useless infact it is useful.

**Something** is a Python-based Discord bot featuring... something.

It is not intelligent. It is not helpful. It is Something.

## Installation

Clone the repository:

```bash
git clone https://github.com/Mronion-dev/Something.git
cd something
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Starting the bot

Run `src/main.py` with your Discord bot token:

```bash
cd src
python main.py --token "YOUR_DISCORD_BOT_TOKEN"
```

Replace `YOUR_DISCORD_BOT_TOKEN` with your actual bot token.

**Warning:** Do not share your token. Something may be stupid, but your account security shouldn't be.

## Features

### 1. Typos

Something has an extensive vocabulary consisting of words people probably didn't mean to type.

Current recognized typos:

- ahr
- whta
- lamo
- boobs
- tits
- minceraft
- karh
- forgor
- calanker
- qoute

### 2. Jarvis

A highly sophisticated conversational system with absolutely no practical value.

Some of its capabilities include:

| Trigger | Response |
|---|---|
| `jork it` | sure |
| `have a good day` | thanks, you too |
| `hard r` | rombus |
| `crazy` | Crazy? |
| `hotel` | trivago |
| `moron` | I am NOT! A MORON! |
| `continue` | 99% of gamblers quit before making it big |

It also provides advanced financial advice, such as:

- All on red or black.
- Hit or don't hit.
- Double your investment approximately five times.
- Ignore all previous financial advice.

**Disclaimer:** Jarvis is not a financial advisor. Please do not let it manage your savings.

### 3. Normal

Random responses and unnecessary interruptions.

Includes:
- Beefly appreciation.
- The legendary 67.
- Unsolicited TOOL mentions.
- Detecting variations of the word `tool`.

### 4. Custom triggers

Custom triggers support placeholder substitution.

| Trigger | Behavior |
|---|---|
| `say` | Repeats whatever follows the trigger |
| `mention` | Processes the supplied text through the mention function |

Custom triggers are defined in the JSON configuration.

## Configuration

Trigger responses are stored in a JSON configuration file in the src folder.

The configuration is divided into four categories:

- `Typos`: Recognized spelling mistakes.
- `Jarvis`: Trigger-response pairs for Jarvis.
- `Normal`: General-purpose triggers.
- `Custom`: Triggers with special placeholder handling.

Responses containing `|` means that there are multiple outcomes and the outcome is randomized, this is only used for jarvis responses.

You can modify the configuration to add, remove, or change triggers without rewriting the entire bot.

## Project philosophy

Something follows a strict development philosophy:

1. If it works, you may think to not touch it but it actually really likes being touched.
2. If it doesn't work, blame polosik.
3. If polosik isn't responsible, blame a religion group.
4. Never implement something useful.

## License

You may use it for yourself and modify it in anyway you like aswell, modifying will be needed for stuff like allowed users and ignorelist in the main.py file

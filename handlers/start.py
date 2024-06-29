# handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = """
🫵 Join AIFact Frenzy Campaign now to start earning points and receive airdrops!💰💰💰
➡️️ Image Generator:
- 🎨 Prompt to create
- 🖼 3 trials for a day
- 🏆 Post on the leaderboard
➡️️ Daily Sign-in: 
- 💡 + 10 points each day
➡️️ Votes:
- 😍 Vote on the leaderboard
- 💡 + 30 points.
➡️️ Leaderboard: 
- ✨ Showcase artworks
- 🥇 Extra points for top users
➡️️ Invite Friends: 
- 🤝 Share your referral link
- 💡 Earn additional 10% of your referees' daily points.
➡️️ X Engagement:
- 👍 Follow @AIFactOfficial
- ❤️ Like/Repost/Comment daily posts
- 💡 Earn more points
💎💎💎 Join AIFact Chat (http://t.me/AIFact_chat), share your artworks, and help your favorite works move up the ranks on the leaderboard to receive more points!
    """

    keyboard = [
        [
            InlineKeyboardButton("Generate Image", callback_data='generate_image'),
            InlineKeyboardButton("Daily Sign-in", callback_data='daily_signin')
        ],
        [
            InlineKeyboardButton("Leaderboard", callback_data='leaderboard'),
            InlineKeyboardButton("Invite Friends", callback_data='invite_friends')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

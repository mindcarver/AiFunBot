from services.mysql.mysql import db_conn
from telegram import Update
from telegram.ext import CallbackContext


def daily_signin(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    try:
        with db_conn.cursor() as cursor:
            # 检查用户是否已签到
            cursor.execute(
                "SELECT `draw_count` FROM `user_stats` WHERE `user_id`=%s", (user_id,)
            )
            row = cursor.fetchone()

            if not row:
                # 如果用户不存在，插入新记录
                cursor.execute(
                    "INSERT INTO `user_stats` (`user_id`, `draw_count`) VALUES (%s, 1)",
                    (user_id,),
                )
            else:
                # 如果用户已存在且今天未签到，则增加画图次数
                current_count = row["draw_count"]
                cursor.execute(
                    "UPDATE `user_stats` SET `draw_count`=%s WHERE `user_id`=%s",
                    (current_count + 10, user_id),
                )

            # 提交更改
            db_conn.commit()

            # 向用户发送确认消息
            query.answer(
                text="Signed in successfully! Your drawing count has been increased."
            )

    except Exception as e:
        print(f"An error occurred: {e}")
        query.answer(text="An error occurred during sign-in. Please try again later.")

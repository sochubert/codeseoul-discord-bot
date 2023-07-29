import discord
import logging

from google.cloud import translate_v2 as translate


class CodeSeoulBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.logging = logging.getLogger(
            name="discord.codeseoul"
        )  # Fix the attribute name here
        self.logging.setLevel(logging.DEBUG)
        self.emoji_to_language = {
            "english": "en",
            "korean": "ko",
        }
        self.translate_client = translate.Client()

    async def on_ready(self):
        self.logging.info(f"We have logged in.")

    async def on_message(self, message):
        if message.content.startswith("$hello"):
            await message.channel.send("시발 김남영 닥치라!")

    async def retrieve_message(self, channel_id: int, message_id: int):
        channel = self.get_channel(channel_id)
        message = channel.get_partial_message(message_id)
        return await message.fetch()

    async def send_translation(self, message: discord.Message, translated_content: str):
        await message.reply(translated_content)

    async def translate(self, message_content: str, target_language: str):
        translation_response = self.translate_client.translate(
            message_content, target_language=target_language
        )
        self.logger.debug("translation response contents: %s", translation_response)
        return translation_response["translatedText"]

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        self.logger.debug("caught raw reaction: %s", payload)

        # Only handle emojis that are meant to trigger translation
        if payload.emoji.name in self.emoji_to_language:
            message = await self.retrieve_message(
                payload.channel_id, payload.message_id
            )
            translated_message = await self.translate(
                message.content, self.emoji_to_language[payload.emoji.name]
            )
            await self.send_translation(message, translated_message)

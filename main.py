import json
from aiogram import Bot, Dispatcher, executor, types
from src.settings import setting_module, setup_logger

from commands.post.modules.paginator import Paginator
from commands.post.modules.configs import Configs

setup_logger()
bot = Bot(token=setting_module.token)
dp = Dispatcher(bot)


FILE_CONFIG_DIR = 'commands/post/configs.json'
with open(FILE_CONFIG_DIR, 'r') as f:
    CONFIG_DATA = json.loads(f.read())


@dp.message_handler(commands=['spot', 'post'])
async def post_generator(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    content = message.text[6:]

    configs = Configs(CONFIG_DATA)
    if not configs.get_by_code(message.from_user.id):
        configs.get_by_code(message.chat.id, code_type='guilds')

    kwargs = configs.build_kwargs('text', 'spot')

    # compute name tag
    if configs.name_tag is None:
        name_tag = f'@{message.from_user.username}'
    elif configs.name_tag is False:
        name_tag = configs.name_tag
    else:
        name_tag = f'@{configs.name_tag}'

    colors = configs.get_colors_setup('text', 'spot')

    paginator = Paginator(configs.logo, configs.resolution, colors=colors, name_tag=name_tag)
    paginator.paginate_text(content, **kwargs)

    img = paginator.get_image()
    if message.from_user.id == message.chat.id:
        await message.answer_document(img)
    else:
        await message.answer_photo(img)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

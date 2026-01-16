from aiogram import Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from messages import WELCOME_MSG, MENU_MSG, HELP_MSG, get_main_menu, get_back_menu

logger = logging.getLogger(__name__)

# Импорты команд
from plugins.data_validator import (
    data_validator_command,
    process_format_choice as process_data_format_choice,
    process_data_validation,
    process_repeat_choice as process_data_repeat_choice,
    DataValidatorStates
)

from plugins.file_generator import (
    generate_file_command,
    process_format_choice as process_file_format_choice,
    process_file_params,
    handle_choice,
    FileGeneratorStates
)

from plugins.pairwise_tester import (
    pairwise_command as pairwise_test_command,
    process_pairwise_parameters,
    PairwiseStates
)

from plugins.docs_creator import (
    docs_command,
    process_docs_type,
    DocsStates,
    # Тест-кейс
    tc_process_title,
    tc_process_description,
    tc_process_preconditions,
    tc_process_steps,
    tc_process_expected_result,
    tc_process_priority,
    tc_handle_choice,
    # Баг-репорт
    bug_process_title,
    bug_process_description,
    bug_process_steps,
    bug_process_actual_result,
    bug_process_expected_result,
    bug_process_environment,
    bug_process_severity,
    bug_process_logs,
    bug_process_curl,
    bug_process_docs,
    bug_handle_choice,
    # Чек-лист
    cl_process_title,
    cl_process_items,
    cl_handle_choice,
)

from plugins.test_data_generator import (
    generate_test_data_command,
    process_feature_choice,
    process_format_choice as process_test_data_format_choice,
    process_count,
    process_regenerate_choice as process_test_data_regenerate_choice,
    process_payment_system,
    process_card_regenerate_choice,
    TestDataGeneratorStates
)

from plugins.sql_generator import (
    sql_generator_command,
    process_sql_type,
    process_table_name,
    process_columns,
    process_where,
    process_limit,
    process_sql_choice,
    SqlGeneratorStates,
)

from plugins.timestamp_converter import (
    timestamp_converter_command,
    process_timestamp_input,
    process_convert_choice,
    TimestampConverterStates
)

from plugins.api_validator import (
    api_validator_command,
    process_api_validation,
    process_validate_choice,
    ApiValidatorStates
)

class CommandRouter:
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.text_commands = {
            "🗂 создать файл": self.handle_file_command,
            "🧪 создать pairwise тест": self.handle_pairwise_command,
            "📑 проверить json xml yaml": self.handle_data_validator_command,
            "📝 создать документацию": self.handle_docs_command,
            "👥 создать тестовые данные": self.handle_test_data_command,
            "🕐 конвертировать timestamp": self.handle_timestamp_converter_command,
            "🗃 сгенерировать sql": self.handle_sql_generator_command,
            "🔍 проверить api": self.handle_api_validator_command,
            "назад в меню": self.handle_back_to_menu,
            "информация": self.handle_help_command
        }

    async def handle_data_validator_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(DataValidatorStates.waiting_for_format)
        await data_validator_command(message, state)

    async def handle_file_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(FileGeneratorStates.waiting_for_format)
        await generate_file_command(message, state)



    async def handle_pairwise_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(PairwiseStates.waiting_for_parameters)
        await pairwise_test_command(message, state)

    async def handle_docs_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(DocsStates.waiting_for_type)
        await docs_command(message, state)

    async def handle_test_data_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(TestDataGeneratorStates.waiting_for_format)
        await generate_test_data_command(message, state)

    async def handle_sql_generator_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(SqlGeneratorStates.waiting_for_type)
        await sql_generator_command(message, state)

    async def handle_timestamp_converter_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(TimestampConverterStates.waiting_for_input)
        await timestamp_converter_command(message, state)

    async def handle_api_validator_command(self, message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(ApiValidatorStates.waiting_for_url)
        await api_validator_command(message, state)

    async def handle_back_to_menu(self, message: Message, state: FSMContext):
        await state.clear()
        await message.answer(MENU_MSG, reply_markup=get_main_menu())

    async def handle_help_command(self, message: Message, state: FSMContext):
        await state.clear()
        await message.answer(HELP_MSG, reply_markup=get_main_menu())

    def register_handlers(self):
        try:
            logger.info("Регистрация обработчиков команд...")
            
            # Универсальный обработчик /cancel
            @self.dp.message(Command("cancel"))
            async def cmd_cancel(message: Message, state: FSMContext):
                await state.clear()
                await message.answer("✅ Операция отменена", reply_markup=get_main_menu())

            # Обработчики базовых команд
            @self.dp.message(Command("start"))
            async def cmd_start(message: Message, state: FSMContext):
                await state.clear()
                await message.answer(WELCOME_MSG, reply_markup=get_main_menu())

            @self.dp.message(Command("help"))
            async def cmd_help(message: Message, state: FSMContext):
                await self.handle_help_command(message, state)

            # Обработчики специализированных команд
            @self.dp.message(Command("file"))
            async def cmd_genfile(message: Message, state: FSMContext):
                await self.handle_file_command(message, state)



            @self.dp.message(Command("pairwise"))
            async def cmd_pairwise(message: Message, state: FSMContext):
                await self.handle_pairwise_command(message, state)

            @self.dp.message(Command("datavalidator"))
            async def cmd_validatedata(message: Message, state: FSMContext):
                await self.handle_data_validator_command(message, state)

            @self.dp.message(Command("docs"))
            async def cmd_docs(message: Message, state: FSMContext):
                await self.handle_docs_command(message, state)

            @self.dp.message(Command("testdata"))
            async def cmd_testdata(message: Message, state: FSMContext):
                await self.handle_test_data_command(message, state)

            @self.dp.message(Command("timestamp"))
            async def cmd_timestamp(message: Message, state: FSMContext):
                await self.handle_timestamp_converter_command(message, state)

            @self.dp.message(Command("sql"))
            async def cmd_sql(message: Message, state: FSMContext):
                await self.handle_sql_generator_command(message, state)

            @self.dp.message(Command("api"))
            async def cmd_api(message: Message, state: FSMContext):
                await self.handle_api_validator_command(message, state)

            # Обработчики состояний с проверкой /help
            @self.dp.message(StateFilter(FileGeneratorStates.waiting_for_format))
            async def handle_file_format_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_file_format_choice(message, state)
            
            @self.dp.message(StateFilter(FileGeneratorStates.waiting_for_params))
            async def handle_file_state(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_file_params(message, state)
                    
            @self.dp.message(StateFilter(FileGeneratorStates.waiting_for_choice))
            async def handle_file_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await handle_choice(message, state)
          
            @self.dp.message(StateFilter(PairwiseStates.waiting_for_parameters))
            async def handle_pairwise_state(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_pairwise_parameters(message, state)

            @self.dp.message(StateFilter(PairwiseStates.waiting_for_action))
            async def handle_pairwise_action(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                from plugins.pairwise_tester import process_pairwise_action
                await process_pairwise_action(message, state)

            @self.dp.message(StateFilter(DataValidatorStates.waiting_for_format))
            async def handle_data_format_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_data_format_choice(message, state)
          
            @self.dp.message(StateFilter(DataValidatorStates.waiting_for_data))
            async def handle_data_validation(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_data_validation(message, state)
          
            @self.dp.message(StateFilter(DataValidatorStates.waiting_for_repeat))
            async def handle_data_repeat_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_data_repeat_choice(message, state)

            # Документация (тест-кейсы, баг-репорты, чек-листы)
            @self.dp.message(StateFilter(DocsStates.waiting_for_type))
            async def handle_docs_type(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_docs_type(message, state)

            # Тест-кейс
            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_title))
            async def handle_tc_title(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_process_title(message, state)

            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_description))
            async def handle_tc_description(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_process_description(message, state)

            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_preconditions))
            async def handle_tc_preconditions(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_process_preconditions(message, state)

            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_steps))
            async def handle_tc_steps(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_process_steps(message, state)

            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_expected_result))
            async def handle_tc_expected_result(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_process_expected_result(message, state)

            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_priority))
            async def handle_tc_priority(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_process_priority(message, state)

            @self.dp.message(StateFilter(DocsStates.tc_waiting_for_choice))
            async def handle_tc_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await tc_handle_choice(message, state)

            # Баг-репорт
            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_title))
            async def handle_bug_title(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_title(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_description))
            async def handle_bug_description(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_description(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_steps))
            async def handle_bug_steps(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_steps(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_actual_result))
            async def handle_bug_actual_result(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_actual_result(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_expected_result))
            async def handle_bug_expected_result(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_expected_result(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_environment))
            async def handle_bug_environment(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_environment(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_severity))
            async def handle_bug_severity(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_severity(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_logs))
            async def handle_bug_logs(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_logs(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_curl))
            async def handle_bug_curl(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_curl(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_docs))
            async def handle_bug_docs(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_process_docs(message, state)

            @self.dp.message(StateFilter(DocsStates.bug_waiting_for_choice))
            async def handle_bug_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await bug_handle_choice(message, state)

            # Чек-лист
            @self.dp.message(StateFilter(DocsStates.cl_waiting_for_title))
            async def handle_cl_title(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await cl_process_title(message, state)

            @self.dp.message(StateFilter(DocsStates.cl_waiting_for_items))
            async def handle_cl_items(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await cl_process_items(message, state)

            @self.dp.message(StateFilter(DocsStates.cl_waiting_for_choice))
            async def handle_cl_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await cl_handle_choice(message, state)

            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_feature))
            async def handle_test_data_feature(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_feature_choice(message, state)
            
            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_payment_system))
            async def handle_payment_system_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_payment_system(message, state)
            
            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_card_regenerate_choice))
            async def handle_card_regenerate_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_card_regenerate_choice(message, state)

            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_format))
            async def handle_test_data_format(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return

                await process_test_data_format_choice(message, state)

            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_count))
            async def handle_test_data_count(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_count(message, state)

            @self.dp.message(StateFilter(TestDataGeneratorStates.waiting_for_regenerate_choice))
            async def handle_test_data_regenerate_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_test_data_regenerate_choice(message, state)

            @self.dp.message(StateFilter(TimestampConverterStates.waiting_for_input))
            async def handle_timestamp_input(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_timestamp_input(message, state)

            @self.dp.message(StateFilter(TimestampConverterStates.waiting_for_convert_choice))
            async def handle_timestamp_convert_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_convert_choice(message, state)

            @self.dp.message(StateFilter(ApiValidatorStates.waiting_for_url))
            async def handle_api_url(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_api_validation(message, state)

            @self.dp.message(StateFilter(ApiValidatorStates.waiting_for_validate_choice))
            async def handle_api_validate_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                if message.text == "Назад в меню":
                    await self.handle_back_to_menu(message, state)
                    return
                await process_validate_choice(message, state)

            # Генератор SQL
            @self.dp.message(StateFilter(SqlGeneratorStates.waiting_for_type))
            async def handle_sql_type(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_sql_type(message, state)

            @self.dp.message(StateFilter(SqlGeneratorStates.waiting_for_table_name))
            async def handle_sql_table(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_table_name(message, state)

            @self.dp.message(StateFilter(SqlGeneratorStates.waiting_for_columns))
            async def handle_sql_columns(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_columns(message, state)

            @self.dp.message(StateFilter(SqlGeneratorStates.waiting_for_where))
            async def handle_sql_where(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_where(message, state)

            @self.dp.message(StateFilter(SqlGeneratorStates.waiting_for_limit))
            async def handle_sql_limit(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_limit(message, state)

            @self.dp.message(StateFilter(SqlGeneratorStates.waiting_for_choice))
            async def handle_sql_choice(message: Message, state: FSMContext):
                if message.text == "/help":
                    await self.handle_help_command(message, state)
                    return
                await process_sql_choice(message, state)

            # Главный обработчик текстовых сообщений
            @self.dp.message()
            async def handle_text(message: Message, state: FSMContext):
                text = message.text.lower()
                if text in self.text_commands:
                    await self.text_commands[text](message, state)
                else:
                    current_state = await state.get_state()
                    if not current_state:
                        await message.answer(MENU_MSG, reply_markup=get_main_menu())

            logger.info("Все обработчики успешно зарегистрированы")
            
        except Exception as e:
            logger.error(f"Ошибка регистрации обработчиков: {e}", exc_info=True)
            raise
